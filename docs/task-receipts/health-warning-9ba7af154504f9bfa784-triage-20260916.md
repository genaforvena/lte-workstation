# Health-warning triage: witness-task-autonomy

The owned warning was emitted at 2026-09-15T19:21:54Z with three
`reconcile-still-in-owner-queue` errors for `check-witness-chat-range` review
tasks. The warning is stale as a current fleet condition.

Evidence inspected on 2026-09-16:

- `/home/mesh-home/.mesh/chat.log:67668` contains the source FAIL at 19:21:54Z.
- `/home/mesh-home/.mesh/witness-task-autonomy.log` contains later PASS runs at
  01:40:15Z, 01:45:16Z, 01:50:14Z, and 01:55:13Z, all with `source=PASS` and
  `errors=none`.
- The subsequent 02:00:24Z and 02:05:19Z FAIL rows concern newer active-stall
  warnings (`operator-intake` and `senses-ambient-stale-followup`), not the
  19:21 queue-reconciliation warning.
- `mesh-task queue --dispatch --owner health` returned the newer exact-owner
  row `health-warning/9ba7af154504f9bfa784/triage`; its dispatch check exited 0
  before the owner-authored take.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/9ba7af154504f9bfa784 triage`
  recorded `status=active` in `/home/mesh-home/.mesh/chat.log` at 02:15:01Z.

Conclusion: no repository or substrate repair is justified for this stale
warning. Keep monitoring for a new unpredicted witness failure; the newer
02:00–02:05 active-stall warnings are separate queue work.
