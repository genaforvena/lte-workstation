# Bounded Self-Review Shadow Implementation Plan

> **For agentic workers:** Use inline execution in this authorized genome task. Keep the steps in order and verify each behavior with the focused test before landing.

**Goal:** Produce an on-demand, read-only per-mind review artifact from accepted task-ledger, retained-artifact, and timestamped board evidence.

**Architecture:** Add one standalone Python tool under `scripts/`. It reads append-only `chat.log`, decodes canonical task-state events through the repository's task-log codec, matches timestamped board markers to exact task IDs, and writes a durable per-mind cursor plus a separate non-liveness JSONL report. The first call may report when the initial bounded source window meets the 50-record threshold; later calls trigger after 50 new attributable source records or six hours, with a one-hour minimum interval.

**Tech Stack:** Python 3 standard library; existing `mesh_task_log` decoder; shell-based fixture tests.

## Global Constraints

- Consume only canonical task transitions, retained task artifacts, and timestamped board lines.
- Review at most the latest 50 source records in six hours and 20 task transitions per report.
- Persist the source cursor before writing a recommendation report.
- Deduplicate by exact task ID and retain duplicate-match evidence.
- Emit exactly one evidence-linked no-action, update, or new-task recommendation per report.
- Exclude this tool's own output and routine `[handoff]` / `[idle]` churn from triggers.
- Do not ingest raw conversations, schedule a trigger, create tasks, or mutate routing/substrate state.
- Record source coverage, dispositions, duplicate matches, missing evidence, and processing cost outside liveness logs.

---

### Task 1: Add source parsing and bounded trigger tests

**Files:**
- Create: `tests/test-mesh-self-review-shadow.py`
- Create: `scripts/mesh-self-review-shadow`

**Interfaces:**
- CLI: `mesh-self-review-shadow <mind> [--chat-log PATH] [--state-dir PATH] [--report-dir PATH] [--now ISO-8601]`
- Source rows carry exact task ID, owner, event timestamp, source kind, byte offset, and digest.
- Report JSON contains bounds, input coverage, task/artifact dispositions, duplicate matches, processing time, and one recommendation object.

- [x] Write fixture tests for event decoding, handoff/idle exclusion, the 50-record/six-hour trigger, the one-hour minimum, the 20-transition cap, digest mismatch as unknown, and exact-task deduplication.
- [x] Run the focused test and confirm it fails because the tool is absent.
- [x] Implement the smallest parser and trigger logic that passes the tests.
- [x] Run the focused test to green before adding artifact and cursor tests.

### Task 2: Persist cursor before recommendation output

**Files:**
- Modify: `scripts/mesh-self-review-shadow`
- Modify: `tests/test-mesh-self-review-shadow.py`

- [x] Add a test that observes the cursor already advanced when report writing begins.
- [x] Add atomic per-mind cursor storage with a lock and source identity/high-water offset.
- [x] Add a separate non-liveness report artifact and exactly-one recommendation record.
- [x] Verify crash-safe ordering and idempotent exact-task duplicate handling with fixtures.

### Task 3: Validate live read-only operation and document outcome

**Files:**
- Modify: `scripts/mesh-self-review-shadow`
- Create: `docs/task-receipts/self-review-shadow-implementation-20260914.md`

- [x] Run a bounded live review from the accepted sources without scheduling or mutation.
- [x] Record source coverage, dispositions, duplicate matches, missing evidence, and measured processing cost.
- [x] Run focused test and syntax checks; inspect the report and cursor artifacts.
- [ ] Land only this plan, tool, test, and receipt through the mesh landing path.
