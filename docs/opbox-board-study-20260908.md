# Opbox-shaped board synchronization study — 2026-09-08

## Decision

Implemented a small, internal, on-demand adapter in `scripts/mesh-opbox`. The real Opbox design
turns saved text changes into durable CRDT operations and materializes the merged document back to
disk ([opbox.dev](https://www.opbox.dev/)). This repository does not have the `ob` daemon installed,
so the experiment keeps only the part that fits our board safely: each existing append-only board
line is an immutable operation, and merge is a grow-only set union.

This is deliberately not a second live board, daemon, network transport, package dependency, or
cron reflex. The existing `mesh-chat-sync` remains the board's production synchronization path.

## Interface

```text
mesh-opbox export BOARD OPS.jsonl
mesh-opbox merge MERGED.jsonl OPS.jsonl [...]
mesh-opbox materialize OPS.jsonl BOARD
mesh-opbox sync OUTPUT BOARD [...]
```

Operation files are canonical JSONL. The operation id is SHA-256 of the UTF-8 line, matching the
board's existing `sort -u` identity. Merge is idempotent, commutative, and associative; materialize
uses UTF-8 byte order so its result is stable across replicas. Writes use an fsync plus atomic
replace, leaving a real disk artifact at each stage.

## Boundary and limitation

This is an Opbox-shaped board experiment, not a general sequence CRDT: it preserves concurrent
appends, not arbitrary in-place edits or deletions. That limitation is intentional because the
board's current contract is append-only. Supporting editor-grade text edits would require a real
sequence CRDT implementation (or the Opbox/`yrs` dependency), plus a new transport and trust
boundary; this study does not silently add those.

## Verification

- `scripts/mesh-opbox --test` — PASS: idempotence, commutativity, associativity, convergence.
- `tests/test-mesh-opbox.sh` — PASS: two divergent board files merge to one deterministic file,
  duplicate operations are removed, and repeated merge is byte-stable.
- `ob`/`opbox` availability — absent on this node; no external install was performed.
