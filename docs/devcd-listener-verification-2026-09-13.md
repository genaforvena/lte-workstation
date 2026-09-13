# Devcoredump listener current-state verification

Verified: 2026-09-13T16:35:35Z

## Live status

`mesh-devcd-catch --status` on mesh-home reported `ARMED (disabled=0)`, zero live dumps, listener
`UP (pid 173301)`, one restart in the previous 24 hours, and the `devcd-catch` supervisor registry
row present. The listener process was also present as
`bash /home/mesh-home/.local/bin/mesh-devcd-catch --listen`. No recovery action was needed during
this verification.

## Cause and recovery

The 2026-09-13T11:37:18Z FYI was true when emitted: the listener was absent and the healer's
supervisor call returned 0 without restoring it. The supervisor log attributes the later restart to
an unknown signal. The failed repair gap came from concurrent `mesh-supervise` calls: the nonblocking
lock path logged `SKIP` but returned success, so the healer treated an unrun reconciliation as a
completed attempt. At 11:38:03Z the active supervisor restarted the listener; the healer verified
pid 173301 at 11:38:14Z. The correction is already landed and deployed: bounded 65-second lock
waiting, an explicit rc 75 `LOCK-TIMEOUT`, and the same wait allowance in the devcd healer. See
commits `582009b3` (`Wait for active supervisor before claiming child checks ran`) and `2b4c6890`
(`Keep devcoredump listener repair alive through lock waits`).

## Stale-pane correction and fresh verification

The witness pane's `root-mesh-devcd-catch ... count=142 task:none` was a recurrence summary of
append-only historical FYIs, not a live listener verdict. Its source is the 11:37:18Z row in
`~/.mesh/chat.log`; the 11:38:03Z restart and 11:38:14Z repair are later rows. The count-only view
omitted the newest event timestamp, making an old down event read as current. `mesh-fyi-ledger`
now adds `latest=<UTC timestamp>` to each recurring FYI line so the pane exposes recency. Its focused
regression test passes (`tests/test-mesh-fyi-ledger.sh`).

Fresh command at verification time: `mesh-devcd-catch --status` — listener UP pid 173301, channel
armed, no live dumps, registry row present. No current service blocker remains.
