#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
PYTHONPATH="$root/job" python3 - <<'PY'
from mesh_job_interview_confirm import extract_confirmation, current_proposed, negotiation_rejected

row = {
    "id": "c1",
    "state": "proposed",
    "start_utc": "2026-09-08T09:00Z",  # 12:00 MSK
    "company": "Example",
    "vacancy": "Senior Go",
    "channel": "hh-чат 123",
    "note": "предложено: вт 08.09 12:00, вт 08.09 13:00 (МСК)",
}

confirmed = """
Илья, здравствуйте! Готовы провести интервью во вторник 08.09 в 12:00 МСК.
Подключение: https://meet.example/interview-123
Участники: Илья и Анна, руководитель команды.
"""
got = extract_confirmation(confirmed, row)
assert got == {
    "start_utc": "2026-09-08T09:00Z",
    "participants": "Илья и Анна, руководитель команды",
    "link": "https://meet.example/interview-123",
    "place": "",
}, got

assert extract_confirmation(
    "Спасибо! Ближайшие свободные окна: вт 08.09 12:00, вт 08.09 13:00 (МСК).",
    row,
) is None
assert extract_confirmation(
    "Подтверждаем вт 08.09 в 12:00 МСК. Ссылку пришлём позже.", row
) is None

place = extract_confirmation(
    "Подтверждаем встречу 08.09 в 12:00 МСК, офис: Казань, ул. Восстания, 104И. "
    "Участники: рекрутер и Илья.", row
)
assert place == {
    "start_utc": "2026-09-08T09:00Z",
    "participants": "рекрутер и Илья",
    "link": "",
    "place": "Казань, ул. Восстания, 104И",
}, place

assert not current_proposed({"state": "proposed", "start_utc": "2020-01-01T09:00Z",
                             "note": "предложено: пн 01.01 12:00 (МСК)"})
assert current_proposed({"state": "proposed", "start_utc": "2026-01-01T09:00Z",
                         "note": "предложено: вт 08.09 12:00 (МСК)"})
assert negotiation_rejected("Backend-разработчик 15:55 ИНКОМСИСТЕМ Rejection")
assert not negotiation_rejected("Backend-разработчик 15:55 ИНКОМСИСТЕМ Interview")

print("test-job-interview-confirm: ok")
PY

[[ "$(PYTHONPATH="$root/job" python3 -m mesh_job_interview_confirm --test)" == "mesh-job-confirm: ok" ]]
[[ "$(cd /tmp && "$root/job/mesh-job-confirm" --test)" == "mesh-job-confirm: ok" ]]
[[ "$(cd /tmp && "$HOME/.local/bin/mesh-job-confirm" --test)" == "mesh-job-confirm: ok" ]]
