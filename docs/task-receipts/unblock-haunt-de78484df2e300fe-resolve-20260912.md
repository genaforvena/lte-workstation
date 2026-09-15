# Haunt resolver: A10 release remains coordinator-held

Date: 2026-09-12 (UTC)  
Owner: haunt  
Task: `unblock/haunt/de78484df2e300fe/resolve`

## Live evidence

- `mesh-task status tinyfleet-applications-20260908` exits 0 and reports
  `[blocked] (21/22)`: `simulator-actions` is blocked on `owner-authorized recovery evidence`;
  the next verification row remains open and belongs to `vpn`.
- `mesh-task check pending tinyfleet-applications-20260908/simulator-actions haunt` exits 2.
  The implementation step is not eligible for haunt to take or resume.
- The independent receipt
  `/home/mesh-home/tiny-fleet/docs/task-receipts/A09-V-reconciliation-20260909.md` has SHA-256
  `fe05f8f3796700714005557baaae90f8f51ece685c6e1a33d993c26872b8b8fa`. It reconciles only the
  A09 receipt hash typo, leaves the application verdict `INCONCLUSIVE`, and explicitly says it does
  not release A10.
- The current task-ledger blocker says not to release A10 without coordinator authorization. No
  authorization event is present in the live parent ledger; its status remains blocked.

## Disposition

The narrowest safe prerequisite is an authorized coordinator event that releases A10 and changes
the ledger. The receipt correction and any source-only edit cannot provide that authority. The
implementation task is therefore not resumed, and the parent remains blocked. This resolver is
closed with the live evidence above; retry only after an authorized ledger event, then run the
owner-scoped dispatch and exact-row check again. No Tiny Fleet source or experiment files were
modified; that checkout already had unrelated dirty changes.
