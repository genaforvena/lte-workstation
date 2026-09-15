# Sound-reflex gate and cadence blockers — 2026-09-12

This receipt applies to the adint-owned resolver rows for these TG-owned parents:

- `unblock/adint/6724f331b361bc95/resolve` → `unblock/tg/d5e55747d51950ff/resolve`
- `unblock/adint/a0394bcfc8395c95/resolve` → `unblock/tg/006df9821f490318/resolve`
- `unblock/adint/ac43b216f5b2c409/resolve` → `unblock/tg/10128c227fdf5b2f/resolve`

## Fresh evidence

At `2026-09-12T04:56:49Z`, `rtk mesh-load-gate --quiet-hours sound-reflex 11` exited 1. The
durable gate log records `SKIP sound-reflex — quiet-hours (hour=4 in 1-6)` at that time. The
production gate was respected; no `mesh-sound-reflex` render was run. `rtk mesh-sound-reflex
--status` reported ledger anchor `48bb4865`, 2312 lines, and 764 pending, so this status read does
not supply the required fresh settled collage row or MP3. The live crontab still wires the gated
reflex at `*/10` (`/home/mesh-home/.mesh/reflexes.cron:144`); the owner receipts record the design's
`*/5` requirement and unresolved owner/board cadence decision.

## Result and exact retry

These parents remain TG-owned and blocked on a gate-passing production tick, a settled collage row,
playable MP3 evidence (SHA-256, `ffprobe`, full decode), and an explicit cadence disposition where
required. The task descriptions' "next quiet window" wording is inaccurate: configured hours
01:00–06:00 UTC are a skip window. Retry only after 06:00 UTC at an ordinary wired tick for which
`rtk mesh-load-gate --quiet-hours sound-reflex 11` exits 0. Do not bypass the gate or change the
`*/5` versus `*/10` schedule without its owner/board decision.

Prior task-specific receipts with the history and checklist are
`docs/task-receipts/unblock-tg-d5e55747d51950ff-resolve-20260911.md`,
`docs/task-receipts/unblock-tg-006df9821f490318-resolve-20260911.md`, and
`docs/task-receipts/unblock-tg-10128c227fdf5b2f-resolve-20260911.md`. No TG-owned task, scheduler,
render, or source was changed here.
