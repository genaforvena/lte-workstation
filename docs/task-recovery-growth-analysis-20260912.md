# Task recovery growth analysis

Date: 2026-09-12 UTC  
Task: `task-recovery-growth-20260912/bound-blocker-recovery-growth`

## Finding

The five-minute `mesh-task-unblock-sweep` could create another resolver for an unchanged
blocked epoch while a previous retry was still open. `ensure_unblock_task()` collected completed
unresolved attempts separately from pending attempts; if any terminal failure existed, it retried
that old result without first checking for a newer open resolver. A live phone-reachability blocker
had reached 45 resolver chains (attempts 2–45 were still open and unclaimed). The scheduled sweep
also recursively generated recovery work for blocked recovery tasks, with no ancestry limit.

At 00:09:43, the canonical journal reported 746 tasks: 272 unfinished, 408 DONE, and 66 REJECTED.
The audit showed 79 `OPEN_UNOWNED` steps, and replay found 249 resolver chains with retries up to
attempt 39. Just before the final fix, the same phone blocker had 45 attempts, 44 pending. This is
direct evidence of task growth without corresponding owner start or terminal evidence.

## Change

`scripts/mesh-task` now:

- returns the newest pending resolver before considering terminal failures;
- orders terminal retries by `unblock_attempt` first, so equal-second creation timestamps cannot
  make backoff inspect an older attempt;
- caps automatic retries at three terminal unresolved results and writes one durable `[yield]`
  explaining that the parent remains blocked on its stated retry condition;
- caps recovery ancestry at two resolver levels (the original resolver and one cross-mind hop).
  A resolver blocked at that cap remains visible with its `needs` and `retry` fields and emits a
  `[yield]`; no third-level task is created.

Existing tasks remain in the append-only ledger. The change does not impersonate their owners or
close old pending attempts. The owner still must produce a real artifact, reject with a concrete
reason, or resume after the exact prerequisite is evidenced.

## Verification

- `tests/test-mesh-task-recovery-growth.py` — 3 tests PASS. It first reproduced the duplicate while
  a failed attempt and newer open attempts coexisted, and the third-level recovery spawn; it now
  checks pending-task idempotency, the three-attempt cap, and the depth cap.
- `tests/test-mesh-task-blocked-self-unblock.py` — 16 tests PASS, including the existing bounded
  backoff and one-hop recovery cases.
- `scripts/mesh-task --test`, `scripts/mesh-task-unblock-sweep --test`, and Python compilation —
  PASS.
- `tests/test-mesh-task-no-expiry.py` was also run and failed in its pre-existing unstaged additions:
  those assertions expect prose-valued `unblock_for` keys and no resolvers for owner-bearing
  external/operator blockers, while the current ledger contract uses hashed epoch identities and
  materializes owner resolvers. That file was left unchanged; its contract mismatch remains open.
- Source and deployed `mesh-task` SHA-256 match:
  `6081b392b53094ba1cec3c58f521c62e5ecbbe4d472406acd74a28247ecb8441`.
- The deployed sweep wrapper matches its source at SHA-256
  `892a197a7c244c20e2668d71ffda5479655cfba0ee180b82fc394fe02958addb`; crontab runs it every five
  minutes at `*/5 * * * *`.
- The live all-owner cron sweep at 00:30 returned `unblock-sweep owner=all created=0`. The phone
  blocker remained at 45 attempts with 44 pending both before and after that sweep; no new attempt
  was recorded.
- At 00:34:40, the live pane showed 775 tasks, 287 unfinished, 66 rejected, and 422 done. Its task
  journal was 6 seconds old and the board tail displayed 20 of 51,897 raw lines, unfiltered. The
  journal source was `PASS` with zero replay errors.

The ledger still has substantial open work: the current audit view includes 98 `OPEN_UNOWNED`, 48
`BLOCKED`, and 90 `QUEUED` steps, plus 46 held-expired and 3 held-rejected rows. The audit therefore
remains non-green; this fix stops one source of unbounded recovery growth but does not prove that the
remaining tasks have started or finished. The 44 already-open duplicate resolvers remain owner
obligations.

## Next action

At the next witness sweep, reconcile the genome-owned pending resolvers for
`coordination-hledger-identity-phone-20260908/phone-authorized-keys-recheck`: verify the exact owner
has taken one current resolver, then require artifact-backed completion or a concrete REJECTED reason
for duplicate attempts. Continue the same exact-owner start/terminal check for the remaining
`OPEN_UNOWNED` rows; do not infer progress from dispatch or silence.
