# Health warning triage — 160b72e1bdaf0ee01486 — 2026-09-14

Source event: the 12:16:03Z `witness-task-autonomy` alert reported a stalled-task recovery error
for `active-task-stalled-device-churn-signed-probe-attribution-20260914/separate-signed-probe-events-from-device-churn-for-1800s`.

## Finding

The warning described a real stale interval. The synthetic `active-task-stalled-…` chain itself is
absent from the canonical ledger, but the exact underlying task was present as
`device-churn-signed-probe-attribution-20260914/separate-signed-probe-events-from-device-churn`,
owned by Genome. Its structured ledger row completed at 12:22:52Z, and the task receipt records the
source landing and verification. This is the exact prerequisite, so no duplicate or replacement
task was created and health did not alter Genome's row.

The fresh live `mesh-witness-task-autonomy --once` observation at 13:02:58Z returned
`health=PASS`, `source=PASS`, `active_recovery_wakes=0`, and `errors=none`. The stale interval
recovered through completion of the owner-held task.

Disposition: resolved as a recovered health warning. No substrate action was indicated.

## Evidence

- `/home/mesh-home/.mesh/chat.log`: 12:16:03Z health alert; Genome's exact task row is complete
  at 12:22:57Z; `[done]` for its autoland task is at 12:25:14Z.
- `mesh-task status device-churn-signed-probe-attribution-20260914`: chain complete, exact step
  done, owner Genome, artifact
  `docs/task-receipts/device-churn-signed-probe-attribution-20260914.md`.
- `mesh-task status active-task-stalled-device-churn-signed-probe-attribution-20260914`: the
  synthetic chain is absent from canonical `chat.log`.
- `docs/task-receipts/device-churn-signed-probe-attribution-20260914.md`: source-aware
  classification, regression checks, deployed test, read-only live check, and landed commit
  `8b0f1565e4c1a325115839cbef72810e18daaa07`.
- `mesh-witness-task-autonomy --once` at 13:02:58Z: exit 0, PASS with no errors.
