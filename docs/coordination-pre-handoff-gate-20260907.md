# Pre-handoff task gate — 2026-09-07

The Codex lifecycle now checks an active per-window task context before it can clear a pane.
The context must contain one canonical task ID, the exact current window owner, and a non-empty
`next_action`. The board log must contain that task ID, owner, and the same explicit next action.

If the context is absent or marked done, behavior is unchanged. If an active context is malformed
or lacks the matching board receipt, the completion receipt remains `pending`, records
`pre-handoff gate`, and `mesh-clear` is not called. This keeps the obligation visible until the
owner publishes a usable board update.

Changed:

- `scripts/mesh-codex-lifecycle`
- deployed `~/.local/bin/mesh-codex-lifecycle` (byte-identical)

Verification:

- `python3 scripts/mesh-codex-lifecycle --test` — PASS
- `~/.local/bin/mesh-codex-lifecycle --test` — PASS
- `python3 -m py_compile scripts/mesh-codex-lifecycle` — PASS
- `git diff --check` — PASS
- `bash tests/test-mesh-witness-lifecycle.sh` — PASS
- `bash tests/test-mesh-witness-promises.sh` — PASS
