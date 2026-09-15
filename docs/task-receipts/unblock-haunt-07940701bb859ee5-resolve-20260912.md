# Unblock receipt: haunt closeout prerequisite — 2026-09-12

Task: `unblock/haunt/07940701bb859ee5/resolve`
Parent: `tinyfleet-publishable-closeout-20260907/publishable-repository-closeout`

## Finding

The prerequisite is not a local code or dispatch repair. The educational lesson
gate requires two distinct adults to independently review the exact `kids-v1`
package and record their own approval or disagreement. The request packet
explicitly forbids entering a record for another person. No such reviews exist,
so neither the gate nor the dependent repository closeout can safely advance.

The existing lesson task was explicitly dispatched to owner `haunt` and is
currently `blocked` on those reviews. A fresh `mesh-task check dispatch
crypthauntology-kids-followup-20260912/lesson-review-safety-gate haunt` returned
exit 2: the blocked row is not dispatch-eligible. That is consistent with its
ledger record; changing task ownership or manufacturing signoffs would not
satisfy the review requirement.

## Evidence

- Repository: `/home/mesh-home/src/hyperhauntology_for_kids`
- Current materials hash, recomputed from `lessons/`:
  `0e0e1b2a066541176fd2fddfb7a3ae30e1da5473dc24e41fa1f1b9258a09b405`
- `protocol/lesson-review-signoffs.json`: `reviewers: []`, matching hash.
- `reports/safety-review.json`: automated checks pass, human review pending,
  `pilot_authorized: false`.
- `docs/task-receipts/haunt-kids-lesson-review-gate-20260912.md`: gate remains
  blocked pending two independent adult reviews.
- Verification: `python3 -m unittest discover -s tests` — 57 tests passed.
- No lesson files, signoffs, or release artifacts were changed.

## Resolution

Keep this unblock task blocked as an external event. Retry only after two
distinct adult reviewers independently record decisions for the current
materials hash. Then re-check and resume the lesson gate, and only after it
reaches a terminal state re-check the Tiny Fleet closeout.
