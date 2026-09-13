# Devcoredump listener current-state verification

Verified: 2026-09-13T16:42:51Z

## Live status

The count-142 event came from phaedra. There, `mesh-devcd-catch --status` reported `ARMED
(disabled=0)`, zero live dumps, listener `UP (pid 4162320)`, zero restarts in the previous 24 hours,
and the supervisor registry row present. `ps` showed that PID as
`bash /root/.local/bin/mesh-devcd-catch --listen`, started 2026-08-27T20:01:09Z. The listener-up and
repair ledger entries are from 20:01:09Z and 20:01:23Z that day; no recovery action was needed during
this verification.

## Cause and recovery

The count-142 recurrence's latest source event was 2026-08-27T19:25:03Z. Phaedra's listener was
re-registered and repaired at 20:01:02Z/20:01:23Z and has remained up since. A separate mesh-home
FYI at 2026-09-13T11:37:18Z described a real outage on mesh-home: the listener was absent and the
healer's supervisor call returned 0 without restoring it. The supervisor log attributes the later
restart to an unknown signal. Its repair gap came from concurrent `mesh-supervise` calls: the
nonblocking lock path logged `SKIP` but returned success, so the healer treated an unrun
reconciliation as a completed attempt. At 11:38:03Z the active supervisor restarted it; the healer
verified pid 173301 at 11:38:14Z. The correction is already landed and deployed: bounded 65-second
lock waiting, an explicit rc 75 `LOCK-TIMEOUT`, and the same wait allowance in the devcd healer. See
commits `582009b3` (`Wait for active supervisor before claiming child checks ran`) and `2b4c6890`
(`Keep devcoredump listener repair alive through lock waits`).

## Stale-pane correction and fresh verification

The witness pane's `root-mesh-devcd-catch ... count=142 task:none` was a recurrence summary of
append-only historical FYIs, not a live listener verdict. Its latest source is line 21790 in
`~/.mesh/chat.log`: `2026-08-27T19:25:03Z root/mesh-devcd-catch@phaedra`, a full 17 days before this
verification. The separate mesh-home alert at 11:37Z is a different recurrence. The count-only view
omitted the newest event timestamp, making the old phaedra down event read as current.
`mesh-fyi-ledger` now adds `latest=<UTC timestamp>` to each recurring FYI line; the refreshed pane
shows `count=142 latest=2026-08-27T19:25:03Z task:none`. Its focused regression test passes
(`tests/test-mesh-fyi-ledger.sh`).

Fresh commands at verification time: `ssh phaedra '/root/.local/bin/mesh-devcd-catch --status'` —
listener UP pid 4162320, channel armed, no live dumps, registry row present; and mesh-home
`mesh-devcd-catch --status` — listener UP pid 173301, channel armed, no live dumps, registry row
present. No current service blocker remains on either host.
