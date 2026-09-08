# Human-readable task-ledger independent verification

Date: 2026-09-08

Independent verification of the deployed readable task ledger was run from the repository root.

Evidence:

- `python3 -m unittest tests/test-mesh-task-log.py tests/test-mesh-board-task-state.py tests/test-mesh-task-import.py tests/test-mesh-task-no-expiry.py` — 27 tests passed.
- `bash tests/test-mesh-task-source-coverage.sh` — PASS.
- `bash tests/test-mesh-task-ledger-sync.sh` — PASS.
- `bash tests/test-mesh-task-restart-continuity.sh` — PASS.
- `bash tests/test-mesh-task-audit-complete.sh` — PASS.
- `bash tests/test-mesh-task-dispatch-receipt.sh` — PASS.
- `python3 scripts/mesh-task --test` — PASS.
- An isolated temporary mesh completed create → take → done for a future task. Its five-line
  `chat.log` contained readable `[task-ledger]` records only: no `[task-state]` or `plist64:`
  markers. The derived chain cache replayed `status=complete`.

The checks used an isolated `MESH_DIR`/`MESH_TASK_DIR`; no production task chain or board state was
used as a fixture. No code changes were required by this verification.
