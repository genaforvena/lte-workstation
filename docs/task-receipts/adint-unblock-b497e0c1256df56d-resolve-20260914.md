# Adint resolver diagnosis — shared-task routing shadow

Task: `unblock/adint/b497e0c1256df56d/resolve`

## Result

The rejected witness resolver was not missing an internal prerequisite. The source task
`self-review-routing-shadow-20260914/independently-evaluate-routing-shadow` is blocked by its
predeclared evaluation gates: at least 14 days and 100 genuinely eligible shared, unowned tasks,
with a terminal INCONCLUSIVE review at day 30 if fewer than 100 accrue. The trial started at
`2026-09-14T16:52:06Z`; the earliest eligible gate check is `2026-09-28T16:52:06Z`, and the
terminal review is due no later than `2026-10-14T16:52:06Z`.

The earlier evidence is in
`docs/task-receipts/self-review-routing-shadow-interim-evaluation-20260914.md` and the frozen
criteria are in `task-receipts/self-review-routing-synthesis-20260914.md`. I reran the live scorer
at `2026-09-14T17:20:12Z`. It exited 0 with `candidates=0 excluded=0`, decision `collecting`,
`elapsed_days=0.0195`, and `eligible_tasks=0` in both baseline and shadow. Its source was
`/home/mesh-home/.mesh/chat.log`, 64,804 lines, 55,545,560 bytes, zero malformed task events,
SHA-256 `5f5042d27a4cd6fab4b42d692898de772ce342ca5f011a83652e03ffc57ed199`. The emitted report at
`/home/mesh-home/.mesh/self-review-routing-shadow/reports/routing-shadow.jsonl` has SHA-256
`2af04d0bb3569a42ba9b66eb374f8ed474975cca5e77d80b0af9a0be0858e5e3`.

The scorer's nine fixture tests pass. The scorer is deliberately read-only and manual under the
frozen protocol. No mesh-owned implementation or registration can make the real duration pass
sooner; inventing or relabeling tasks to reach 100 would contaminate the sample. The independent
prerequisites are already present: the scorer, its fixture suite, the frozen criteria, and the
running trial. The primary evaluator remains blocked on the exact external event above. Resolver
history shows the prior witness attempts rejected; no active exact witness resolver remained at
the latest status check, so I created no duplicate resolver or premature comparison task.

## Verification and next action

- `scripts/mesh-task-routing-shadow` — exit 0; collecting, zero candidates.
- `python3 tests/test-mesh-task-routing-shadow.py` — 9 tests passed.
- `mesh-task status self-review-routing-shadow-20260914` — evaluator remains blocked on the frozen
  external-event gate.
- Do not run the comparison before the gates. At `2026-09-28T16:52:06Z`, inspect the live sample;
  if it has at least 100 eligible tasks, create a fresh witness-owned comparison task linked to
  this evidence and the rejected history. Otherwise continue collecting and perform the terminal
  INCONCLUSIVE review no later than `2026-10-14T16:52:06Z`.
