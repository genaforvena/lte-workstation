# FYI ledger embedded-row recovery — 2026-09-12

Task: `fyi-ledger-malformed-row-20260912/reconcile-source-row` (owner `genome`).

## Decision and source evidence

`mesh-fyi-ledger --witness` previously exited 2 because the FYI marker inside the valid
2026-08-30 `[strand]` row at `~/.mesh/chat.log:56940` was interpreted as though the outer row
were itself a malformed FYI message. A second archive row at line 56957 contains the same nested
record. The append-only source was not modified.

The parser now recovers a nested FYI only when it finds a complete timestamp, author, `::`, and
`[fyi]` record. Each containing physical row is listed as a coverage gap. Event identity hashes the
recovered record, so the two archived copies are one event rather than two observations. Marker-like
prose with no complete nested record is ignored. A malformed FYI marker at the actual message-body
start still fails loudly with `line 1: malformed FYI marker`.

Source hashes from the initial inspection:

- Physical row 56940: `380244a94892952f192942a7372af5575ccf9389c062ee18cf14f2690d11ce76`
- Recovered FYI record: `6bf65e3f2b998c13015953d1d3eb3a931aa4bc2f630e299966bc44326b4401a8`

## Verification

- `bash tests/test-mesh-fyi-ledger.sh` — PASS; includes the two embedded copies, partial-coverage
  gap lines, canonical event de-duplication, and a precise malformed-row error assertion.
- `scripts/mesh-fyi-ledger --test` — PASS.
- `python3 -m py_compile scripts/mesh-fyi-ledger` — PASS.
- `git diff --check` — PASS.
- Live `scripts/mesh-fyi-ledger --witness` — PASS; recurring FYI and linked task dispositions
  rendered. Linked examples include `run-paired-replications=BLOCKED` and
  `summarizer-conditional-entropy=UNKNOWN`.
- Live materialization rebuilt from the unchanged append-only log: 9,078 replayed events,
  9,075 unique identities, 3 repeated identities, 44 linked task references, partial coverage,
  and replay parity PASS. Gap lines: `56425,56940,56957`; the latter two are the duplicate wrappers
  around this recovered record. Captured source cutoff: `2026-09-12T15:05:01Z`, SHA-256
  `2d832f15148e1ec3b8357affbd2e1f0b36fe187dcbdeaaa7a20d084550ef06f0`.
- Refreshed `mesh-dash --once witness` showed FYI replay `pass`, coverage `partial`, age `0s`, and
  linked dispositions including `run-paired-replications=BLOCKED` and
  `summarizer-conditional-entropy=UNKNOWN`.

## Landing

- Parser: `21f742ed57e9e173450058ef0fe8453c382c54a4` at `origin/main`, subject
  `mesh-land: update scripts/mesh-fyi-ledger: recover complete nested FYIs with coverage gaps`.
- Regression: `e1c0a33cccbcc9372612fe53048385ba4e2ac552` at `origin/main`, subject
  `mesh-land: update tests/test-mesh-fyi-ledger.sh: cover nested FYI recovery and malformed rows`.
- Deployed parser SHA-256 matches the source: `c0bd29dfa5e9e04d8ef187991c810e00657fed2a122b81edb8b49405b228f877`.

The task receipt and implementation plan are being landed as scoped documentation units.
