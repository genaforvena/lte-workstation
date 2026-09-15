# Job HH start-lock resolver — 2026-09-12

Resolver: `unblock/job/6f9ee08d62753858/resolve` (owner `job`). The parent
`job-autonomy-followups-20260912/recover-hh-communications` remains blocked.

## Finding

At 2026-09-12T06:17Z, `mesh-hh-drive --alive` reported `down`; the HH command
queue was still 0 bytes. The start-lock path was a regular file on the local
root filesystem, device `64512` (`fc:00`), inode `7362721`. `/proc/locks`
contained `FLOCK ADVISORY WRITE 2198814 fc:00:7362721 0 EOF`, confirming an
exclusive lock on that exact file. PID `2198814` was absent from this node's
`/proc`, and no HH driver, Playwright, or Chromium process was visible. The
holder therefore cannot be inspected or safely stopped from this PID
namespace. The lock is held by the kernel; the pathname itself is not evidence
of a stale lock that can be removed.

## Disposition and next action

No safe local prerequisite/fix is available while that holder remains. Do not
unlink or bypass the lock, write/replay the HH command queue, or launch a second
browser. The required external event is release of the lock by its current
holder, or completion of that holder's start such that `mesh-hh-drive --alive`
reports `up`.

After that event, as `job`: verify `wc -c ~/.mesh/job/hh-cmd.txt` is `0`, run
`mesh-hh-drive --alive`, and only if it still reports down run
`mesh-hh-drive --start` once. Confirm the driver is up and then resume
`job-autonomy-followups-20260912/recover-hh-communications` to inspect chats
`5617701145` / UIDs `18328`, `18382`, and `18401`. Never replay
`~/.mesh/job/hh-cmd.replay-backup-20260912T034053Z.txt`.

No employer messages were sent during this diagnosis. The parent task remains
blocked until the stated external event is verified.
