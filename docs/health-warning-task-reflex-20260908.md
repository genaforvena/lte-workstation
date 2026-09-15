# Health-warning task reflex — 2026-09-08

`scripts/mesh-health-warning-task` tails `~/.mesh/chat.log` from an atomic byte
cursor. It recognizes `room sense ... lost` messages, explicit
`[health-warning]`/`[warning]`/`[alarm]` records, and warning-bearing `[check]` or
`[fyi]` records from health/watch/sense/doctor/fleet/reflex producers.

Each new incident is fingerprinted and materialized with `mesh-task create` as
`health-warning/<fingerprint>/triage`, with `health` as the exact owner. The
existing `mesh-task-journal` then exposes the durable chain in `~/.mesh/tasks.journal`.
Task and task-state records are excluded from matching so the writer cannot
re-ingest its own output. A failed create leaves the cursor before that source
line for retry.

Wiring:

- declared example: `scripts/reflexes.cron.example`
- node desired set: `~/.mesh/reflexes.cron`
- live crontab: `* * * * * /home/mesh-home/.local/bin/mesh-health-warning-task ...`
- deployed copy: `~/.local/bin/mesh-health-warning-task` (SHA-256 matches source)

Verification performed:

- `tests/test-mesh-health-warning-task.py`: pass, including deduplication and
  ignoring quoted `[health-warning]` text inside generated `[task]` records.
- isolated real `mesh-task` run: exactly one `[task]` record, `QUEUED` with owner
  `health`, and no self-recursion.
- live recent-window run: four warning chains created and `mesh-task-journal`
  published them as `QUEUED\thealth\thealth-warning/...` rows.
- `mesh-dms` fenced the crontab change; the scheduler has since touched
  `~/.mesh/health-warning-task.log` at 10:13Z.

The log retains the earlier pre-fix PATH failure as historical evidence; the
deployed default now invokes the absolute `~/.local/bin/mesh-task` path, and the
cursor remains retryable if a future task creation fails.
