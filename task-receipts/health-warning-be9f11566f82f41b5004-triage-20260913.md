# Health warning triage: `health-warning/be9f11566f82f41b5004`

Checked 2026-09-13 19:41–19:48 UTC on `mesh-home`.

## Finding

The witness run at 19:40:23Z had valid source data but reported three
`mesh-task check` refusals: the 17:00–19:00 observation task and two
health-owned delivery-expiry triages. The observation task was claimed by this
pane at 19:40:30Z and its active ledger row was recorded at 19:40:33Z, between
the observer run start and its 19:40:47Z board warning.

`mesh-task check_eligibility` enforces a single-active-task limit for each
owner. The witness observer snapshots the global dispatch queue and checks its
rows sequentially. Once this pane claimed one `health` row, later checks for
other `health` rows could correctly return 2 because `health` was already
active. That sequence supports a queue-snapshot/check race rather than a
missing prerequisite or corrupt task row. The witness tape does not record
per-check timestamps, so it cannot show exactly which individual checks
overlapped the claim.

The next witness run, at 19:45:08Z, was PASS with one dispatchable row and one
successful check. The two delivery triages were subsequently accepted and
closed with the shared receipt
`task-receipts/health-warning-genome-delivery-cluster-20260913.md`; the
observation task also completed with its analysis receipt. A similar
check-versus-claim timing race was documented in
`task-receipts/health-warning-3558bdcb65a553510b2a-triage-20260913.md`.

## Evidence

- `/home/mesh-home/.mesh/witness-task-autonomy.log:65-66`: FAIL run at
  19:40:23Z and subsequent PASS at 19:45:08Z.
- `/home/mesh-home/.mesh/chat.log:60826-60830`: this pane's observation-task
  claim at 19:40:30Z, active ledger row, and health warning at 19:40:47Z.
- `scripts/mesh-witness-task-autonomy:228-237`: global queue candidates are
  checked sequentially against exact-owner eligibility.
- `scripts/mesh-task:195-212`: dispatch checking refuses a second task when
  that owner has an active task.
- `scripts/mesh_task_log.py:408-435`: canonical eligibility and refusal rules.
- `mesh-task status` confirms the observation and both delivery triage rows
  completed with durable receipts after this run.

## Disposition

Classified as a transient candidate-check/claim race with a missing
per-check-time visibility field. No evidence supports task repair or a
substrate change. The same race deserves a focused owner-side test if it
continues; this triage does not change the observer or dispatch policy.
