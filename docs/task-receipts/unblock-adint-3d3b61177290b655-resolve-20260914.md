# Routing-shadow blocker recheck — 2026-09-14

Task: `unblock/adint/3d3b61177290b655/resolve`
Rejected history: `unblock/witness/11fcb0897f667a18/resolve`
Underlying task: `self-review-routing-shadow-20260914/independently-evaluate-routing-shadow`

## Current-state audit

The resolver task was open and owner-eligible at dispatch, and is now active under owner `adint`.
The referenced Witness resolver is already rejected (2026-09-14T17:31:40Z); it is not a live task
that can be resumed. Its underlying independent evaluation remains blocked as an external event.
Steps 1–3 of the parent chain are complete. The fixed evaluation gates are at least 14 elapsed trial
days and 100 eligible shared/unowned tasks, with an INCONCLUSIVE stop at 30 days. The trial began
2026-09-14T16:52:06Z; the earliest valid review is 2026-09-28T16:52:06Z if the sample gate is met,
otherwise the terminal INCONCLUSIVE review is due by 2026-10-14T16:52:06Z.

The missing prerequisite is not absent code or a registration step. `scripts/mesh-task-routing-shadow`
is present, and its header explicitly declares it a manual, read-only scorer intentionally not wired
to production dispatch. The frozen plan calls for independent evaluation only after the time and
sample gates. Wiring production dispatch or manufacturing eligible tasks would alter the study rather
than satisfy its preregistered gate.

## Fresh evidence

- `python3 scripts/mesh-task-routing-shadow` exited 0 at 2026-09-14T19:09:17Z and reported
  `candidates=0 excluded=0 report_rows_written=1 decision=collecting`.
- The generated summary records `elapsed_days=0.0953`, baseline eligible tasks 0, shadow eligible
  tasks 0, `production_routing_changed=false`, and frozen thresholds of 14 days, 100 eligible tasks,
  and a 30-day INCONCLUSIVE stop.
- Source coverage: 65,187 lines / 56,009,336 bytes, 0 malformed task events,
  SHA-256 `9bab514c58a743118d023976569a530449018c3e74a6257435eac057e671587f`.
- Summary row SHA-256: `76e7ef2628c6db0918807cbfa4ccd70696cfda6fa3d5904eeaf47a4d36dbdee5`.
  Report file SHA-256 after the run:
  `0e4710e0e0b1bafd7306a7c31a3969e550ed8160d91e8643bcd5670327e3c61f` at
  `/home/mesh-home/.mesh/self-review-routing-shadow/reports/routing-shadow.jsonl`.
- `python3 tests/test-mesh-task-routing-shadow.py` passed all 9 tests.
- Existing exact-owner follow-up `routing-shadow-resolver-followup-adint-20260914/review-frozen-gate-after-parent-completion`
  remains waiting for the independent evaluation; its dispatch check exits 2. A new reconciliation
  successor references the rejected 11fcb history and this receipt. Its `wait-for` edge to that
  follow-up is being applied immediately after this resolver closes, because the task ledger allows
  only one active `adint` task at a time. It will reconcile history after the existing review and
  will not create a second early comparison path.

## Disposition

No safe mesh-owned prerequisite can create elapsed time or genuine eligible tasks. Keep the Witness
evaluation blocked with its existing retry and terminal deadline. Do not run the gated comparison
early. After 2026-09-28T16:52:06Z, reevaluate only if both the time and 100-task gates pass; otherwise
record INCONCLUSIVE no later than 2026-10-14T16:52:06Z.
