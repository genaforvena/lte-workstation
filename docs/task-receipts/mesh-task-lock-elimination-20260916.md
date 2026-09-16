# Mesh task lock elimination — 2026-09-16

## Root cause

`scripts/mesh-task` held `$MESH_TASK_DIR/.mesh-task.lock` across every mutable
operation, including an external board receipt. A delayed `mesh-chat` call for
one chain therefore blocked creation, claim, progress, and completion for every
other chain. The append-only task ledger already owns the authoritative
serialization point: `mesh_task_log.append()` holds the chat-log append lock,
replays the current revision, and rejects an unexpected successor revision.

## Change

The global coordinator lock is removed. Each mutation now holds deterministic,
hashed locks only for its task chain and acting owner. The chain lock preserves
receipt-before-state ordering against stale re-dispatch of that chain. The owner
lock preserves the cross-chain active-capacity check. The log append remains the
only ledger-wide critical section and validates the revision before fsync.

This makes a slow receipt unable to stop unrelated work while retaining both
same-chain exclusion and owner-capacity exclusion.

## Verification

- `tests/test-mesh-task-lock-scope.sh` held `one/work` at its board receipt and
  created `two/work` under another owner before releasing it: PASS.
- `tests/test-mesh-task-reschedule.sh` preserved the stale-re-dispatch guard: PASS.
- `tests/test-mesh-task-ledger-sync.sh`, `tests/test-mesh-task-restart-continuity.sh`,
  `tests/test-mesh-task-optional-owner.py`, `tests/test-mesh-task-log.py`, and
  `tests/test-mesh-task-unowned-pickup.py`: PASS.
- `python3 scripts/mesh-task --test`, `python3 -m py_compile scripts/mesh-task
  scripts/mesh_task_log.py`, and `git diff --check`: PASS.
- Deployed `/home/mesh-home/.local/bin/mesh-task` is byte-identical to source
  (`39ea7074de400a9e05d83164b7287affc9074891c3ba1d5719e4def015c52772`)
  and its `--test` passed.

The two one-slot capacity fixtures now set `MESH_TASK_MAX_ACTIVE=1` explicitly;
production's default remains three.
