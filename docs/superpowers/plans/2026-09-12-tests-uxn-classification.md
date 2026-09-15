# Tests and UXN Classification Implementation Plan

> **For agentic workers:** Execute inline with test-first checkpoints; preserve the current working tree and do not land from a worktree.

**Goal:** Move only manifest-classified UXN tests/fixtures and UXN source/build assets into their target lanes, while preserving old UXN paths and excluding non-runtime material from production installs.

**Architecture:** Keep live UXN host tools and docs under `scripts/uxn/`. Move test drivers and fixture trees to `scripts/tests/uxn/`; move UXN sources, tracked ROM/SYM outputs, and generated `bin/` outputs to `scripts/ux/`. Keep compatibility symlinks under `scripts/uxn/` for all moved paths so existing callers continue to resolve. Add a checked UXN build manifest that records every generated output and its recipe before moving any generated output.

**Tech Stack:** Python 3 standard library, shell test drivers, `scripts/mesh-manifest` TSV inventory.

## Global Constraints

- Preserve all existing `scripts/uxn/...` command and asset paths through compatibility links.
- Only files explicitly classified as UXN tests/fixtures or UXN sources/assets may move.
- Every ROM, SYM, and UXN `bin/` output must be listed and validated before it moves.
- Tests must run with the working directory outside the repository root.
- Production deployment must not install any UXN fixture, test driver, source, ROM, SYM, or build binary as a mesh command.
- Preserve unrelated dirty and untracked work.

---

### Task 1: Add a failing UXN migration contract test

**Files:** Create `tests/test-mesh-uxn-layout.sh`.

- [ ] Assert the build manifest validator accounts for every tracked `.rom` and `.sym` and every present `scripts/uxn/bin/*` output.
- [ ] Assert legacy runtime asset paths still resolve after migration.
- [ ] Assert all test drivers and fixture directories have test/fixture classifications and no deploy basename.
- [ ] Run this test from a temporary directory; verify it fails because the UXN build manifest/target paths are absent.

### Task 2: Create and validate the UXN build manifest

**Files:** Create `scripts/uxn/uxn-build-manifest.tsv`, `scripts/uxn/check-build-manifest`, and extend `tests/test-mesh-uxn-layout.sh`.

- [ ] Record each ROM/SYM and generated emulator/compiler binary with source inputs, build recipe, and output role.
- [ ] Reject missing inputs, duplicate outputs, unlisted ROM/SYM files, and undeclared present `bin/` files.
- [ ] Validate the manifest and retain the passing output before moving generated outputs.

### Task 3: Classify and move UXN test material

**Files:** Modify `scripts/mesh-manifest`; move only classified UXN test drivers/fixtures to `scripts/tests/uxn/`; retain old paths as compatibility links.

- [ ] Make `test-*` entries and named UXN fixture assets/directories explicit in manifest classification.
- [ ] Verify the contract test fails before moves and passes after moves.
- [ ] Run all moved UXN test drivers from an external temporary working directory.

### Task 4: Relocate UXN sources and generated assets

**Files:** Move classified UXN source trees and manifest-listed ROM/SYM/bin output into `scripts/ux/`; preserve `scripts/uxn` compatibility links; update `scripts/mesh-manifest` domain mapping.

- [ ] Move only source/assets covered by the inventory and build manifest.
- [ ] Preserve old UXN runtime paths and executable-tool basenames.
- [ ] Validate `scripts/ux/check-build-manifest` and `scripts/mesh-manifest --check`.

### Task 5: Verify deployment exclusion and caller compatibility

**Files:** Update `tests/test-mesh-uxn-layout.sh` and add `docs/task-receipts/tests-and-uxn-classification-20260912.md`.

- [ ] Run the UXN layout test from outside the repository root.
- [ ] Run focused UXN test drivers and `mesh-sync-tools --test`.
- [ ] Inspect real manifest parity and assert test/fixture/source/asset paths have no production installed basename.
- [ ] Record current unresolved consumers or blockers honestly; do not treat a successful self-test as proof of deployment exclusion.
