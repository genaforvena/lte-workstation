# Blocked chains and independent progress — 2026-09-08

Task: `wake-coordination-repair-20260908/blocked-chain-independent-progress`.

## Verdict

**REJECTED: do not infer or auto-dispatch an in-chain successor past a typed
blocker.** `mesh-task` chains are ordered sequences, not dependency graphs. The
three-column TSV accepted by `mesh-task create` records `owner`, `slug`, and
description only; it has no machine-readable prerequisite edge. Treating a
later row as independent would substitute an unverified scheduler guess for
the plan's declared order, and could start work whose missing prerequisite is
safety-, capability-, or operator-input-related.

The safe dispatch rule is already available: put genuinely independent work in
its own chain. A typed block continues to hold only its own chain; the other
chain can be claimed by its exact owner and retains its normal receipt,
lease, artifact, and audit obligations. A final verification step belongs in
the dependent chain only after its inputs are actually settled.

No `mesh-task` source change is appropriate for this task. Adding a scheduler
escape hatch without a declared DAG would make the failure direction silent:
the system would call a dependency absent because it was never represented.

## Deterministic fixture

The existing self-test constructs exactly the safe split:

1. Create `demo/verify`, claim it as `beta`, and type-block it on
   `operator-input` / `csv-path`.
2. Create a separate `second/work` chain for the same owner.
3. Claim `second/work` successfully while `demo/verify` remains visibly
   `blocked`; then type-block it independently.
4. Assert that dispatching the blocked `demo` chain is refused, then resume
   and settle it before its own successor is dispatched.

This is intentionally unlike a successor in `demo`: `take()` rejects any row
whose index is not `current`, while a distinct chain is separately claimable.
The fixture is in `scripts/mesh-task`'s `--test` routine (the independent
chain section) and is exercised by the commands below.

## Verification

At 2026-09-08T02:44Z:

```
$ python3 scripts/mesh-task --test
mesh-task: smoke-test ok (canonical ask/task, exact owner, lease/progress,
typed block/resume, artifact hash, idempotent done)

$ bash tests/test-mesh-task-reschedule.sh
test-mesh-task-reschedule: PASS (sent/unclaimed and expired work re-dispatch exactly)
```

`git diff --check` also passed. These checks verify the fixture's typed-block
hold, cross-chain claimability, and normal dispatch recovery; they do not
claim that queued rows are independent.

## Live-chain reconciliation

`mesh-task audit` at 2026-09-08T02:43Z showed the issue on live data:

| blocked current row | queued row that must not be inferred independent |
| --- | --- |
| `design-audit-task-sweep-20260907/plans-sound-collage` (`dependency`) | `design-audit-task-sweep-20260907/plans-window-lease` (`wake`) |
| `design-spec-task-sweep-20260907/spec-sound-pane-records` (`dependency`) | `design-spec-task-sweep-20260907/spec-clear-on-claim` (`wake`) |
| `ask-answer-funnel-implementation-20260907/unit-5-canary` (`dependency`) | `ask-answer-funnel-implementation-20260907/final-funnel-verification` (`tg`) |

The row descriptions make the first two look separate, but they are in
historical ordered sweep chains with no declared dependency metadata. Their
current `QUEUED` status is therefore honest, not a scheduler bug. They were
not reordered or dispatched. If the owning planners confirm independence,
they must create separate artifact-gated chains (and leave the original
blocked row and its final verifier intact) rather than mutate history or
silently bypass the blocker.

## Next action

Proceed to `wake-coordination-repair-20260908/receipt-race-reconciliation`.
The final chain verification must record this rejection and confirm no source
or deployed-copy parity work was created by it.
