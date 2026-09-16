# Health warning triage — 2026-09-16

Task: `health-warning/149d50e18f7d12f8cd77/triage`

## Live evidence

- Fresh `timeout 20s mesh-dash --once check`: exit `124`; no completed fresh
  rendering was available from this attempt.
- Fresh `timeout 20s mesh-load-gate --quiet-hours witness`: exit `1`.
- Node state: `CRITICAL|entropy=OFFLINE|sockstat=BUSY|swap=CRITICAL|loadavg=OVERLOADED|psi=STALLED|psimem=QUIET|loadavg (critical input)`.
- The prior live dash rendered `PROBE-WARNING: LOCAL LOAD HIGH`; its fleet
  reachability results are therefore unreliable. GPU and egress were healthy
  in that same reading.
- The witness autonomy log continues to report failures naming stalled and
  recovery tasks; the original warning is not reconciled.

## Disposition

This is a mesh-owned transient resource block, not a cleared warning. Do not
run the bounded witness check while the load gate is closed.

## Exact retry edge

After load normalization, run `mesh-dash --once check` and require the output
to omit `PROBE-WARNING: LOCAL LOAD HIGH`; then require
`mesh-load-gate --quiet-hours witness` to exit `0`; then run
`timeout 30s mesh-witness-task-autonomy --once`. Accept only a new timestamped
row in `/home/mesh-home/.mesh/witness-task-autonomy.log`, and reconcile its
warning IDs against the canonical ledger.
