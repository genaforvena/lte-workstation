# FYI Ledger Embedded Event Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let FYI replay recover a complete embedded FYI event from a non-FYI source row while marking coverage partial, without accepting malformed FYI rows.

**Architecture:** Keep `chat.log` append-only and adjust only `scripts/mesh-fyi-ledger` source parsing. A nested record is recoverable only when its timestamp, author, separator, and `[fyi]` marker form a complete recognizable prefix; record its physical line as a parse gap. Extend the existing shell regression with the precise historical shape and retain the loud malformed-row assertion.

**Tech Stack:** Python 3 standard library, Bash regression, hledger.

## Global Constraints

- Never edit or rewrite `~/.mesh/chat.log`.
- Keep malformed FYI message bodies as a nonzero replay failure.
- Publish partial coverage and the physical gap line for recovered embedded events.
- Rebuild the live FYI materialization only after focused tests pass.

---

### Task 1: Specify recovery and malformed-row behavior

**Files:**
- Modify: `tests/test-mesh-fyi-ledger.sh`
- Test: `tests/test-mesh-fyi-ledger.sh`

**Interfaces:**
- The test drives the public `mesh-fyi-ledger --build` command and checks its materialized manifest and journal.

- [x] Add a fixture shaped like the 2026-08-30 `[strand]` source row with a complete embedded 2026-08-22 FYI event.
- [x] Assert recovery, `coverage=partial`, physical gap lines, canonical event de-duplication, and the recovered event in the journal.
- [x] Keep the malformed complete FYI row fixture and assert its precise error.
- [x] Run `bash tests/test-mesh-fyi-ledger.sh`; it failed on the embedded-event case before implementation.

### Task 2: Recover complete nested FYI events with explicit gaps

**Files:**
- Modify: `scripts/mesh-fyi-ledger`
- Test: `tests/test-mesh-fyi-ledger.sh`

**Interfaces:**
- `parse_source(path)` continues returning `(rows, manifest)`; nested recoveries add a physical line number to `manifest["parse_gap_lines"]` and force partial coverage.

- [x] Extend parsing of valid non-FYI outer rows to locate a nested complete `timestamp author :: [fyi]` record; ignore marker-like prose with no complete record.
- [x] Parse the recovered FYI record through the existing validation and materialization path, hashing the recovered record for stable de-duplication.
- [x] Run `bash tests/test-mesh-fyi-ledger.sh` and verify malformed true FYI rows remain a failure.
- [x] Run `scripts/mesh-fyi-ledger --test`.

### Task 3: Rebuild and verify the live view

**Files:**
- Create: `docs/task-receipts/fyi-ledger-malformed-row-20260912.md`

**Interfaces:**
- Live replay uses the unchanged append-only `~/.mesh/chat.log`; the witness pane reads the materialized `~/.mesh/fyi` view.

- [x] Run the deployed `mesh-fyi-ledger --build` and `--witness`; inspect `~/.mesh/fyi/manifest`.
- [x] Run `mesh-dash --once witness`; record pane age, replay status, linked dispositions, and partial source coverage.
- [x] Finalize the receipt with the parser decision, source hashes, test output, live replay output, and landing evidence.
