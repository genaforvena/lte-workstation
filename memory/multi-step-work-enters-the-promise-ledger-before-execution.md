# Multi-step work enters the promise ledger before execution

Date: 2026-09-07  
Window: `tg`  
Operator direction: minds should create promises in their work so they can execute and coordinate multi-step tasks through hledger.

## The observed gap

The TG intake design already said operator asks and autonomous discoveries should enter `mesh-task`, but that contract lived in `docs/tg-operator-intake-design-20260907.md`; it was not in the mesh-wide doctrine loaded by every mind. The live board showed the consequence. Between 14:43Z and 15:47Z, `spend.log` recorded 85 Codex TURN rows but only 5 carried `task:` attribution (5.9%). This denominator includes legitimate idle observation turns, so it does not prove 80 missing promises; it does prove that the labour ledger cannot currently attribute most mind activity to durable work branches and that adoption cannot be assumed.

A sharper failure appeared in the promise lifecycle itself. The board contains four semantic reconciliation receipts for `tg-operator-intake-owner` while the authoritative `mesh-promises --balance` continued to show its liability. Only the exact keyed `[done]` at 15:00:44Z produced the matching `-1 PROMISE` transaction. Conversation about completion did not move the ledger.

## Root cause and repair

Two boundaries were open:

1. `scripts/mesh-task` updated chain JSON and ignored failed board writes in `take`, `done`, `progress`, `block`, and `resume`. A chain could therefore advance while its hledger-visible promise/HOLD lifecycle stayed behind.
2. The admission rule was local documentation, so other minds had no loaded invariant requiring long-running work to create a promise before execution.

The implementation adds a required-emission boundary to `mesh-task`: a refused canonical lifecycle event now exits non-zero before chain state changes. `tests/test-mesh-task-ledger-sync.sh` drives `/bin/false` at the real command boundary and asserts failed `take` remains `open` and failed `done` remains `active` without an artifact. The mesh-wide `CLAUDE.md` now requires every multi-step or cross-turn work item—operator-originated or autonomous—to enter a keyed board promise or `mesh-task` chain before execution, with owner, next action, artifact, and closure criterion.

## Honest boundary

Not every TURN should mint a task: idle observation, one bounded answer, and a non-actionable `[fyi]` remain valid without a chain. The enforceable code boundary begins once `mesh-task` is used; the shared doctrine supplies the admission decision before that. A future classifier may audit untagged substantive turns, but raw untagged-TURN count is not safe as a hard gate because it includes legitimate watch work.
