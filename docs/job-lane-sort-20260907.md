# Job lane sort — 2026-09-07

Источник состояния: `~/.mesh/job-board.tsv`, `~/.mesh/job/cal-state.json`,
`~/.mesh/job/chatwatch-verdicts.log`.

## Result

- Durable confirmed interviews: **0**.
- Active proposed interview threads: **2**; both are waiting for employer confirmation:
  - `Рекрутер` — `Senior Backend разработчик Go`, HH chat `5598744817`; proposed
    07 Sep 2026 at 14:00/15:00/16:00/17:00 MSK.
  - `ИНКОМСИСТЕМ, НИЦ` — `Backend-разработчик (Node.js / TypeScript)`, HH chat
    `5602196687`; proposed 07 Sep at 16:00/17:00/18:00 or 08 Sep at 12:00 MSK.
- The 7 board rows marked `interview` are not confirmed calendar rows. They include
  stale or application-state records (Future Focus, Бегачева, Сбер Python, Atsearch,
  Сбер GigaChat, and the two current vacancy records above); none has the required
  durable confirmation fields: exact time, participants, link/place, and source.

## Verification

- `job/mesh-job-cal --agenda --json`: exactly 2 rows, both `state=proposed`.
- `job/mesh-job-chatwatch --check`: lock free, 238 chats known.
- Latest chatwatch read: `203` rows, `coverage=prefix`, `live=9`, `new=0`.
- No Telegram interview alert was sent because no confirmed interview exists.

Next action: continue the scheduled chatwatch/reply loop; when an employer confirms a
slot with link or place and participants, write a `confirmed` calendar row first and
send the interview alert in the required format.
