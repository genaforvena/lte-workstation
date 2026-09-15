# Receipt-race reconciliation — 2026-09-08

Task: `wake-coordination-repair-20260908/receipt-race-reconciliation`.

## Finding and repair

`mesh-task` deliberately emits a board receipt before committing the matching
chain JSON: if the board write fails, the durable state must not silently
advance. Before this repair, that necessary ordering left a race. While an
owner's `take` was blocked in `mesh-chat` immediately after writing `[taking]`,
a witness `reschedule-task` could read the still-open JSON, emit a stale
`[yield]`, re-post `[task]`, and save an open row. The owner would then save
its active row. The final chain state looked claimed, but the board contained
the false recovery chase and duplicate dispatch.

`scripts/mesh-task` now holds one advisory exclusive lock at
`$MESH_TASK_DIR/.mesh-task.lock` for every mutating transition, including
`take`, `done`, and `reschedule-task`; read-only `status` and `audit` remain
available while a receipt writer is held. The lock covers receipt emission and
the corresponding atomic JSON replacement. Thus recovery waits for a newer
canonical owner transition, reloads it, and refuses the re-schedule when the
row is active or done. It does not attempt to infer state from arbitrary prose
or an ACK: canonical owner receipts remain the task-keyed transitions emitted
by `mesh-task`.

This is intentionally a directory-wide lock rather than a per-chain lock.
`take()` also checks the owner's contexts across chains, so separate chain
locks would still leave a multi-file owner-claim race.

## Deterministic ordering fixture

`tests/test-mesh-task-reschedule.sh` now uses a fake `mesh-chat` that writes
the owner `[taking]` receipt and blocks before returning. It then launches a
witness re-schedule concurrently.

Before the repair the fixture fails with:

```
FAIL: stale witness re-schedule completed while owner [taking] was held
```

After the repair it proves that `status` remains available while the owner is
held, while the recovery process remains blocked until the owner is allowed to
save, then fails its re-schedule instead of issuing a yield/re-dispatch. It
asserts the chain remains `active`, the row remains
`active`, there are only the three pre-existing `[task]` deliveries, and no
`unclaimed dispatch re-scheduled` line was written.

## Verification

At 2026-09-08T02:47Z:

```
$ bash tests/test-mesh-task-reschedule.sh
test-mesh-task-reschedule: PASS (sent/unclaimed recovery and receipt race preserve exact owner claim)

$ python3 scripts/mesh-task --test
mesh-task: smoke-test ok (canonical ask/task, exact owner, lease/progress,
typed block/resume, artifact hash, idempotent done)

$ bash tests/test-mesh-task-dispatch-receipt.sh
test-mesh-task-dispatch-receipt: PASS (initial dispatch carries exact take command)

$ bash tests/test-mesh-witness-lifecycle.sh
test-mesh-witness-lifecycle: PASS (adint/tiny-fleet/job alerts, blocked hold, dedup)

$ python3 -m py_compile scripts/mesh-task
$ git diff --check
```

All checks passed. The deployed `~/.local/bin/mesh-task` was source-identical
before this source change, so deployed parity is now intentionally pending a
separate authorized deployment; no installed tool was overwritten.

## Live replay

The board already records this class of stale observation being reconciled
rather than treated as a fresh obligation: at `2026-09-08T02:29:16Z` haunt
reported a corrective take, and at `02:29:22Z` the coordinator rejected it
because the current row had already advanced to
`tinyfleet-applications-20260908/verify-command-intents`. The later canonical
owner receipt at `02:31:06Z` and terminal receipt at `02:32:46Z` confirm why a
recovery snapshot cannot be considered a durable claim by itself. The new lock
makes the same reconciliation atomic for the narrower receipt-before-save
interval.

At the live recheck, `wake-coordination-repair-20260908` remained active at
step 3, owned by `wake`; no live chain was rescheduled during this audit.

## Next action

Settle this step with this artifact, then run the chain's
`final-coordination-verification` step. That final pass must report the source/
deployed parity as pending unless the installer is deliberately run and checked.
