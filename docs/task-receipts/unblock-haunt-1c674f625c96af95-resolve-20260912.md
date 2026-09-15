# Haunt resolver: A10 remains externally held

Date: 2026-09-12 (UTC)  
Owner: haunt  
Task: `unblock/haunt/1c674f625c96af95/resolve`

## Fresh evidence

- The exact-owner resolver was eligible (`mesh-task check dispatch ... haunt` exited 0) and
  was claimed by `MESH_TASK_ACTOR=haunt mesh-task take ... resolve`.
- `mesh-task status tinyfleet-applications-20260908` reports the chain `[blocked] (21/22)`;
  `simulator-actions` remains blocked behind the rejected `verify-transliteration` predecessor,
  and `verify-simulator-actions` remains open for VPN.
- `mesh-task check pending tinyfleet-applications-20260908/simulator-actions haunt` exited 2.
- The independent A09 reconciliation receipt
  `/home/mesh-home/tiny-fleet/docs/task-receipts/A09-V-reconciliation-20260909.md` still has
  SHA-256 `fe05f8f3796700714005557baaae90f8f51ece685c6e1a33d993c26872b8b8fa`. It confirms the
  receipt correction but says the application verdict remains `INCONCLUSIVE` and does not release
  A10.
- Earlier exact-owner Haunt receipts record the successful `recover ... hold` action and the same
  coordinator boundary: `docs/task-receipts/unblock-haunt-ce12ed76efbdd2ad-resolve-20260912.md`
  and `docs/task-receipts/unblock-haunt-400503a105e567f3-resolve-20260912.md`.

## Disposition

The remaining prerequisite is explicit coordinator authorization to release A10. No code change,
receipt correction, or owner-side recovery can supply that authority; reactivating
`simulator-actions` would contradict the independent A09 receipt. This resolver is closed as an
artifact-backed terminal diagnosis. The Tiny Fleet implementation chain remains blocked until an
authorized coordinator event changes the ledger. No Tiny Fleet source or experiment files were
modified.
