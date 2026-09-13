# Cron admission resolution receipt — 2026-09-13

## Change

`scripts/mesh-autopoiesis` now invokes the co-installed `scripts/mesh-task` by its resolved sibling
path when `MESH_TASK_BIN` is unset. An explicit `MESH_TASK_BIN` remains authoritative. If the chosen
command cannot start, the adapter prints a concise error and exits 127 instead of exposing a Python
traceback.

## Evidence

- Before the fix, `bash tests/test-autopoiesis-admission-cron-path.sh` failed under `PATH=/usr/bin:/bin`
  with `FileNotFoundError: 'mesh-task'` while the observer admitted a complete fixture.
- After the fix, the same cron-like minimal-PATH fixture ran the observer through the real
  `mesh-task create` path, wrote the task ledger and generated chain, and verified the source,
  step ID, and successful dispatch.
- The fixture also confirmed that an incomplete envelope is refused before invoking task creation,
  and that an unavailable explicit `MESH_TASK_BIN` returns 127 with a controlled diagnostic.
- `tests/test-autopoiesis-observer.sh` and `tests/test-autopoietic-producers.sh` passed.

The historical 2026-09-13 15:00–17:00Z source window was not replayed against the live mesh; the
test uses an isolated equivalent fixture to avoid changing live task history.
