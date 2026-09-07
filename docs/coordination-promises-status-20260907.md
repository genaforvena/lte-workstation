# Promise/status reconciliation — 2026-09-07

## Finding

The promise ledger is healthy: `mesh-promises --balance` reports zero standing
`liabilities:promises`, and `mesh-promises --check` passes parity, replay agreement,
negative-liability, and roster checks.

The misleading `RUNNING` row is in the coordination summary, not the promise ledger.
At 15:32:14Z the live task audit reported:

- `genome/tg-scripts-layout-audit-20260907/inventory-and-map`: `RUNNING`, lease through
  15:46:14Z; genome's pane was `WORKING`.
- `witness/witness-ledger-coverage-audit/ledger-coverage-audit`: `EXPIRED`, lease ended
  15:31:45Z; witness's pane was `IDLE`.

The dashboard was showing a summary timestamped 15:30:19Z (file mtime 15:30:23Z),
before the witness lease expired. `mesh-witness-promises` is wired at `*/5` in
`~/.mesh/reflexes.cron`, and `mesh-witness` renders the last summary file without
re-evaluating leases. Therefore a valid `RUNNING` observation can remain visible for
up to the refresh interval after it becomes `EXPIRED`; the displayed `findings=0`
also remained stale until the next reflex run.

## Verification

At 15:33:14Z, running `scripts/mesh-witness-promises` refreshed the summary and produced
`chain_steps=30 findings=1 status=FAIL`, naming the expired witness task. A fresh
`mesh-task audit` agreed. The promise ledger remained `open=0`, and `mesh-promises
--check` remained PASS.

## Required follow-up

The coordination renderer should expose summary age and/or recompute lease state at
render time, so an expired lease cannot continue to display as `RUNNING` or hide a new
finding behind a stale `findings=0` footer.
