# Scoped mesh-land test-artifact support — 2026-09-11

`mesh-land` now accepts `MESH_LAND_EXTRA_PATHS` only as a space-delimited list of exact regular,
non-symlink files beneath `tests/`. Globs, empty entries, directories, symlinks, missing paths,
absolute/parent paths, and every outside-`tests/` path are rejected. This supports landing a named
focused test without globally enumerating the worktree's unrelated `tests/` files.

Explicit test candidates are commit-only artifacts: they are included in the scoped git commit but
are skipped by the runtime deploy loop and do not become `~/.local/bin` tools or autowire inputs.

Verification:

- `timeout 180 bash scripts/mesh-land --test` — PASS; full self-test covers exact admission,
  glob/outside/missing/directory/absolute/parent/symlink refusal, and no runtime test copy
- `bash -n scripts/mesh-land` — PASS
- `MESH_LAND_EXTRA_PATHS=tests/test-mesh-pane-consume-task-aware-idle-gate.sh MESH_LAND_PATHS=tests/test-mesh-pane-consume-task-aware-idle-gate.sh mesh-land` — PASS; exact test surfaced as the sole candidate
- `mesh-land --check` — PASS

This support artifact is separate from the idle-turn correction and must land first.
