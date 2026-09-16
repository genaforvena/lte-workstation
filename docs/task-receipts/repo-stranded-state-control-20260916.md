# Repository stranded-state control — 2026-09-16

Result: fixed and landed in commit `978941a3`.

Measured before landing: `main` matched `origin/main`, but the worktree contained 381 dirty
entries overall and 37 under `scripts/` (30 tracked dirty, 7 untracked). `mesh-land --check`
reported a 234-item bulk landing backlog. A concurrent manual `mesh-land --apply` writer held the
landing lock while another landing path had already deployed source matching the dirty worktree;
manual `--apply` previously did not acquire that lock.

Changes:

- `mesh-land --check` now writes a deterministic HEAD+porcelain dirty report and creates one
  idempotent exact-owner `priority:incident` task per changed signature.
- `mesh-land --apply` and `--autoland` now share the same non-blocking single-writer lock.
- Added regressions for occupied `--apply` locking and dirty-task/report idempotency.

Verification: `tests/test-mesh-land-dirty-task.sh` PASS; `tests/test-mesh-land-apply-lock.sh` PASS;
`tests/test-mesh-land-check-budget.sh` PASS; landing pushed successfully and `HEAD == origin/main`.
Remaining dirty paths are unrelated work preserved for their own gated landing units.
