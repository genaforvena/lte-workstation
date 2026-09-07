# TG Presence and Ledger Dispatch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep `tg` focused on operator communication while assigning eligible Ledger work to available non-TG windows with durable ownership, evidence, and witness closure.

**Architecture:** `mesh-promises` remains the authoritative materialized obligation view. A staffing query derives live windows and their current work state from the existing tmux/charter/ledger artifacts, then excludes communication and protected substrate roles before proposing a real owner. `mesh-dispatch` emits only explicit owner-tagged tasks, and every assignment/decline/retry remains visible as a Ledger promise.

**Tech Stack:** Bash, Python 3 standard library, `mesh-promises`, `mesh-board`, `mesh-task`, `mesh-dispatch`, tmux, hledger-derived journals, shell integration tests.

## Global Constraints

- `tg` may create, explain, and relay work but must not become the default worker for repository tasks.
- All delegation must use `mesh-task`/board events so `mesh-promises --feed` and `mesh-promises --check` can account for it.
- Never infer availability from an idle-looking pane alone; require a live window, charter role, and no blocking hold/claim or active protected work.
- Exclude `tg`, `tg-roz`, human-owned work, substrate single-writer work, and windows with stale/blocked ownership unless an explicit operator-directed override exists.
- A task is not assigned until the owner receipt is visible; failed delivery remains open and retryable.
- Preserve unrelated dirty worktree changes and use fixture-driven, mutation-tested verification.

---

### Task 1: Freeze the staffing policy and census contract

**Files:**
- Create: `docs/design-tg-presence-and-ledger-dispatch-20260907.md`
- Test: `tests/test-mesh-tg-dispatch-policy.sh`

**Interfaces:**
- Consumes: `mesh-promises --json`, `tmux list-windows`, charter files, and `mesh-task status`.
- Produces: a versioned policy with fields `window`, `role`, `live`, `protected`, `open_promises`, `open_holds`, `eligible`, `reason`, and `observed_at`.

- [ ] Write fixtures containing `tg`, a free `haunt`, a busy `genome`, a stale `witness`, and a human-owned task; assert only free `haunt` is eligible.
- [ ] Run `bash tests/test-mesh-tg-dispatch-policy.sh`; expected result is red because no policy artifact exists.
- [ ] Document the exact exclusion and eligibility predicates, including the fail-closed result when the census or Ledger is unavailable.
- [ ] Add the policy test's mutation arm: mark `tg` free and confirm the fixture still rejects `tg` as a worker.
- [ ] Run the fixture test and confirm PASS with the mutation failing for the intended reason.

### Task 2: Add a read-only staffing query

**Files:**
- Create: `scripts/mesh-staffing`
- Modify: `scripts/mesh-board`
- Test: `tests/test-mesh-staffing.sh`

**Interfaces:**
- `mesh-staffing --json` returns `{"observed_at":...,"windows":[...]}` and exits non-zero when required live-state inputs cannot be read.
- `mesh-board available --json` exposes the same eligible-window records without creating a task or changing the Ledger.

- [ ] Add tests for live-window enumeration, TG exclusion, protected-role exclusion, open-hold exclusion, and unavailable-input refusal.
- [ ] Run the focused test and verify the missing command/fields fail.
- [ ] Implement the query using bounded subprocess calls, explicit timestamps, and structured reasons for every rejected window.
- [ ] Add a mutation that removes the TG exclusion and assert the test goes red.
- [ ] Run `bash tests/test-mesh-staffing.sh` and `bash scripts/mesh-board --test`; expected result is PASS.

### Task 3: Make dispatch consume staffing candidates

**Files:**
- Modify: `scripts/mesh-dispatch`
- Modify: `scripts/mesh-task`
- Test: `tests/test-mesh-dispatch-staffing.sh`

**Interfaces:**
- `mesh-dispatch` consumes `mesh-board available --json` and chooses one eligible owner per pass.
- `mesh-task create` preserves the plan's owner when explicit; an unowned task receives the selected owner in the emitted board tail before the promise feed.

- [ ] Add a failing fixture with an open task, free `haunt`, busy `genome`, and `tg` as the posting window; assert the task is offered only to `haunt`.
- [ ] Run the fixture before implementation and record the old candidate behavior.
- [ ] Implement one-owner-per-pass dispatch with `owner`, `task`, `status`, and `artifact` tags, without mutating the Ledger directly.
- [ ] Add failed-delivery coverage: a refused owner receipt leaves the promise open and emits a retry reason.
- [ ] Run `bash tests/test-mesh-dispatch-staffing.sh`, `bash scripts/mesh-dispatch --test`, and `python3 scripts/mesh-task --test`.

### Task 4: Turn plans into ordered Ledger promises

**Files:**
- Modify: `scripts/mesh-task`
- Modify: `scripts/mesh-promises`
- Test: `tests/test-mesh-plan-ledger-contract.sh`

**Interfaces:**
- `mesh-task create <chain> <plan.tsv>` emits one promise per step with stable `task:<chain>/<step>` identity.
- `mesh-task dispatch <chain>` exposes only the current eligible step; later steps remain queued and do not become free-floating TG work.

- [ ] Add a plan fixture with four ordered steps and assert `mesh-promises --feed` reports four obligations with only step one dispatchable.
- [ ] Add a failing mutation that deletes one plan row and assert the plan/ledger cardinality check fails.
- [ ] Run `mesh-promises --feed` and `mesh-promises --check` on the fixture; expected parity is PASS.
- [ ] Verify a blocked step stays visible with its retry reason and is not silently reassigned.

### Task 5: Pilot, witness, and operational handoff

**Files:**
- Create: `docs/coordination-tg-presence-and-ledger-dispatch-20260907.md`
- Modify: `docs/mesh-architecture.md`
- Test: `tests/test-mesh-tg-presence-live.sh`

**Interfaces:**
- Produces a live census artifact, one delegated task receipt, one failed-delivery/retry receipt, and a witness verdict.

- [ ] Run the read-only census against the live tmux and Ledger state before enabling dispatch.
- [ ] Dispatch one bounded non-substrate task to an eligible non-TG window and verify owner receipt, artifact path, and promise closure.
- [ ] Run the deliberate delivery failure arm and verify the promise remains open and retryable.
- [ ] Run `mesh-promises --check`, `mesh-task status <pilot-chain>`, and the full focused test set.
- [ ] Publish the witness verdict; if any input is unavailable, publish `BLOCKED` with the exact retry command and leave the promise open.

## Self-review and gaps

The existing ledger-driven dispatch plan covers generic ledger-backed candidate sourcing. This
plan adds the missing operator-channel protection, live-window eligibility predicates, and explicit
staffing pilot. It does not authorize automatic reassignment of substrate or human-owned work.

