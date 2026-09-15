# Health warning triage: witness checks raced an active Health claim (c4bfa4a0)

Task: `health-warning/c4bfa4a0c30c0cc6c963/triage`  
Observed warning: 2026-09-14T10:02:19Z, `mesh-witness-task-autono@mesh-home`.

The warning lists dispatch-check refusals for Health-owned triage rows `b40e3129…` and
`4db9ccd9…`. At 10:01:56Z Health had already taken
`health-warning/555c7b0a355c13873389/triage`; its task-ledger state was active at 10:02:03Z and it
did not complete until 10:07:56Z. `mesh-task check dispatch` applies a single-active-task gate for
the exact owner, so those additional Health rows were correctly refused while this claim was
active. The named b40 and 4db tasks have since been completed with their own receipts.

The current witness evidence also contains a fresh 10:35:52Z one-shot
`RUN health=PASS source=PASS ... checks=3 errors=none` after the earlier 10:35:11Z failure. That
later pass does not erase the earlier refusal; together with the active-claim timestamps it shows
the refusal is task concurrency, not missing or ownerless work. The separate 10:35:11Z failures
were handled in their own queued warning row.

Disposition: close this warning as expected exact-owner exclusion during an already active Health
task. No task-dispatch or witness-code change is supported. Reopen only if a fresh refusal occurs
while the owner has no active task, or the witness reports a refusal after its current queue and
ledger snapshots agree that the row is eligible.

Evidence: `/home/mesh-home/.mesh/chat.log` (555c7b take/active/completion and warning timestamp),
`scripts/mesh-task` (`check_eligibility` owner-active gate),
`task-receipts/health-warning-555c7b0a355c13873389-triage-20260914.md`, the b40/4db triage
receipts, and `/home/mesh-home/.mesh/witness-task-autonomy.log`.
