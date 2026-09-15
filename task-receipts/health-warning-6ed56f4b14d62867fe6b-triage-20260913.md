# Health warning triage — `health-warning/6ed56f4b14d62867fe6b`

Source event: the 2026-09-13T20:27:47Z `witness-task-autonomy` alert reported
`source=FAIL` with `journal-rc-1;journal-source-not-PASS`.

## Finding

This was a transient task-journal failure. The witness tape records a failed run at
20:25:44Z, then a normal run at 20:30:15Z with `health=PASS source=PASS` and no errors.
An independent live rebuild at 20:31:11Z also exited 0 and published
`~/.mesh/tasks.journal` with `task_source=PASS`, `source_errors=0`, all 61,010 of
61,010 source events replayed, and SHA-256
`b8c4b06d9009709938030986629c24e881c9f3504f9f6e3927392e93792a8ec1`.

The failing run's tape contains only the journal return code, not its stderr. Source review
shows exit 1 can mean an incomplete `chat.log` event, task-audit failure/timeout, or an
invalid audit row. The later source is complete and valid, so the exact failing branch and
input cannot be recovered from retained evidence. Do not claim a specific root cause.

The journal's active rows and task audit are readable now; no missing prerequisite is
identified. `mesh-reflex-health --check` reports the scheduled reflex cohort fresh, and the
actual 20:30 witness run confirms recovery. Its cadence is aliased/sample-like, so this is
evidence of a recent pass, not a continuous guarantee.

## Disposition

Recovered on the next scheduled witness run; no code or task-ledger repair is indicated.
Residual blindness: witness records the journal's nonzero status but not the failing
subprocess diagnostic. If it recurs, capture the journal's stderr at failure before treating
the source as persistently broken.

## Evidence

- `/home/mesh-home/.mesh/witness-task-autonomy.log`: 20:25:44Z FAIL and 20:30:15Z PASS.
- `/home/mesh-home/.mesh/tasks.journal`: 20:31:11Z current complete PASS source and task audit.
- `scripts/mesh-task-journal`: the three exit-1 branches and stderr messages.
- `scripts/mesh-witness-task-autonomy`: failure classification and summary emission.
- `mesh-reflex-health --check`: scheduled reflexes fresh at 20:32Z.
