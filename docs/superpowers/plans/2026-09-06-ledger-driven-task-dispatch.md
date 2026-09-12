# Ledger-Driven Task Dispatch Implementation Plan

> **Status: SUPERSEDED for dispatch authority.** The 2026-09-08 tasks-only coordination decision
> makes structured task-state events in `chat.log` the lifecycle and dispatch authority; hledger
> promises remain a materialized accounting view and are not a separately dispatchable queue. See
> `docs/task-only-coordination-20260908.md` and the audit at
> `docs/design-audit-ledger-driven-task-dispatch-20260912.md`. Retain this plan as historical design
> evidence; do not implement its hledger-first dispatch path without a new operator decision.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make hledger-backed promise liabilities the dispatch queue, including ordered multi-step chains, while retaining the board as the event and human-readable coordination surface.

**Architecture:** `mesh-promises --feed` materializes board events into the promise journal. A new `mesh-board` query surface reads that journal for open obligations, owner/task queries, and counts. `mesh-dispatch` consumes the query surface for its candidate set and preserves existing pacing, ownership, and delivery behavior; it uses an explicit, loud board fallback only when the ledger is unavailable.

**Tech Stack:** Bash, Python 3, hledger, existing `mesh-promises`, `mesh-dispatch`, and `mesh-task` artifacts.

## Global Constraints

- Preserve unrelated dirty worktree changes.
- Every ledger transaction must remain hledger-balanced and replay/query agreement must be checkable.
- Multi-step chains remain ordered and artifact-gated; only the current eligible step is dispatchable.
- Failed delivery remains retryable and must not be recorded as delivered.
- Do not remove existing cron or board wiring in this change.

### Task 1: Add the ledger query surface

**Files:**
- Create: `scripts/mesh-board`
- Test: `scripts/mesh-board` self-test

- [ ] Write failing tests for open count, owner-filtered obligations, task lookup, and unavailable-ledger refusal.
- [ ] Run `bash scripts/mesh-board --test` and observe the expected failures.
- [ ] Implement hledger-backed `open`, `count`, `owes`, `task`, and `incidents` commands with explicit errors.
- [ ] Run the focused self-test and verify it passes.

### Task 2: Route dispatch candidates from liabilities

**Files:**
- Modify: `scripts/mesh-dispatch`
- Test: `scripts/mesh-dispatch` self-test

- [ ] Add a failing fixture where the board contains repeated task lines but the promise ledger has one net open liability; assert dispatch sees one candidate.
- [ ] Run the focused self-test and observe failure against the current board scan.
- [ ] Replace the live candidate source with `mesh-board open --dispatch`, preserving priority, owner, human-owned refusal, hold handling, and one-dispatch pacing.
- [ ] Add an explicit `ledger-unavailable` diagnostic and retain board scanning only as an intentional compatibility mode.
- [ ] Run `bash scripts/mesh-dispatch --test` and verify the existing regression suite remains green.

### Task 3: Connect ordered chains to ledger task identity

**Files:**
- Modify: `scripts/mesh-task`
- Test: `scripts/mesh-task` self-test

- [ ] Add failing assertions that create/take/done emits one stable `task:<chain>/<step>` identity and that only the current step is eligible.
- [ ] Run the focused self-test and observe failure if the ledger feed cannot identify the chain step.
- [ ] Add the minimal tagged lifecycle emission while preserving current JSON chain and context artifacts.
- [ ] Run `bash scripts/mesh-task --test` and verify ordered handoff, artifact gate, and retry behavior.

### Task 4: End-to-end verification

- [ ] Run `bash scripts/mesh-board --test`.
- [ ] Run `bash scripts/mesh-task --test`.
- [ ] Run `bash scripts/mesh-dispatch --test`.
- [ ] Run `mesh-promises --check` and confirm parity plus replay/balance agreement.
- [ ] Record the actual artifacts and any compatibility limitation in the handoff.
