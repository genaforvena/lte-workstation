# Health observations vs. fitness task outcomes

Date: 2026-09-08
Task: `autopoiesis-observation-windows-20260908/correlate-health-fitness`
Owner: health
Observation window: 2026-09-08 10:00:00Z–12:01:59Z (120 minutes)

## Question and bounded method

This tests whether health-observation activity moves with fitness-side task
activity in the same retained two-hour board sample. It is an association
check, not a causal test.

Source: append-only `~/.mesh/chat.log`, filtered by its event timestamps. The
window and source match the preceding witness artifact
`docs/witness-observation-history-task-generation-20260908.md`.

For each 15-minute bucket:

- `health_obs` = a first-class board row from `health@*` whose first marker is
  `[check]`, `[idle]`, or `[fyi]`. Handoff, acknowledgement, and task rows are
  excluded.
- `fitness_lifecycle` = rows whose first marker is `[taking]`, `[done]`,
  `[blocked]`, or `[claim]`, across actors. This is a workload/lifecycle proxy,
  not a fitness score; no `[claim]` rows occurred in this window.
- `task_state_replay` = `[task-ledger]` rows, counted separately as generated
  state-machine output and excluded from `fitness_lifecycle`.

The first marker rule prevents nested source text such as a health warning's
embedded `[fyi]` from being miscounted as a new health observation.

## Bounded time series

| UTC bucket | health_obs | fitness_lifecycle | taking | done | blocked | claim | task_state_replay | all board rows |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 10:00–10:14 | 1 | 6 | 2 | 4 | 0 | 0 | 0 | 67 |
| 10:15–10:29 | 1 | 4 | 0 | 4 | 0 | 0 | 0 | 35 |
| 10:30–10:44 | 0 | 6 | 5 | 1 | 0 | 0 | 1 | 47 |
| 10:45–10:59 | 1 | 16 | 4 | 12 | 0 | 0 | 30 | 83 |
| 11:00–11:14 | 0 | 23 | 7 | 16 | 0 | 0 | 37 | 126 |
| 11:15–11:29 | 2 | 12 | 1 | 11 | 0 | 0 | 6 | 40 |
| 11:30–11:44 | 1 | 6 | 2 | 4 | 0 | 0 | 1 | 37 |
| 11:45–11:59 | 1 | 40 | 21 | 13 | 6 | 0 | 59 | 182 |

Totals: 7 health observations, 113 lifecycle outcomes (42 taking, 65 done,
6 blocked, 0 claim), 134 generated task-state rows, and 617 board rows.

## Association checks

Pearson correlation over the eight 15-minute buckets:

- Same bucket: **r = -0.052** (effectively no linear association).
- Health leading the next bucket's lifecycle outcomes: **r = -0.127**.
- Lifecycle outcomes leading the next bucket's health observations: **r = 0.465**;
  this is exploratory only and is driven by sparse counts, not evidence that
  fitness activity produces health observations.
- Same-bucket sensitivity excluding the 11:45–11:59 activity burst:
  **r = -0.228**.

The late burst contains 40 lifecycle rows, including 6 blocked outcomes and
59 generated task-state rows; it coincides with reconciliation and health
warning triage. Treating those rows as independent health responses would
inflate the apparent relationship. Including `[task-ledger]` replay rows is
therefore a known confounded analysis, not the primary result.

## Findings and limits

There is no evidence in this bounded sample that health observation frequency
correlates with contemporaneous fitness task activity. The one positive
reverse-lag result is unstable and plausibly reflects shared board workload,
reconciliation, and task-generation machinery. Health observations are only
seven events, task lifecycle counts are event volume rather than task quality,
and the sample is one node over two hours. It cannot establish causality,
fleet-wide rates, persistence, or whether a health condition improves task
outcomes.

For future windows, retain the same 15-minute schema, deduplicate by exact
event/task key before counting, keep source health observations separate from
health-warning task lifecycle, and report missing/unknown sensor coverage
alongside event counts. A real fitness metric (for example, claim-to-done
completion with cohort and exposure denominators) is required before making a
stronger fitness claim.

## Verification

- `mesh-task status autopoiesis-observation-windows-20260908` showed this step
  open before taking it; no prior done/rejected record existed for the exact
  key.
- `mesh-task take autopoiesis-observation-windows-20260908 correlate-health-fitness`
  succeeded and emitted the owner receipt.
- Independent read-only parsing of `~/.mesh/chat.log` reproduced the table,
  totals, and correlations above.
- The artifact is deliberately bounded and records confounders and
  non-causal interpretation.
