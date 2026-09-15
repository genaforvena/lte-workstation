# Haunt resolver: Tiny Fleet task event still absent

Date: 2026-09-12 (UTC)  
Owner: haunt  
Task: `unblock/haunt/a9457737cb7b87e1/resolve`

## Live ledger audit

- `mesh-task queue --dispatch --owner haunt` returned this resolver row; it was claimed by
  `haunt@mesh-home` at 20:56:34Z. The exact dispatch check now exits 2 because the row is already
  active, not because it is stale. No second take was attempted.
- `mesh-task status tinyfleet-applications-20260908` still reports `[blocked] (21/22)`. The
  `simulator-actions` step is blocked on owner-authorized recovery evidence; the next verification
  step belongs to VPN.
- `mesh-task check pending tinyfleet-applications-20260908/simulator-actions haunt` exits 2.
  Before this resolver was claimed, the owner-scoped dispatch queue returned only the resolver; no
  eligible Tiny Fleet task was available to satisfy the parent task's required event.
- The independent A09 receipt at
  `/home/mesh-home/tiny-fleet/docs/task-receipts/A09-V-reconciliation-20260909.md` currently hashes
  to `fe05f8f3796700714005557baaae90f8f51ece685c6e1a33d993c26872b8b8fa`. It says the corrected
  receipt clears only the typo; the application verdict remains `INCONCLUSIVE` and A10 is not
  released.

## Disposition

The smallest safe prerequisite is a coordinator-authorized A10 release that creates a new or
recovered exact-owner Tiny Fleet task in a claimable chain. No code or receipt correction can
provide that authority. The live ledger still refuses the only apparent implementation step, so
the parent `tinyfleet-live-proof` remains blocked and is not resumed. Retry after the required
task-ledger event, then rerun the owner-scoped queue and exact-row check before taking anything.
No Tiny Fleet source or experiment files were changed.
