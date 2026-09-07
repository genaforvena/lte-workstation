# Task-chain / hledger coordination audit — 2026-09-07

## Outcome

The mesh can represent ordered multi-step work with `mesh-task`, but two failures prevented that capability from being reliable across minds:

1. Lifecycle state could advance when the matching board event failed, leaving chain JSON ahead of the hledger promise/HOLD ledger.
2. The rule requiring multi-step and cross-turn work to create a promise lived only in a TG intake design, not in the mesh-wide doctrine every mind loads.

Both boundaries are repaired in the current worktree. `scripts/mesh-task` is also deployed byte-identically to `~/.local/bin/mesh-task`.

## Evidence from the board and ledgers

The board sequence for `tg-operator-intake-owner` contains four semantic reconciliation receipts while `mesh-promises --balance` continued to list the exact liability. The liability cleared only after the exact keyed `[done]` at `2026-09-07T15:00:44Z`, which produced the matching `-1 PROMISE` journal transaction. This demonstrates that prose saying work is complete is not a ledger transition.

The task-chain examples are otherwise structurally sound:

- `ideas-queue-escalations` completed four ordered owner steps with `[task]` → `[taking]` → artifact-hashed `[done]` events.
- `tg-scripts-layout-audit-20260907` completed its TG framing step, handed off to genome, and correctly kept the third step queued while step two remained current.
- At `15:53Z`, that current genome step was `EXPIRED` and the genome pane was idle. TG posted an exact targeted dispatch instructing genome to renew with progress evidence or record a typed block; the queued successor must not start early.

The labour tape also shows the adoption gap. From `14:43Z` through `15:47Z`, 85 Codex TURN rows were recorded and only 5 carried `task:` attribution (5.9%). Idle/watch turns are included, so 80 rows cannot honestly be called missing tasks. The measurement does show that most labour is not attributable to durable branches and that adoption cannot be inferred from the existence of `mesh-task`.

## Root cause and implementation

`take`, `done`, `progress`, `block`, and `resume` called `emit(...)` but discarded its boolean result after or alongside state mutation. A refused `mesh-chat` write therefore returned command success and left JSON in the new state without the canonical event from which `mesh-promises` materializes hledger.

`require_emit(...)` now makes the board write a precondition of these state transitions. A refused event exits 1 before chain JSON or task context is committed. Successor dispatch retains the existing retryable `dispatch=failed` state: by that point the completed step's exact `[done]` has already been emitted and the next open promise can be retried without reopening the completed work.

`CLAUDE.md` now carries the mesh-wide admission rule linked to `memory/multi-step-work-enters-the-promise-ledger-before-execution.md`: operator asks and autonomous findings use the same path; work with multiple required steps or work that must survive the current turn creates a keyed board promise or `mesh-task` chain before execution, with exact owner, next action, expected artifact, and closure criterion. A prose handoff is not sufficient state.

## Red / green and live verification

RED before implementation:

```text
FAIL: take succeeded although its ledger-visible [taking] event was refused
```

GREEN after implementation:

```text
test-mesh-task-ledger-sync: PASS
mesh-task: smoke-test ok (canonical ask/task, exact owner, lease/progress, typed block/resume, artifact hash, idempotent done)
test-mesh-task-audit-complete: PASS
test-mesh-dispatch-hledger-gate: PASS (failed feed blocks routing)
```

Additional checks passed:

- `python3 -m py_compile scripts/mesh-task`
- `git diff --check`
- source/deployed SHA-256 both `36b7a5f3aed40a49b2ab978f9e37035f1be1403a3ee68b8eca597e583b4f1280`
- deployed `~/.local/bin/mesh-task --test`
- `mesh-promises --feed` materialized the current board
- `mesh-promises --check`: parity PASS; promise replay `3 == 3` hledger; claim replay `0 == 0`; hold replay `6 == 6`; ask replay `17 == 17`; no negative liability; owner roster clean

## Remaining obligation

The separate chain `tg-scripts-layout-audit-20260907` remains open at `inventory-and-map`; its expired owner was explicitly re-dispatched at `15:53:47Z`. This audit does not close or impersonate genome's work. Raw untagged TURN count also remains an observation rather than a hard gate because it includes legitimate idle sensing; enforcing promise admission is currently a shared doctrine decision, while transitions after admission are now fail-closed in code.
