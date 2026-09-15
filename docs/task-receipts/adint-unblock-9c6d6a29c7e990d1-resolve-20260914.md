# Adint duplicate resolver diagnosis — shared-task routing shadow

Task: `unblock/adint/9c6d6a29c7e990d1/resolve`

## Finding

This retry points to the rejected witness resolver
`unblock/witness/b4b3e19d674c3da8/resolve`. At `2026-09-14T17:22:47Z`, the ledger still marked
that resolver rejected and the original
`self-review-routing-shadow-20260914/independently-evaluate-routing-shadow` step blocked on its
frozen 14-day/100-eligible-task gate. The latest live scorer evidence is the immediately preceding
adint receipt `docs/task-receipts/adint-unblock-b497e0c1256df56d-resolve-20260914.md`: scorer run
at `17:20:12Z`, 0 eligible tasks, 0 recommendations, collecting. That receipt also records the
source digest, report digest, and nine passing fixture tests.

The gate has no safe internal prerequisite that can make elapsed trial time or genuine eligible
tasks appear sooner. Synthetic or relabelled tasks would invalidate the frozen sample. The scorer,
fixture tests, frozen criteria, and trial are already present, so creating another resolver or
comparison task now would duplicate work or bypass the gate. I leave the evaluator blocked.

## Next action

At `2026-09-28T16:52:06Z`, rerun the scorer and inspect whether at least 100 eligible tasks exist.
If so, create the fresh witness-owned comparison task with links to this evidence and the rejected
resolver history. If fewer than 100 exist, continue collection and issue the terminal INCONCLUSIVE
review by `2026-10-14T16:52:06Z`.
