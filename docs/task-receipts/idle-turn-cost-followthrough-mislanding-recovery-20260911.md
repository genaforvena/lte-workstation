# Idle-turn follow-through mislanding recovery — 2026-09-11

## Recovery artifact

The scope-violating commit `8c0481eb4250946308835ab5e11e3e9cfed4fee5` was normally reverted by
`6d87ae8018ef522fb15e1ffadf868034b213f16d` (`Revert "mesh-land: land idle-turn correction
regression tests"`). The reverted path was `tests/test-mesh-task-no-expiry.py`; its exact resolver-test
content delta remains restored as uncommitted mode `100644` work for its real owner. The restored
file's exact content blob is `da3708dcf59110854cdaf1ad451b31895dde1631`, its filesystem mode is
`644`, and `git status --short -- tests/test-mesh-task-no-expiry.py` reports `M` (preserved dirty
status). This equals `git rev-parse 8c0481e:tests/test-mesh-task-no-expiry.py` exactly.

The actual pane-consume correction regression is the separately landed
`tests/test-mesh-pane-consume-task-aware-idle-gate.sh` from `025ef766c7fd80fa17d1510502bc5470a29a215e`.
The correction source and receipts remain intact in the canonical history:

- `scripts/mesh-pane-consume` — correction source, deployed SHA
  `44a44dd490c31a44dda3bed0ca681d61be638f26a222b063a33778647dd20c3a`;
- `docs/task-receipts/idle-turn-cost-followthrough-correction-implementation-20260911.md`;
- `docs/task-receipts/idle-turn-cost-followthrough-correction-prelanding-review-20260911.md`.

## Remote convergence

`bash scripts/mesh-land --push-heal` pushed the stranded normal-revert commit without rewriting
history or force-pushing. Verification after the push:

- local `HEAD`: `6d87ae8018ef522fb15e1ffadf868034b213f16d`;
- cached `origin/main`: `6d87ae8018ef522fb15e1ffadf868034b213f16d`;
- server `refs/heads/main`: `6d87ae8018ef522fb15e1ffadf868034b213f16d`;
- `git diff --name-status origin/main..HEAD`: empty.

The correction task remains open pending independent witness verification. No correction `[done]`
or task close is claimed by this recovery receipt.
