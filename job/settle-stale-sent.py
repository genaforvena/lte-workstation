#!/usr/bin/env python3
"""Settle the job board's stale awaiting-reply cohort from the reply tape.

The pane names the sent/replied set "chase or drop" and nothing owned it. This settles two halves
of it from EVIDENCE THE LANE ALREADY HOLDS, never by guessing:

1. REPLIED — ~/.mesh/job/reply-state.json is keyed by hh vacancy id and carries a confirmed
   employer chat. A board row still on `sent` for a vacancy present there has an answer; the board
   was the thing that lagged, not the application.
2. STALE   — a `sent`/`replied` row whose application is >= 30 days old. An hh vacancy closes in
   that window and the silence is an answer, so leaving it `sent` is not a live application but an
   unmeasured funnel number. These go to `dropped` with the age recorded — the board's own exit for
   "the vacancy is gone" (mesh-job-apply:settle_capped uses `dropped` for exactly that case).

The write goes through mesh-job-mail's board_mark, the lane's own in-place writer, keyed by hh
vacancy ID. This tool NEVER matches on a title — board_mark exists because a title match flipped
five employers' rows off one company's autoreply. Verified first: the 3x АНТРАКС rows are three
distinct vacancy ids, so no row is a duplicate to merge.

board_mark rewrites only the state column, so the reason is written as a separate pass and the
before/after funnel is printed; every change is auditable and reversible from the printed diff.

usage: settle-stale-sent.py [--apply]    # default is a dry run that changes nothing
"""
import datetime, types
import json
import pathlib
import sys

HOME = pathlib.Path.home()
BOARD = HOME / ".mesh" / "job-board.tsv"
REPLY_STATE = HOME / ".mesh" / "job/reply-state.json"
MAIL = HOME / ".local/bin/mesh-job-mail"
CUTOFF_DAYS = 30
TODAY = datetime.date(2026, 9, 23)
CUTOFF = TODAY - datetime.timedelta(days=CUTOFF_DAYS)
def load_mail_board_mark():
    """Import board_mark from the deployed mail tool rather than re-implementing the writer.
    It is an extensionless executable, so load it as source and exec under a module namespace."""
    src = MAIL.read_text(encoding="utf-8")
    mod = types.ModuleType("mesh_job_mail")
    mod.__file__ = str(MAIL)
    exec(compile(src, str(MAIL), "exec"), mod.__dict__)
    return mod.board_mark, mod.BOARD


def vid_of(link):
    return (link.rstrip("/").rsplit("/", 1)[-1] or None) if link else None


def read_board():
    raw = BOARD.read_text(encoding="utf-8").splitlines()
    header = [c.lstrip("# ").rstrip() for c in raw[0].split("\t")]
    idx = {n: header.index(n) for n in ("date", "company", "role", "link", "state", "note")}
    return header, raw, idx


def set_note(vid, reason):
    """Append the reason to a row's note. The key is the vacancy id in the link column."""
    header, raw, idx = read_board()
    out, n = [], 0
    for line in raw:
        f = line.split("\t")
        if vid_of(f[idx["link"]]) == vid:
            old = f[idx["note"]]
            f[idx["note"]] = (old + " || " if old else "") + reason
            n += 1
        out.append("\t".join(f))
    BOARD.write_text("\n".join(out) + "\n", encoding="utf-8")
    return n


def state_of(vid):
    _, raw, idx = read_board()
    for line in raw[1:]:
        f = line.split("\t")
        if vid_of(f[idx["link"]]) == vid:
            return f[idx["state"]], f[idx["date"]][:10], f[idx["company"]]
    return None, None, None


def funnel():
    _, raw, idx = read_board()
    out = {}
    for line in raw[1:]:
        f = line.split("\t")
        out[f[idx["state"]]] = out.get(f[idx["state"]], 0) + 1
    return out


def settle(vid, state_word, reason, apply_changes, board_mark, stats):
    old, date, company = state_of(vid)
    if old is None or old == state_word:
        return
    print("  %s %-40s %s -> %s" % (date, company[:40], old, state_word))
    if apply_changes:
        board_mark(vid, None, None, state_word)
        set_note(vid, reason)
        got, _, _ = state_of(vid)
        if got != state_word:
            print("FAIL: settle of %s did not stick (got %s)" % (vid, got), file=sys.stderr)
            stats["failed"] += 1
            return
    stats[state_word] += 1


def main():
    apply_changes = "--apply" in sys.argv
    if not apply_changes:
        print("DRY RUN — nothing is changed. Pass --apply to settle.\n")

    board_mark, _mail_board = load_mail_board_mark()
    _, raw, idx = read_board()
    rows = [dict(zip(("date", "company", "link", "state"), (
        f[idx["date"]], f[idx["company"]], f[idx["link"]], f[idx["state"]])))
        for f in (l.split("\t") for l in raw[1:])]
    replies = json.loads(REPLY_STATE.read_text(encoding="utf-8"))
    print("reply tape: %d vacancy ids with an employer chat" % len(replies))

    stats = {"replied": 0, "dropped": 0, "failed": 0}
    print("\n-- rows the reply tape shows an ANSWER for, still on `sent` --")
    for r in rows:
        vid = vid_of(r["link"])
        if r["state"] == "sent" and vid in replies and replies[vid].get("confirmed"):
            settle(vid, "replied",
                   "2026-09-23: сверка с reply-state.json — есть подтверждённый чат %s (%s); "
                   "доска отставала, не заявка" % (replies[vid].get("chat"), replies[vid].get("sent", "")),
                   apply_changes, board_mark, stats)

    print("\n-- `sent` rows >= %d days old with no employer answer (vacancy closed) --" % CUTOFF_DAYS)
    # A `replied` row is documented employer contact — it is never silence. Settling one to
    # `dropped` would erase the reply from the funnel, so the stale settle touches only `sent`.
    # Likewise a row with live chat traffic is not silent even if the board never caught up to it.
    live_chats = {rec.get("chat") for rec in replies.values() if rec.get("chat")}
    for r in rows:
        vid = vid_of(r["link"])
        try:
            d = datetime.date.fromisoformat(r["date"][:10])
        except ValueError:
            continue
        if r["state"] != "sent" or d >= CUTOFF:
            continue
        if vid in replies:
            print("  SKIP %s %s — reply tape has a chat for this vacancy" % (d.isoformat(), r["company"][:36]))
            continue
        settle(vid, "dropped",
               "2026-09-23: нет ответа работодателя %d дн (с %s) — вакансия закрыта, исход не "
               "измерен; снимаю с ожидания" % ((TODAY - d).days, d.isoformat()),
               apply_changes, board_mark, stats)

    print("\nsettled: %d replied, %d dropped%s"
          % (stats["replied"], stats["dropped"],
             ", %d FAILED" % stats["failed"] if stats["failed"] else ""))
    return 1 if stats["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
