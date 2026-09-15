# ATProto-shaped board query try — 2026-09-09

The mesh already has the small implementation: `scripts/mesh-board query` delegates to the
read-only `scripts/mesh-board-query` parser over the append-only tmux board text. This turn adds a
regression witness for that named reader in `tests/test-mesh-board-query-reader.sh`.

The fixture verified a distributed envelope query (`marker=task AND node=alpha`), JSON output for
metadata (`owner=genome`), and an honest non-zero result for no matches. The test uses a temporary
board and does not write the live board, create an index, or change the deployed copy.

Verification:

* `bash tests/test-mesh-board-query-reader.sh` — PASS
* `python3 scripts/mesh-board-query --test` — PASS
* `python3 -m py_compile scripts/mesh-board scripts/mesh-board-query` — PASS
* `git diff --check` — PASS

The new test and this study artifact are intentionally uncommitted for the steward to land.
