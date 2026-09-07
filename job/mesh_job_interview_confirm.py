#!/usr/bin/env python3
"""Promote an employer-confirmed HH interview to the durable calendar and Telegram.

The parser is deliberately conservative: a proposed slot is not an interview unless the
thread contains an explicit acceptance, a date/time matching one of the offered slots, a
meeting link or physical place, and named participants.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import time
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

MSK = ZoneInfo("Europe/Moscow")
HOME = Path.home()
JOB = HOME / ".mesh" / "job"
SCHED = JOB / "schedule.tsv"
LOG = JOB / "hh-drive.log"
LOCK = JOB / ".apply.lock"
COLS = ["id", "state", "start_utc", "dur", "company", "vacancy", "kind", "channel", "contact", "note"]
HH = "mesh-hh-drive"
CAL = "mesh-job-cal"
TG = "mesh-tg"

CONFIRM_MARKERS = re.compile(
    r"(?:подтверждаем|подтвержден[аоы]?|назначаем|назначен[аоы]?|"
    r"договорились|подходит|жд[её]м вас|встреча состоится|интервью состоится|"
    r"созвон состоится|встречаемся|готов(?:ы|о) провести)", re.I
)
DATE_TIME = re.compile(
    r"(?<!\d)(?P<day>\d{1,2})[./](?P<month>\d{1,2})"
    r"(?:[./](?P<year>\d{2,4}))?[^\d]{0,18}(?:в\s*)?"
    r"(?P<hour>\d{1,2})[:.](?P<minute>\d{2})(?!\d)", re.I
)
LINK = re.compile(r"https?://[^\s<>\]\[)\"']+", re.I)
PARTICIPANTS = re.compile(
    r"(?:участники|участник[и]? встречи|состав)\s*[:\-]\s*([^\n]+)", re.I
)
PLACE = re.compile(r"(?:офис|адрес|место встречи|локация)\s*[:\-]\s*([^\n]+)", re.I)


def negotiation_rejected(thread_text):
    """Detect HH's current negotiation status in the top of the rendered chat page."""
    return bool(re.search(r"\bRejection\b|\bОтказ\b|отклонено", (thread_text or "")[:1400], re.I))


def _year_for(row):
    try:
        return datetime.strptime(row.get("start_utc", "")[:10], "%Y-%m-%d").year
    except ValueError:
        return datetime.now(MSK).year


def _offered_slots(row):
    out = []
    for m in DATE_TIME.finditer(row.get("note", "")):
        year = int(m.group("year")) if m.group("year") else _year_for(row)
        if year < 100:
            year += 2000
        out.append((year, int(m.group("month")), int(m.group("day")),
                    int(m.group("hour")), int(m.group("minute"))))
    return out


def _confirmed_slot(text, row):
    offered = set(_offered_slots(row))
    for m in DATE_TIME.finditer(text):
        year = int(m.group("year")) if m.group("year") else _year_for(row)
        if year < 100:
            year += 2000
        candidate = (year, int(m.group("month")), int(m.group("day")),
                     int(m.group("hour")), int(m.group("minute")))
        if candidate in offered:
            return datetime(*candidate, tzinfo=MSK)
    return None


def _clean(value):
    return re.sub(r"\s+", " ", value).strip(" \t\r\n.,;")


def extract_confirmation(thread_text, row):
    """Return durable confirmation fields, or None for an incomplete/non-confirmation thread."""
    text = (thread_text or "")[-5000:]
    if not CONFIRM_MARKERS.search(text):
        return None
    dt = _confirmed_slot(text, row)
    if dt is None:
        return None
    links = [u.rstrip(".,;") for u in LINK.findall(text)
             if "hh.ru" not in u.lower() and "headhunter" not in u.lower()]
    place_match = PLACE.search(text)
    place = _clean(place_match.group(1)) if place_match else ""
    place = _clean(re.split(r"\s+участники\s*:", place, maxsplit=1, flags=re.I)[0])
    participant_match = PARTICIPANTS.search(text)
    participants = _clean(participant_match.group(1)) if participant_match else ""
    if not participants or (bool(links) == bool(place)):
        return None
    return {
        "start_utc": dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "participants": participants,
        "link": links[-1] if links else "",
        "place": "" if links else place,
    }


def rows():
    if not SCHED.exists():
        return []
    out = []
    for line in SCHED.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        values = line.split("\t") + [""] * len(COLS)
        out.append(dict(zip(COLS, values[:len(COLS)])))
    return out


def current_proposed(row):
    """Only inspect proposed appointments that are still live or recently elapsed."""
    if row.get("state") != "proposed":
        return False
    offered = _offered_slots(row)
    if offered:
        latest = max(datetime(*slot, tzinfo=MSK) for slot in offered).astimezone(timezone.utc)
        return latest > datetime.now(timezone.utc) - timedelta(minutes=90)
    try:
        start = datetime.strptime(row.get("start_utc", ""), "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return False
    return start > datetime.now(timezone.utc) - timedelta(minutes=90)


def _drive(args, timeout=120):
    return subprocess.run([HH] + args, capture_output=True, text=True, timeout=timeout)


def _js(expr, marker, wait=30):
    before = LOG.stat().st_size if LOG.exists() else 0
    _drive(["--send", "js " + expr])
    for _ in range(wait):
        time.sleep(1)
        with LOG.open("r", encoding="utf-8", errors="replace") as fh:
            fh.seek(before)
            for line in fh:
                if line.startswith("[js] ") and marker in line:
                    try:
                        return json.loads(line[5:])
                    except json.JSONDecodeError:
                        return None
    return None


def read_thread(chat):
    if _drive(["--alive"]).returncode != 0:
        return None
    _drive(["--send", "goto https://hh.ru/chat/%s" % chat])
    time.sleep(1.5)
    marker = "MESH_INTERVIEW_%s" % chat
    expr = "JSON.stringify({marker:%r,url:location.href,text:(document.body.innerText||\"\").replace(/\\s+/g,\" \")})" % marker
    result = _js(expr, marker)
    if not result or result.get("url", "").rstrip("/").endswith("/bad-redirect"):
        return None
    return result.get("text", "")


def _display_time(start_utc):
    dt = datetime.strptime(start_utc, "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc).astimezone(MSK)
    return dt.strftime("%d.%m.%Y %H:%M МСК")


def _prep(row):
    role = row.get("vacancy", "вакансию")
    return "Повторить ключевые проекты и архитектурные решения по роли «%s», подготовить вопросы команде и проверить ссылку/камеру." % role


def _notify(row, confirmation):
    access = confirmation["link"] or confirmation["place"]
    body = ("[job] ИНТЕРВЬЮ подтверждено\n"
            "Компания: %s\nРоль: %s\nДата: %s\n%s\nУчастники: %s\nЧто подготовить: %s" % (
                row.get("company", "?"), row.get("vacancy", "?"),
                _display_time(confirmation["start_utc"]),
                ("Ссылка: " if confirmation["link"] else "Место: ") + access,
                confirmation["participants"], _prep(row)))
    return subprocess.run([TG, body], check=False).returncode == 0


def selftest():
    row = {
        "state": "proposed", "start_utc": "2026-09-08T09:00Z",
        "note": "предложено: вт 08.09 12:00, вт 08.09 13:00 (МСК)",
    }
    accepted = ("Готовы провести интервью во вторник 08.09 в 12:00 МСК. "
                "Подключение: https://meet.example/interview-123 "
                "Участники: Илья и Анна, руководитель команды.")
    got = extract_confirmation(accepted, row)
    assert got and got["start_utc"] == "2026-09-08T09:00Z"
    assert got["link"] == "https://meet.example/interview-123"
    assert got["participants"] == "Илья и Анна, руководитель команды"
    assert extract_confirmation("Спасибо, ближайшие окна: вт 08.09 12:00 (МСК).", row) is None
    assert extract_confirmation("Подтверждаем вт 08.09 в 12:00 МСК. Ссылку пришлём позже.", row) is None
    assert not current_proposed({"state": "proposed", "start_utc": "2020-01-01T09:00Z"})
    assert negotiation_rejected("Backend-разработчик 15:55 ИНКОМСИСТЕМ Rejection")
    print("mesh-job-confirm: ok")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.test:
        selftest()
        return 0
    from mesh_job_hh_lock import hh_driver_lock
    found = []
    with hh_driver_lock(LOCK, wait=0, mode="confirm") as (acquired, reason):
        if not acquired:
            print("mesh-job-confirm: n/a — %s" % reason, file=os.sys.stderr)
            return 2
        for row in rows():
            if row.get("state") != "proposed" or not row.get("channel", "").startswith("hh-чат "):
                continue
            if not current_proposed(row):
                subprocess.run([CAL, "--cancel", row["id"]], capture_output=True, text=True)
                continue
            chat = row["channel"].split()[-1]
            thread = read_thread(chat) or ""
            if negotiation_rejected(thread):
                subprocess.run([CAL, "--cancel", row["id"]], capture_output=True, text=True)
                continue
            confirmation = extract_confirmation(thread, row)
            if not confirmation:
                continue
            result = subprocess.run([
                CAL, "--confirm", row["id"], "--participants", confirmation["participants"],
                *( ["--link", confirmation["link"]] if confirmation["link"] else ["--place", confirmation["place"]] ),
                "--source", "HH chat %s" % chat,
            ], capture_output=True, text=True)
            if result.returncode != 0:
                continue
            notified = _notify(row, confirmation)
            found.append({"id": row["id"], "company": row["company"],
                          "vacancy": row["vacancy"], "notified": notified,
                          **confirmation})
    if args.json:
        print(json.dumps(found, ensure_ascii=False, indent=1))
    else:
        for item in found:
            print("confirmed %s — %s%s" % (item["company"], item["vacancy"],
                                            " (TG sent)" if item["notified"] else " (TG failed)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
