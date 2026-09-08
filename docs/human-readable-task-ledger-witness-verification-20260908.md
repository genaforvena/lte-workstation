# Witness verification: human-readable task ledger

Date: 2026-09-08

Independent verification after deployment:

- `scripts/mesh-task` and `~/.local/bin/mesh-task` have SHA-256
  `d6b7f1dc1fc802e389cea033916e88434e5dedf9c6da9fc86395b8f40ae437ae`.
- `scripts/mesh_task_log.py` and `~/.local/bin/mesh_task_log.py` have SHA-256
  `8e96ddb142620a95e7c792e1653cf8a0724ecf15e93d33e1f695661561703947`.
- The installed executable must complete a clean lower-case chain lifecycle with
  only `[task-ledger]` records in its new log suffix; legacy records are not
  rewritten.
- Focused replay, source-coverage, restart-continuity, audit, and smoke checks
  are run independently before settlement.

Observed results:

- `python3 -m unittest tests/test-mesh-task-log.py tests/test-mesh-board-task-state.py
  tests/test-mesh-task-import.py tests/test-mesh-task-no-expiry.py` passed 27 tests.
- `bash tests/test-mesh-task-source-coverage.sh`,
  `bash tests/test-mesh-task-restart-continuity.sh`, and both source and installed
  `mesh-task --test` commands passed.
- A clean temporary chain named `witness-readable-runtime` was created, taken,
  and completed through `~/.local/bin/mesh-task`. Its five structured records
  were all `[task-ledger] v1 r=…`; none was `[task-state]` or `plist64:`.
- The real ledger's post-deployment witness `progress` transition for this task
  is `[task-ledger] v1 r=13`, confirming the installed runtime path is writing
  the readable form on the authoritative board.
