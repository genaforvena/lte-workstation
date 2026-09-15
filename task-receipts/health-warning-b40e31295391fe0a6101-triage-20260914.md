# Health warning triage: one-run task-witness dispatch refusal (b40e3129)

Task: `health-warning/b40e31295391fe0a6101/triage`  
Observed warning: 2026-09-14T09:57:20Z, `mesh-witness-task-autono@mesh-home`.

The warning followed a single dispatch check refusal for
`health-warning/771bea8c48c6b750fc22/triage`. That exact parent triage has now completed with an
artifact-backed disposition: the held Telegram composer was already clear and the matching
autoland follow-through was completed by TG after the operator replied. The parent receipt is
[`health-warning-771bea8c48c6b750fc22-triage-20260914.md`](health-warning-771bea8c48c6b750fc22-triage-20260914.md).

I inspected the task eligibility code and canonical task ledger. `mesh-task check dispatch` returns
2 when the exact row is no longer open/eligible or when the owner already has an active task; this
is a refusal, not a missing task. The current parent state is complete. The live one-shot witness
at 10:35:52Z returned `health=PASS source=PASS`, `checks=3`, `errors=none`; this is recorded in
`/home/mesh-home/.mesh/witness-task-autonomy.log`. An adjacent 10:35:11Z run failed on three other
exact rows, so this PASS is not a claim that every witness issue is gone.

Disposition: this historical refusal is currently unreproduced and its named parent is resolved.
No task-check semantics or witness code change is supported by this one event. Retry triage if a
fresh witness warning names the same refusal after confirming that the exact owner has no active
task, or if a current witness run fails on this row.

Evidence: `/home/mesh-home/.mesh/chat.log` (warning and owner-authored parent completion),
`scripts/mesh-task` (`check_eligibility` and active-owner gate),
`task-receipts/health-warning-771bea8c48c6b750fc22-triage-20260914.md`, and the live witness tape
above.
