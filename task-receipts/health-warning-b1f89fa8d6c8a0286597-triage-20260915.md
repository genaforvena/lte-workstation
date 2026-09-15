# Health warning triage — witness task autonomy

Task: `health-warning/b1f89fa8d6c8a0286597/triage`
Owner: `health`
Observed: 2026-09-15T23:33Z–23:35Z UTC

## Finding

The warning reported `witness-task-autonomy` failure with a reconciliation
error for `health-warning/bf4309521d1101a1961e/triage`. The exact row was later
owner-claimed by `health` and completed with receipt
`task-receipts/health-warning-bf4309521d1101a1961e-triage-20260915.md`.

Live evidence:

- Before this triage, `mesh-task queue --dispatch --owner health` returned the
  warning row as eligible; `mesh-task check dispatch ... health` returned 0.
- The row was taken with `MESH_TASK_ACTOR=health` and then closed with the
  receipt above. `mesh-task status` reported the parent `[complete]` and the
  step `[done]`.
- A fresh `timeout 45s mesh-witness-task-autonomy --once` did not complete and
  returned rc=124. No new RUN line was emitted during the timeout.
- The latest available journal line at 22:50:46Z still reported
  `health=FAIL ... check-health-warning/b1f89fa8d6c8a0286597/triage-for-health-rc-2:reconcile-still-in-owner-queue`.
  That is consistent with the row being queued at the time and is stale after
  the owner-authored take.
- At the failed retry, `llama-server` was sustaining about 237% CPU and the
  host was also running many concurrent `mesh-task check` processes. This is a
  plausible cause of the witness timeout, but not proven as its sole cause.

## Decision

The original warning is stale for the named queued row: that row is now
completed. Fleet/task-autonomy health is not green yet because the fresh
witness run timed out and the last journal sample was FAIL. No substrate
change was safe or necessary. Re-run the witness once CPU/check-process
contention subsides; classify any new error from that fresh run rather than
reusing the stale queue error.

