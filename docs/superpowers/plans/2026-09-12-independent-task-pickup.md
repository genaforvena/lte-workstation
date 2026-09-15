# Independent Task Pickup Implementation Plan

> **For agentic workers:** execute this plan inline with test-first changes.

**Goal:** Let an exact task owner pick a later step that is genuinely independent of a blocked chain head, while preserving normal sequential and explicit prerequisite gates.

**Architecture:** Add an owner-authored `independent` annotation with a required reason to an open later step. Dispatch eligibility, queue output, take/settle transitions, audit, and status must agree on this annotation. Existing steps remain serial by default; `waiting_for` remains an unconditional gate. Settling an independent step leaves a blocked head/current pointer intact, and ordinary completion later skips already-terminal independent steps.

**Tech Stack:** Python task coordinator and replay library, shell-invoked Python regression test, append-only `chat.log` task-state records.

## Global Constraints

- `chat.log` task-state records remain canonical; task-chain JSON stays a disposable cache.
- Keep exact-owner and one-active-task-per-owner enforcement.
- Do not bypass a step's explicit `waiting_for` prerequisite.
- Do not edit unrelated dirty files in the shared checkout.

### Task 1: Reproduce independent pickup and record observability

**Files:**
- Create: `tests/test-mesh-task-independent-pickup.py`
- Modify: `scripts/mesh_task_log.py`
- Modify: `scripts/mesh-task`

- [ ] Write a failing isolated test that creates a two-step chain, blocks step one, authorizes step two as independent, and asserts `check dispatch` and the owner queue expose only step two.
- [ ] Assert wrong-owner authorization fails, `waiting_for` still refuses dispatch, and an independent `[taking]` / completion leaves the original blocked step visible in audit and status.
- [ ] Assert completing the original head advances across an already-completed independent step without reopening it.
- [ ] Run the test and confirm failure is due to the missing independent-step interface.
- [ ] Implement owner-authored independence metadata and align queue, check, take, settle, and audit behavior.
- [ ] Run the focused test plus `mesh-task --test`.

### Task 2: Verify live observability and ledger wiring

**Files:**
- Modify: `tests/test-mesh-task-independent-pickup.py` if an uncovered observable is found.
- Verify: `mesh-task audit`, `mesh-task queue --dispatch --owner`, `mesh-task check dispatch`, and `mesh-task status` in the isolated fixture.

- [ ] Confirm canonical replay preserves the independent reason and task transitions.
- [ ] Confirm default sequential chains remain ineligible out of order.
- [ ] Record exact verification output and any limitation in the task receipt.
