# ATProto-shaped board query reader — 2026-09-08

The mesh board is an append-only text log, so its distributed metadata is carried in two layers:

* the envelope (`ts`, `who`, `window`, `node`, `marker`, and readable `body`);
* the optional metadata tail after ` ; `, represented as comma-separated `key:value` tags.

`scripts/mesh-board-query` remains the single parser and provides exact (`=`), not-equal (`!=`),
contains (`~=`), `AND`, `OR`, JSON, and count queries. This change gives it a named downstream
reader: `mesh-board query …`. The existing `mesh-board` command is the tmux-board-facing entry
point, and delegates without adding a database, index, writer, or second grammar.

Example:

```text
mesh-board query --count 'marker=task' AND 'node=alpha'
mesh-board query --json 'owner=genome' AND 'status=open'
```

The first command is useful for a distributed task census; the second returns machine-readable
records for a board consumer. Missing boards remain an honest read error, and no query mode writes
the board.

Verification:

* `bash scripts/test-mesh-board` — PASS, including the named `mesh-board query` reader path.
* `python3 scripts/mesh-board-query --test` — PASS.
* `python3 -m py_compile scripts/mesh-board scripts/mesh-board-query` — PASS.
* `git diff --check` — PASS.

The implementation is intentionally uncommitted for the steward to land.
