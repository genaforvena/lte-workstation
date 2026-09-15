# separate-blocked-from-queued — verification receipt

Implemented the blocked-ledger visibility repair.

- `scripts/mesh-task-journal` now preserves `BLOCKED` rows and emits explicit
  `blocker_type=` and `retry=` fields instead of relabelling them `QUEUED`.
- `scripts/mesh-dash` counts and renders `BLOCKED` rows as unfinished work;
  `HELD_REJECTED` remains visible as well.
- `mesh-task queue --dispatch` continues to select only current OPEN steps;
  blocked work is absent from the dispatch task-id field.

Verification:

- `tests/test-mesh-witness-task-only-materializer.sh` — PASS
- `tests/test-witness-open-pane.py` — PASS
- `tests/test-mesh-witness-task-queue-fit.sh` — PASS
- `tests/test-mesh-task-no-expiry.py` — 12 tests PASS
- deployed `mesh-task-journal --test` — PASS
- deployed `mesh-task --test` — PASS
- source/deployed byte parity — PASS for `mesh-task-journal`, `mesh-dash`, and `mesh-task`
