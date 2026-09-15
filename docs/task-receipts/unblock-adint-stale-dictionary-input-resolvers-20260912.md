# Stale dictionary-input resolver rows — 2026-09-12

This receipt applies to these adint-owned resolver rows:

- `unblock/bash/22d1f3966cf55238/resolve` → `unblock/adint/747f3093803a4ce6/resolve`
- `unblock/bash/655f0e0e5d841d69/resolve` → `unblock/adint/04121d2ccec59b9b/resolve`

## Finding

Both dispatch descriptions still ask for the five dictionary input fields. Those inputs have since
been frozen in `/home/mesh-home/tiny-fleet/runs/operator-selected-dictionary-v1/input-manifest.json`
(SHA-256 `9081dd78b28ed94b501016698cd6d5347095a5ea079730bf888123c3ec2e1e08`) and its 152-row
corpus (SHA-256 `81a41340c0c01555a536e9aa30b3b2b72b1dd9ae48908014fd0f58192515dcd3`). The operator's
repository-selection authorization and field-by-field freeze are documented in
`/home/mesh-home/tiny-fleet/docs/task-receipts/adint-operator-authorized-dictionary-input-20260912.md`.

The first referenced Haunt resolver, `unblock/haunt/62c0662129fa8ee9/resolve`, is complete under
the A08-only scope amendment. Its resume check exits 2 because the row is already complete. The
second task's parent, `haunt-install-unblock-20260907`, is also complete under that same amendment.
These rows need no further operator input.

The separate broader BbyWVY dictionary question remains blocked under
`unblock/haunt/fd5d75268b44e1cc/resolve` as `experiment-contract`. Frozen synthetic A08 inputs do
not prove BbyWVY dictionary behavior, and `scripts/bbywvy_test.py` is a runtime smoke without a
dictionary arm. The remaining action is Haunt's owner-authored scope amendment to A08-only with an
`INCONCLUSIVE` limit, or a compatible measured dictionary arm. Do not re-request the already-frozen
inputs or use the runtime smoke as dictionary evidence.

No Haunt-owned task, dictionary input, or study result was changed.
