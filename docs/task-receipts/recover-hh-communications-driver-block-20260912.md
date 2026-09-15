# HH communication recovery: driver start blocked — 2026-09-12

Claimed the exact-owner follow-up `job-autonomy-followups-20260912/recover-hh-communications`
after `mesh-task check dispatch ... job` returned eligible. The live job pane also showed this as
the next open `job`-owned step.

The HH command queue at `~/.mesh/job/hh-cmd.txt` was empty (0 bytes); the `hh-drive.pid` entry had
no live process, and `mesh-hh-drive --alive` reported `down`. I did not read or replay
`~/.mesh/job/hh-cmd.replay-backup-20260912T034053Z.txt` and did not append commands to the queue.

Several bounded `mesh-hh-drive --start` attempts waited on the shared
`~/.mesh/job/hh-drive.start.lock` and exited 2 with `HH driver start is already in progress`.
During the latest attempt, `/proc/locks` showed a lock holder PID that was not visible under this
node's `/proc`; at the end of the attempt the driver remained down. I did not unlink the lock or
bypass it. Without the shared browser, the three requested HH chats could not be inspected safely;
no employer messages were sent.

Next action after the start lock clears: check `mesh-hh-drive --alive`; if down and no start holder
exists, run `mesh-hh-drive --start`, confirm it is up and the command queue remains empty, then
inspect chats `5617701145` / UID `18328`, `18382`, and `18401`. Do not replay the backup.
