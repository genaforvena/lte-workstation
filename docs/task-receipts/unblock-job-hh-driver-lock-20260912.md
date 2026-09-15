# Job HH start-lock blocker disposition — 2026-09-12

The parent task `job-autonomy-followups-20260912/recover-hh-communications` is blocked on the HH
start lock. The browser reports down, the command queue is 0 bytes, and bounded
`mesh-hh-drive --start` attempts return 2 with `HH driver start is already in progress`. The lock
owner shown in `/proc/locks` is not visible in this node's `/proc`; its owner cannot be inspected or
stopped safely from this window.

No local lock deletion, bypass, command-queue write, or archived replay is safe: any could permit a
second HH browser against the same login or deliver an unknown queued verb. The remaining external
prerequisite is that the current holder release
`~/.mesh/job/hh-drive.start.lock` (or complete its start and make `mesh-hh-drive --alive` report
up).

Once the holder releases the lock, the job window should verify `~/.mesh/job/hh-cmd.txt` is still
empty, run `mesh-hh-drive --alive`, and, only if it remains down, run `mesh-hh-drive --start` once.
After the driver is up, resume the parent task and inspect chats `5617701145` / UID `18328`, `18382`,
and `18401`. Do not replay `~/.mesh/job/hh-cmd.replay-backup-20260912T034053Z.txt`.

No employer messages were sent. This artifact records the external prerequisite; it does not satisfy
it, so the parent task must remain blocked until the lock condition changes.
