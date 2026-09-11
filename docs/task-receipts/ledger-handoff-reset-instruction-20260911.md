# Ledger handoff reset instruction — 2026-09-11

`mesh-task` handoff replies now include the explicit recipient reset sequence:

```text
/clear
tmux send-keys -t <pane> -l '/clear'
tmux send-keys -t <pane> C-m
```

`C-m` is tmux's carriage-return/submit key; it is the canonical form here. The ledger remains responsible for durable
task state and handoff delivery; the actual reset remains gated in `mesh-clear`, preserving the
handoff-before-clear order.

Verification:

- `tests/test-mesh-task-handoff-reset-instruction.sh` — PASS; it failed before the implementation.
- `tests/test-mesh-task-dispatch-receipt.sh` — PASS.
- `python3 -m py_compile scripts/mesh-task` — PASS.
- `git diff --check` — PASS.

Unrelated pre-existing worktree changes were preserved.
