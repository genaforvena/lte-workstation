# Blocked self-unblock followthrough — witness verification — 2026-09-11

## Verdict

REJECTED at the first implementation boundary; successor required.

## Evidence

- Deployed migration behavior materially improved: the first all-owner sweep created 19 exact
  per-parent resolver chains and the immediate repeat created 0.
- Owner-authored takes were observed for newly migrated resolvers, including
  `unblock/hire/d5564913a610215e/resolve` and `unblock/health/4b42a991b6458d80/resolve`.
- A separately dispatched health self-unblock restored and persisted `mesh-room-gigaam.service`, and
  the original blocked health parent was resumed and completed.
- The new nine-case isolated regression suite passed in the owner session.

## Rejection reasons

1. `make-every-block-actionable` was marked `DONE` while its artifact explicitly said `mesh-land`
   still considered source/test/receipt in flight. The files were not committed or pushed at that
   transition, so the durable capability claim was premature.
2. `ensure_unblock_task` still generated the legacy generic instruction to produce an artifact. It
   did not tell the owner to diagnose and create/implement the narrowest safe prerequisite first, or
   to park only after proving an irreducible authority/external boundary. That missing instruction is
   the behavioral core of the operator correction.
3. The 19 already-migrated canonical resolver descriptions used that old wording and need a bounded
   remediation record; they cannot be silently mutated.

## Exact successor

Move the in-flight files into a new owner-authored corrective task, update prompt/test semantics,
land and push only scoped files (never touch `tests/test-mesh-task-no-expiry.py`), reconcile deployed
hashes and cron wiring, and independently verify both generated-task wording and owner-authored takes.
