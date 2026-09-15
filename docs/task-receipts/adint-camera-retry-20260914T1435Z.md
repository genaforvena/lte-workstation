# adint camera resolver retry — 2026-09-14 14:35 UTC

Consumed the live `adint` stream with `mesh-dash --once adint`. It still reports
`step0d-hb-first-cell` active and the room-camera resolver
`unblock/adint/3dd6562eb2e7cc86/resolve` undischarged. The resolver is owned by `adint` and
already has a specific capability retry condition in the ledger.

The prior reconciliation artifact is
[`adint-room-revival-resolver-reconciliation-20260913.md`](adint-room-revival-resolver-reconciliation-20260913.md):
the primary iMac room camera remains unavailable until bounded SSH succeeds, followed by a real
`mesh-imac-cam --test` read. I retried that exact read-only reachability probe:

```text
timeout 8s ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@192.168.8.214 true
exit 255
ssh: connect to host 192.168.8.214 port 22: Connection timed out
```

The retry event did not occur, so the resolver remains blocked on SSH reachability; the camera test
was correctly not attempted. `mesh-task queue --dispatch --owner adint` returned no eligible owned
rows. No mesh task was taken.
