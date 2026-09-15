# Manifest-backed autowire, landing, and vitality Implementation Plan

> **For agentic workers:** use inline execution with test-first checkpoints; each task ends with focused verification.

**Goal:** Make autowire, land, and vitality enumerate script candidates and coverage using the checked shared manifest while preserving compatibility paths.

**Architecture:** Keep `scripts/mesh-manifest` as the sole classifier. Consumers read its tab-separated rows through the existing manifest reader and fail loudly when the manifest cannot be validated or a row is unknown. Preserve each consumer's existing domain-specific eligibility gates after manifest classification.

**Tech Stack:** Bash, Python 3, TSV manifest, shell fixture tests.

## Global Constraints

- No source directories or live deployments move in this slice.
- Unknown rows, duplicate install basenames, and unreadable manifest output must fail loudly.
- Preserve existing top-level compatibility paths and domain-specific gates.
- Verify real cadence/reflex resolution and document an inverse rollback.

### Task 1: Lock loud manifest failure behavior

**Files:** Modify `scripts/lib/mesh-manifest-reader.sh`; extend `tests/test-mesh-manifest-consumers.sh`.

- [x] Add `mesh_manifest_install_sources <repo>` and `mesh_manifest_source_paths <repo>`; both must validate all rows before emitting output.
- [x] Extend the fixture to cover nested owners and all source classes.
- [x] Confirm unknown rows make install-source lookup and complete source coverage fail with empty stdout.
- [x] Run `bash tests/test-mesh-manifest-consumers.sh`; expected: reader fixtures pass, then sync-tools and doctor `--test` pass outside the checkout.

### Task 2: Wire the three consumers

**Files:** `scripts/mesh-autowire`, `scripts/mesh-land`, `scripts/mesh-vitality`, `tests/test-mesh-land-branch-override.sh`, and `tests/test-mesh-manifest-consumers.sh`.

**Interfaces:** consumers source `scripts/lib/mesh-manifest-reader.sh`; autowire uses install source pairs, land uses all classified source paths, and vitality passes installable paths to its Python census code.

- [x] Read manifest classifications through the shared reader, preserving each tool's existing filtering and compatibility-path rules.
- [x] Run `bash -n scripts/mesh-autowire scripts/mesh-land scripts/mesh-vitality scripts/lib/mesh-manifest-reader.sh`.
- [x] Run all three `--test` checks from `/tmp`; expected: each prints `smoke-test: ok`.
- [x] Verify `mesh-land` source/deployed/live cadence `3-59/15 * * * *`; isolated wrong-cadence input must print `DIVERGED`.

### Task 3: Record evidence and rollback

**Files:** `docs/task-receipts/manifest-autowire-land-vitality-20260912.md`.

- [x] Record test results, real cadence/reflex evidence, and the inverse change order for rollback.
- [x] Re-run `scripts/mesh-manifest --check`, focused consumer tests, and `git diff --check` before marking the task done.
