# Independent pickup observability — 2026-09-12

The isolated fixture and the live canonical task ledger agree on the transition model.

- `rtk proxy python3 tests/test-mesh-task-independent-pickup.py` — passed. Its canonical-format `chat.log` fixture records one routed `[task]` row and one `[taking]` transition for the explicitly independent step, then exposes `READY_INDEPENDENT`, later `BLOCKED`/`DONE`, the still-blocked predecessor, and final ordered advancement in `audit` and `status`. It also verifies the default serial and explicit `waiting_for` gates.
- Live `rtk mesh-task audit` lists implementation and behavior verification as `DONE` with artifact paths and this observability step as `RUNNING`. `rtk mesh-task status task-independent-pickup-20260912` reports steps 1 and 2 done and step 3 active; `~/.mesh/tasks.journal` has the matching `DONE`, `DONE`, `RUNNING` rows.
- `rtk mesh-task check resume task-independent-pickup-20260912/verify-task-observability witness` exited 0 for the exact active owner. `rtk mesh-task queue --dispatch --owner witness` returned no rows because witness already owns the active step.
- The live `~/.mesh/chat.log` has exactly one witness-routed `[task]` row and one `[taking]` transition for each of the three chain steps (lines 58143/58145, 58213/58216, and 58226/58233). Separate genome-owned autoland requests are not duplicate witness task rows.

No ledger/journal disagreement or duplicate chain routing was found. The independent-step transition detail is verified in the isolated canonical-format fixture; the live chain confirms that the implementation, behavior verification, and observability work are themselves visible and owned through the ledger. Installed deployment remains pending genome landing as recorded in the implementation receipt.
