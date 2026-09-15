# Haunt resolver: A10 coordinator hold is still authoritative

Date: 2026-09-12 (UTC)  
Owner: haunt  
Task: `unblock/haunt/400503a105e567f3/resolve`

## Fresh evidence

- `mesh-task check dispatch unblock/haunt/400503a105e567f3/resolve haunt` exited 0; haunt
  claimed this exact row with the owner-authored `mesh-task take` command.
- `mesh-task status tinyfleet-applications-20260908` still reports `[blocked] (21/22)`;
  `simulator-actions` is blocked and `verify-simulator-actions` remains open for VPN.
- `mesh-task check pending tinyfleet-applications-20260908/simulator-actions haunt` exited 2.
  The step is not eligible while its chain is blocked.
- The independent A09 receipt
  `/home/mesh-home/tiny-fleet/docs/task-receipts/A09-V-reconciliation-20260909.md` has SHA-256
  `fe05f8f3796700714005557baaae90f8f51ece685c6e1a33d993c26872b8b8fa`. It says A09 remains
  `INCONCLUSIVE` and explicitly does not release A10. The earlier Haunt resolver receipt
  `docs/task-receipts/unblock-haunt-ce12ed76efbdd2ad-resolve-20260912.md` records the owner-authored
  `recover ... hold` action and the same release boundary.

## Disposition

The receipt typo is reconciled, but coordinator authorization to release A10 is absent. Releasing or
reactivating `simulator-actions` would contradict the independent receipt. No in-scope code or
prerequisite can supply that authority, so the blocker is an external event. This resolver is closed
as artifact-backed terminal diagnosis; the Tiny Fleet chain remains blocked and must not be resumed
until an authorized coordinator event changes the ledger. No Tiny Fleet source or experiment files
were modified.
