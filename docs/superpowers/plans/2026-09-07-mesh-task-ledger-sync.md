# Mesh Task Ledger Synchronization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent a durable multi-step chain from changing state when its matching board/hledger lifecycle event cannot be written.

**Architecture:** Keep `mesh-task` JSON as the ordered-chain state and the board-derived hledger journal as the obligation score, but make every lifecycle transition require its board event before committing the new JSON state. Successor dispatch retains its existing retryable `dispatch=failed` state because the completed step's keyed `[done]` event has already been written.

**Tech Stack:** Python 3 standard library, shell integration tests, `mesh-chat`, hledger-derived `mesh-promises`.

## Global Constraints

- Preserve exact owner enforcement, ordered steps, artifact hashing, and retryable successor dispatch.
- Never report a successful lifecycle transition when its canonical board event was not written.
- Verification must exercise the real `mesh-task` command boundary with failing and successful emitters.

---

### Task 1: Fail closed on lifecycle board writes

**Files:**
- Modify: `scripts/mesh-task`
- Create: `tests/test-mesh-task-ledger-sync.sh`
- Create: `docs/coordination-task-ledger-sync-20260907.md`

**Interfaces:**
- Consumes: `MESH_TASK_CHAT_CMD`, canonical task IDs, current chain JSON.
- Produces: non-zero exit with unchanged transition state when a lifecycle event cannot be written.

- [ ] **Step 1: Write the failing integration test**

Create a private chain with a successful task post, then switch the emitter to `/bin/false`. Assert failed `take` leaves the step `open`, and failed `done` leaves an already claimed step `active` without an artifact.

- [ ] **Step 2: Run the test to verify it fails**

Run: `bash tests/test-mesh-task-ledger-sync.sh`

Expected: FAIL because current `mesh-task` exits zero and advances JSON despite `/bin/false`.

- [ ] **Step 3: Implement required emission**

Add one helper that raises a loud error when `emit()` returns false. Build each canonical lifecycle body from the proposed new state, require its emission, and only then save the chain/context transition.

- [ ] **Step 4: Run focused and regression checks**

Run: `bash tests/test-mesh-task-ledger-sync.sh && python3 scripts/mesh-task --test && bash tests/test-mesh-task-audit-complete.sh && mesh-promises --feed && mesh-promises --check`

Expected: all PASS; live promise replay agrees with hledger.

- [ ] **Step 5: Record the live audit artifact**

Document the board example, root cause, changed boundary, red/green evidence, live hledger verification, and any remaining limitation in `docs/coordination-task-ledger-sync-20260907.md`.

### Task 2: Make promise admission a mesh-wide work rule

**Files:**
- Modify: `CLAUDE.md`
- Create: `memory/multi-step-work-enters-the-promise-ledger-before-execution.md`

**Interfaces:**
- Consumes: operator asks, autonomous findings, `mesh-task create`, board `[task]` promises.
- Produces: one shared rule loaded by every mind, with the decision boundary between a bounded observation and durable multi-step work.

- [ ] **Step 1: Measure current adoption**

Compare recent `spend.log` TURN rows with `task:` attribution, then inspect the corresponding board and task-chain records. Record the measurement without treating idle observation turns as unambiguously missing tasks.

- [ ] **Step 2: Put the intake rule in mesh-wide doctrine**

Add one rule under board coordination: before executing work that has multiple required steps or must survive a turn, create a promise/`mesh-task` chain with exact owner, next action, artifact, and closure criterion. A prose handoff cannot be its only state.

- [ ] **Step 3: Record the case**

Capture the repeated semantic-receipt/live-ledger mismatch, the low task-tag attribution measurement, and the executable fail-closed repair in the linked memory case.

- [ ] **Step 4: Verify loaded doctrine and live ledger**

Run: `rg -n 'multi-step-work-enters-the-promise-ledger' CLAUDE.md && mesh-promises --feed && mesh-promises --check && mesh-task audit`

Expected: doctrine link present; parity/agreement pass; active chain work is visible by exact owner and lease.
