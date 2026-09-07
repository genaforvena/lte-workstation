# Job HH serialization repair — 2026-09-07

## Finding

The reply reflex was repeatedly reporting `nav-failed` while the HH session was valid. The shared
`mesh-hh-drive` log showed interleaved `goto`, `settext`, and `click` commands from multiple
browser writers. A cron `mesh-job-apply --tg` process then remained alive for 4h18m holding
`~/.mesh/job/.apply.lock` after repeated 300-second driver failures.

## Change

`job/mesh_job_hh_lock.py` provides a flock-based shared HH-driver guard. `mesh-job-reply` and
`mesh-job-apply-getmatch` now use the same `.apply.lock` before reading or writing HH, report a
named collision, and age the marker after reply releases the flock so chatwatch does not stand down
for 15 minutes after reply is already finished. The production copies and helper under
`~/.local/bin` were updated too, because cron runs those copies.

The shared helper also installs TERM/HUP handlers for lock-owning processes. This matters because
cron/watchdog timeouts otherwise terminate Python before `finally` runs, leaving a fresh marker
that falsely blocks chatwatch.

## Verification

- `tests/test-job-hh-serialization.sh` — PASS
- `job/mesh-job-reply --test` — PASS (one later rerun was interrupted after the live HH probe
  stalled; the earlier complete run ended `mesh-job-reply --test: ok`)
- `job/mesh-job-cal --test` — PASS
- `job/mesh-job-apply-getmatch --test` — PASS (`smoke-test: ok`)
- production getmatch busy-lock gate — PASS (rc=2 with named holder)
- SIGTERM lock-cleanup regression — PASS
- production copy `~/.local/bin/mesh-job-reply --print-knobs` imports the helper; unarmed gate
  returns rc=2
- live HH negotiations page was readable (`All 352`); no confirmed calendar row was produced
- current calendar remains two `proposed` rows and zero durable confirmed interviews

## Remaining state

The external HH/browser environment can still be contended by non-job browser sessions. The job
lane now refuses a collision rather than interleaving commands; cron continues scanning, applying,
mailing, watching chats, replying, and checking the calendar.
