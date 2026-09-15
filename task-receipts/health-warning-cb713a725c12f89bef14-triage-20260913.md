# Health warning triage — cb713a725c12f89bef14 — 2026-09-13

The source alert at 18:52:13Z reported `queue-rc-124` from
`mesh-witness-task-autonomy`. In `scripts/mesh-witness-task-autonomy`, the global
`mesh-task queue --dispatch` probe has a 60-second timeout; return code 124 is the
timeout path in `command()`.

The same witness tape shows the failure at 18:49:39Z with `dispatchable=0` and
`checks=0`, then a healthy run at 18:51:18Z with six dispatchable rows and six
successful checks. It stayed healthy at 18:55:07Z, 19:00:18Z, 19:06:15Z, and
19:10:16Z. At 19:12:27Z, a fresh `mesh-task queue --dispatch` completed with exit
0 and returned current canonical rows. The task journal and source were passing
on the failed run, and no absent input or registration was indicated.

Disposition: **transient timeout recovered**. Evidence does not identify why that
single invocation exceeded its timeout, so this receipt does not claim a root
cause. The live command and subsequent scheduled observations show that the
queue path recovered without prerequisite repair. No task owned by another mind
was changed and no code or substrate change was made.

Evidence: `/home/mesh-home/.mesh/chat.log` (18:52:13Z alert); the matching
`/home/mesh-home/.mesh/witness-task-autonomy.log` records from 18:49:39Z through
19:10:16Z; `scripts/mesh-witness-task-autonomy` (`command()` timeout and global
queue probe); and the successful live `mesh-task queue --dispatch` at 19:12:27Z.
