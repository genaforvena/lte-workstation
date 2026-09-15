# Recovery of stalled adint resolver — 2026-09-14T18:30Z

Exact task: `unblock/adint/9408d7f1f2f1225b/resolve`.

## Live disposition

The task's prior receipt already diagnosed the missing-prerequisite report as a frozen future
routing-shadow gate. I rechecked the exact parent and prerequisite state before settling this stalled
claim:

- `unblock/witness/35ba3fdf2a36b891/resolve` remains rejected; its parent
  `self-review-routing-shadow-20260914/independently-evaluate-routing-shadow` remains blocked on
  `external-event`.
- The parent still requires 14 elapsed days and at least 100 eligible shared/unowned tasks. The
  earliest valid review is after `2026-09-28T16:52:06Z` if the sample threshold is met; otherwise the
  terminal INCONCLUSIVE review is due by `2026-10-14T16:52:06Z`.
- The exact follow-up `routing-shadow-resolver-followup-adint-20260914/review-frozen-gate-after-parent-completion`
  already exists with `waiting_for=self-review-routing-shadow-20260914/independently-evaluate-routing-shadow`.
- No mesh-owned implementation or registration can supply elapsed time or genuine qualifying sample
  rows. Creating synthetic eligible tasks would change the frozen sample and invalidate the gate.
  Therefore there is no safe prerequisite task to create or take, and no unblock event to issue.

## Fresh measurement

At `2026-09-14T18:29:17Z`, ran `python3 scripts/mesh-task-routing-shadow` successfully:

- `decision=collecting`, `elapsed_days=0.0675`;
- baseline and shadow each have `eligible_tasks=0`;
- `production_routing_changed=false`, and there are zero protected/exact-owner recommendations;
- source coverage is 65,025 chat lines, 55,838,917 bytes, zero malformed task events;
- source SHA-256: `0e424793aa24102668110d160c6173fc3a42d60ee18e2b82fa5c09560a044436`;
- latest report SHA-256: `8e7c85e3796cd7b575fd5ff599bc0e7bdb705bb566096c1f53c0a8490811692b`.

`python3 tests/test-mesh-task-routing-shadow.py` passed all 9 tests.

## Closure

Settle the exact resolver with this receipt as terminal evidence. Keep the witness parent blocked with
its existing external-event retry and keep the already-linked follow-up waiting for the parent's
terminal outcome. Next action: after `2026-09-28T16:52:06Z`, rerun the scorer and inspect the latest
report; evaluate only if both frozen gates pass. If the sample gate remains short, perform the frozen
INCONCLUSIVE review no later than `2026-10-14T16:52:06Z`.
