# Human-Readable Task Ledger Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace opaque future `[task-state]` appends with human-readable authoritative ledger messages while preserving replay of all existing JSON and `plist64` history.

**Architecture:** Keep `chat.log` as the sole authority and retain snapshot revisions, but serialize each new snapshot as a readable `[task-ledger]` message with an explicit version, revision, chain identity, current step, chain status, and readable step clauses. Parse legacy `[task-state]` JSON/`plist64` and new `[task-ledger]` lines into the same validated in-memory record, so no historical rewrite is needed.

**Tech Stack:** Python 3 standard library, shell integration tests, append-only `chat.log`.

## Global Constraints

- Future writes must not append `[task-state]`, JSON, plist64, or another opaque whole-record payload.
- Existing JSON and plist64 records remain replayable without modifying `chat.log`.
- New records must remain one physical board line, survive arbitrary Unicode descriptions, and reject malformed, conflicting, missing, or truncated revisions.
- Secret scrubbing happens before durable append and a scrub-induced mutation refuses the transition.
- `chat.log` remains authoritative; task-chain JSON and `tasks.journal` remain rebuildable views.

---

### Task 1: Define the readable wire contract

**Files:**
- Create: `docs/human-readable-task-ledger-contract-20260908.md`

**Interfaces:**
- Consumes: current schema validated by `scripts/mesh_task_log.py:validate`
- Produces: exact `encode_readable(record) -> str` and `decode_readable(payload) -> dict` grammar for Task 2

- [ ] **Step 1: Record representative OPEN, ACTIVE, DONE, BLOCKED, and REJECTED lines.**
- [ ] **Step 2: Specify escaping, field ordering, revision rules, and the legacy marker boundary.**
- [ ] **Step 3: Specify acceptance commands and live-canary evidence.**

### Task 2: Implement readable writer and mixed replay

**Files:**
- Modify: `scripts/mesh_task_log.py`
- Modify: `scripts/mesh-task`
- Modify: `scripts/mesh-chat`
- Test: `tests/test-mesh-task-log.py`
- Test: `tests/test-mesh-task-source-coverage.sh`

**Interfaces:**
- Consumes: Task 1 wire contract
- Produces: new readable encoder/decoder and replay of both `[task-ledger]` and legacy `[task-state]`

- [ ] **Step 1: Replace the plist64 expectation with a test that requires readable field labels and forbids future `[task-state]`, JSON, and plist64 output.**
- [ ] **Step 2: Run `rtk python3 -m unittest tests/test-mesh-task-log.py` and confirm the new assertion fails because encoding still starts with `plist64:`.**
- [ ] **Step 3: Add readable serialization and parsing with deterministic escaping, then route new appends through `[task-ledger]`.**
- [ ] **Step 4: Run the focused unit and source-coverage tests and confirm they pass.**
- [ ] **Step 5: Mutate the readable writer back to plist64 in a temporary copy and confirm the regression assertion fails.**

### Task 3: Verify live future behavior and views

**Files:**
- Create: `docs/human-readable-task-ledger-verification-20260908.md`

**Interfaces:**
- Consumes: Task 2 implementation
- Produces: fresh live `chat.log` line references, replay result, pane output, and checksums

- [ ] **Step 1: Run the complete focused task-ledger test set and record exit codes.**
- [ ] **Step 2: Create and settle a bounded canary chain, then identify every line appended after the baseline byte offset.**
- [ ] **Step 3: Prove appended authoritative records are readable `[task-ledger]` messages and contain no `[task-state]`, JSON snapshot, or plist64 payload.**
- [ ] **Step 4: Run `rtk mesh-task replay --json`, `rtk mesh-task audit`, and `rtk mesh-dash --once witness`; verify legacy and new chains coexist and the pane remains truthful.**
- [ ] **Step 5: Record exact commands, outputs, artifact checksums, unresolved limitations, and close the chain only if every gate passes.**
