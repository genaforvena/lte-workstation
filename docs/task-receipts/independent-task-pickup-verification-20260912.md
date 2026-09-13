# Independent pickup verification — 2026-09-12

The isolated fixture passed after the final test change:

- `python3 tests/test-mesh-task-independent-pickup.py` — passed. It verifies the exact owner can mark a later step independent only while the chain head is blocked; default serial pickup and explicit `waiting_for` remain refused; the owner queue and dispatch check agree; audit reports `READY_INDEPENDENT`; status and the routed task retain the reason; `[taking]`, progress, block, resume, and artifact-backed completion work; the blocked head stays visible; and normal completion skips the already-done independent step.
- `python3 scripts/mesh-task --test` — passed with the same behavior embedded in the coordinator smoke test.

The fake board recorded exactly one routed `[task]` row for the independent step and one `[taking]` transition. The live canonical audit records the implementation step DONE and verification step RUNNING under `task-independent-pickup-20260912`.

This verifies the source code path and task-state contract. The installed command has not changed: `mesh-land` currently refuses candidate enumeration on the already-staged, unclassified symlink `scripts/ux/chibicc/tests`. That separate deployment gate remains with genome; no installed-copy success is claimed here.
