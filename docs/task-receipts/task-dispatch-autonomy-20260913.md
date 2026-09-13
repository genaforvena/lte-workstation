# Task dispatch autonomy verification

On 2026-09-13, witness found a live health-owned task whose durable task-state
record said `dispatch=failed`: the producer ran with a minimal PATH and the
ledger's board-send path searched only for `mesh-chat` on PATH.  The task was
valid and claimable, but its owner had not received its task receipt.

`mesh-task` now resolves its executable sibling `mesh-chat` when no explicit
`MESH_TASK_CHAT_CMD` is supplied.  This gives cron/reflex producers the same
board-writer resolution already used for task-state records.  The witness
observer also treats an exact-owner `OPEN_UNOWNED ... dispatch=failed` audit
row as a repair obligation and runs `mesh-task reschedule-task <task-id>`.
That reuses the normal owner-directed receipt path; it never claims, reassigns,
or changes the task's priority.

Verification passed:

- `tests/test-mesh-task-dispatch-receipt.sh` creates a chain with
  `PATH=/usr/bin:/bin` and proves the adjacent board writer receives `[task]`.
- `tests/test-mesh-witness-task-autonomy.py` injects an exact-owner failed
  dispatch row and proves exactly one reschedule repair.
- `scripts/mesh-task --test`, `tests/test-mesh-health-warning-task.py`,
  `scripts/mesh-task-unblock-sweep --test`, and the deployed observer test
  pass.
- The real failed health task `health-warning/db7406d244e268b2f003/triage`
  was re-dispatched, and Health took it; the 15:38 UTC installed wrapper run
  recorded `RUN health=PASS ... active=2 dispatch_repairs=0`.

Commit `1fe33339` is pushed to `main`.  Source and installed SHA-256 values
match for `mesh-task` and `mesh-witness-task-autonomy`.
