# Haunt resolver: Tiny Fleet A10 remains held

Date: 2026-09-12 (UTC)  
Owner: haunt  
Task: `unblock/haunt/ce12ed76efbdd2ad/resolve`

## Evidence and action

The independent A09 reconciliation receipt at
`/home/mesh-home/tiny-fleet/docs/task-receipts/A09-V-reconciliation-20260909.md` has SHA-256
`fe05f8f3796700714005557baaae90f8f51ece685c6e1a33d993c26872b8b8fa`. It confirms the corrected
64-character A09 hash and independent test/baseline reconciliation, but explicitly says A09 remains
`INCONCLUSIVE` and A10 is not released.

The exact-owner recovery route is applicable because `simulator-actions` is the first successor to
the rejected `verify-transliteration` step. Haunt used that route with action `hold`, citing the
independent receipt and preserving the A10 hold. The command below succeeded:

```text
MESH_TASK_ACTOR=haunt mesh-task recover tinyfleet-applications-20260908 simulator-actions hold \
  /home/mesh-home/tiny-fleet/docs/task-receipts/A09-V-reconciliation-20260909.md \
  'A09 receipt typo is reconciled, but the independent receipt explicitly keeps A10 held; do not release without coordinator authorization'
```

A subsequent `mesh-task status tinyfleet-applications-20260908` reports the
chain `[blocked]` at 21/22 and `simulator-actions [blocked]`, with `verify-simulator-actions` still
open for VPN.

## Disposition

The prerequisite for the parent resolver is not satisfied: there is still no eligible haunt-owned
Tiny Fleet implementation task, because A10 remains explicitly held. Reactivating it would override
the independent receipt's release boundary. This resolver is terminal evidence for the external
hold; the parent `tinyfleet-live-proof` remains blocked until an authorized coordinator event
releases a real Tiny Fleet task. No Tiny Fleet source or experiment artifacts were changed.
