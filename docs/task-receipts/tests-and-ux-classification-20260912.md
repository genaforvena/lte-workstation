# Tests and UXN classification migration receipt

Task: `tg-scripts-layout-migration-20260912/tests-and-ux-classification`  
Owner: `genome`  
Completed: 2026-09-12 UTC

## Change

Moved UXN assembly sources, emulator/compiler source trees, ROMs, symbol tables, and local generated
`bin/` outputs from `scripts/uxn/` to `scripts/ux/`. Moved the UXN test drivers and their fixture
data to `scripts/tests/uxn/`. Existing `scripts/uxn/` paths remain as compatibility symlinks, so
runtime wrappers, external callers, and old test invocations still resolve.

Added `scripts/ux/uxn-build-manifest.tsv` and `scripts/ux/check-build-manifest`. The manifest records
25 ROMs, 24 symbol tables, and five host/target binaries with their source inputs, build recipes,
and SHA-256 for the architecture-independent ROM and symbol outputs. The complete 54-output
inventory was created and validated under `scripts/uxn/` before moving generated output. During
final validation, binary rows were changed to leave host content unpinned because host and
cross-compiler builds vary by platform; the validator requires that policy and checks the declared
inputs/recipes. The finalized manifest was then validated again at its `scripts/ux/` location.

The source manifest now classifies UXN test drivers and fixture files as `domain=tests`,
`kind=fixture`, `deploy_policy=none`, and UXN source/assets as `domain=ux`, `deploy_policy=none`.
`mesh-manifest --check` reports 1,217 complete rows with no duplicate installed basenames.

Build-manifest SHA-256: `c294612ed37716843f8bf885000c6fdfbc552077d19297c1a7078579f22393cc`.

## Verification

- Before output relocation: UXN build manifest covered 54 outputs; every present ROM, SYM, and
  binary hash matched the initial inventory.
- After relocation: `scripts/ux/check-build-manifest` passes with 54 declared outputs, 54 present,
  and 49 hash-verified; the five compiler outputs are platform-specific and intentionally unpinned.
- `tests/test-mesh-uxn-layout.sh` passes when invoked from a temporary directory outside the repo.
  It also changes a copied host binary and confirms the validator does not reject a legitimate
  platform-specific binary rebuild.
- From an external working directory, `scripts/tests/uxn/test-lease-gate`,
  `scripts/tests/uxn/test-band-gate`, and `scripts/tests/uxn/test-rom-binary-contract` pass.
- `scripts/mesh-manifest --check`, `scripts/mesh-sync-tools --test`, `scripts/mesh-autowire --test`,
  and `scripts/mesh-land --test` pass.
- A fresh `scripts/mesh-manifest --parity` audit confirms every `scripts/tests/uxn/` and
  `scripts/ux/` row has no installed basename and `deployed_status=na`.
- Python syntax checks for `scripts/mesh-manifest` and `scripts/ux/check-build-manifest`, plus
  `bash -n` for the contract test and moved lease/band/ROM-contract drivers, pass.

## Unresolved test failures

`tests/test-mesh-manifest-consumers.sh` reaches the manifest checks and sync test successfully, then
fails in its existing `mesh-doctor --test` leg: `smoke-test: FAIL (a twice-red tool did not reach
fail: got 'na')`. `scripts/mesh-doctor` was not changed by this task.

The moved `scripts/tests/uxn/test-threshold-ledger` also reaches its load-gate checks but has four
output assertions that reject the extra `eff_enabled`/effectivity line currently emitted by
`mesh-load-gate`. Neither `scripts/mesh-load-gate` nor its consumers were changed by this task.

The task's requested layout, compatibility, test-from-outside-root, build-manifest, and deployment
exclusion checks pass. Landing remains with the mesh-land steward; this receipt and the focused source
changes are ready for that review.
