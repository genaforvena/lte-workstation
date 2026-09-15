# dispatch-rejected-successors-20260909 / repair-recovery

Recorded 2026-09-09. The four named chains were live at inspection: each had a
rejected current predecessor and open successor rows excluded by `queue
--dispatch`. Rejection history and task IDs are retained.

## Supported recovery commands

The command requires the exact successor owner (`MESH_TASK_ACTOR`), an existing
artifact, and a non-empty reason. It accepts only the first successor after the
rejected current step:

```sh
MESH_TASK_ACTOR=genome scripts/mesh-task recover coordination-hledger-plan-20260908 background-recovery reactivate docs/task-receipts/coordination-hledger-identity-20260908.md "owner-normalization repair artifact verifies retained IDs and exact-owner route"
MESH_TASK_ACTOR=genome scripts/mesh-task recover witness-live-unattended-followup-20260908 repair-ideas-queue-duty-routing reactivate docs/witness-live-unattended-followup-owner-correction-20260908.md "owner-correction artifact verifies queue-duty routing repair"
MESH_TASK_ACTOR=haunt scripts/mesh-task recover tinyfleet-applications-20260908 support-routing hold /home/mesh-home/tiny-fleet/docs/task-receipts/A02-verification.md "verification predecessor remains unresolved; hold downstream application work"
MESH_TASK_ACTOR=operator scripts/mesh-task recover coordination-hledger-identity-human-20260908 phone-authorized-keys-recheck hold docs/task-receipts/dispatch-rejected-successors-20260909-repair-recovery.md "operator identity prerequisite remains unresolved; hold human-dependent work"
```

`reactivate` records `[recovered]`, reopens only that successor, and dispatches
it to its exact owner. `hold` records `[held]`, marks the successor blocked,
and does not dispatch it. Replaying the identical command is idempotent; a
different artifact/reason, wrong owner, non-first successor, missing artifact,
or non-rejected chain is refused. No action automatically accepts a failed
verification.

## Live actions and remaining owner receipts

The two genome-owned repairs above were executed and produced durable ledger
records. The haunt and operator rows remain held for their actual owners to
execute the commands above; this mind did not impersonate either owner.

Verification artifacts:

- `scripts/mesh-task --test` — focused regression suite PASS.
- `scripts/mesh-task audit` — terminal-predecessor successors are rendered as
  `HELD_REJECTED` until explicitly recovered or held.
- `scripts/mesh-task-journal` — accepts the new audit state and publishes the
  task-only pane view.

