# Human-readable task ledger verification

Date: 2026-09-08

The writer now emits `[task-ledger] v1 r=<revision>` snapshots. `scripts/mesh_task_log.py` still
decodes historical `[task-state]` JSON and `plist64:` records, and `mesh-promises` plus the health
warning cursor recognize both markers.

Evidence:

- Before implementation, `python3 -m unittest tests/test-mesh-task-log.py` failed on the required
  readable-marker assertion because the writer emitted `[task-state] plist64:`.
- `python3 -m unittest tests/test-mesh-task-log.py tests/test-mesh-board-task-state.py
  tests/test-mesh-task-import.py tests/test-mesh-task-no-expiry.py` — 25 tests passed.
- `bash tests/test-mesh-task-source-coverage.sh`, `bash tests/test-mesh-task-ledger-sync.sh`,
  `bash tests/test-mesh-task-restart-continuity.sh`, `bash tests/test-mesh-task-audit-complete.sh`,
  and `bash tests/test-mesh-task-dispatch-receipt.sh` — all passed.
- `python3 scripts/mesh-task --test` — passed.
- A temporary canary chain was created, taken, and completed after recording a 967-byte baseline
  offset. Its appended suffix contained revisions `r=3`, `r=4`, and `r=5` as readable
  `[task-ledger]` lines; `mesh-task replay --json` reconstructed `status=complete`. The suffix had
  no `[task-state]` or `plist64:` bytes. The canary artifact was `/tmp/tmp.VAYVyvB4tv/artifact` and
  its recorded SHA-256 was `5b3513f580c8397212ff2c8f459c199efc0c90e4354a5f3533adf0a3fff3a530`.

The unrelated pre-existing `tests/test-mesh-dispatch-hledger-gate.sh` was also attempted; its
synthetic `mesh-promises` feed gate failed before dispatch, so it remains an environment/test-harness
obligation rather than ledger evidence.
