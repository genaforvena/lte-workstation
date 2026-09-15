# Health warning triage — witness task dispatch check

Task: `health-warning/302a03775c847ac58e96/triage`  
Source event: 2026-09-14T06:20:35Z `witness-task-autonomy` health failure  
Artifact time: 2026-09-14T06:32Z

The warning row reports `source=PASS`, `dispatchable=6`, `checks=6`, and one error:
`check-20260914T040000Z-060000Z/analyze-observation-for-health-rc-2`.

I checked the exact health-owned observation task in this turn before taking it:
`mesh-task check dispatch 20260914T040000Z-060000Z/analyze-observation health` returned 0. The
owner-authored `mesh-task take` then returned 0; the board records `[taking]` at 06:20:50Z and the
ledger records that task active at 06:20:54Z. Its receipt is now complete at
`docs/task-receipts/health-observation-analysis-20260914T040000Z-060000Z.md`.

The warning is not reproducible as an eligibility refusal for the row: its direct pre-take check
passed, and the next retained autonomy run at 06:25:14Z reports `health=PASS`, `active=1`,
`dispatchable=5`, `checks=5`, and `errors=none`. The autonomy source runs a separate global queue
read followed by exact-owner checks, so its failed check could reflect a transient queue/ledger
observation; the retained evidence does not establish the precise race. I found no separate active
prerequisite task or repeated failure to justify a code follow-up. No task was taken on another
owner's behalf, and no task code or mesh substrate was changed for this warning.

## Verification

- Exact dispatch check before take: exit 0; owner take: exit 0.
- Read the warning row and structured ledger transitions for the observation task.
- Read the next `/home/mesh-home/.mesh/witness-task-autonomy.log` run at 06:25:14Z: PASS,
  `errors=none`.
- Read `scripts/mesh-witness-task-autonomy` and `scripts/mesh-task` check semantics to distinguish
  candidate validation from task claim state.

Disposition: close as a transient, non-reproduced check error; watch for recurrence through the
existing autonomy health stream.
