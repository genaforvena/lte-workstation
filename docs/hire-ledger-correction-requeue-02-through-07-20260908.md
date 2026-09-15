# Hire ledger correction: requeue 02 through 07

Verified 2026-09-08 against the deployed `/home/mesh-home/.local/bin/mesh-task`.
The previous six chains remain immutable terminal `REJECTED` history. Corrected
replacement chains were created separately and each was taken, typed-blocked, and
returned to the queue with `mesh-task wait-for`.

## Exact prerequisite mappings

| former row | corrected replacement | exact prerequisite |
|---|---|---|
| recreated-rejected-20260908-02/delivery-repair | recreated-rejected-20260908-02-corrected/delivery-repair | recreated-rejected-20260908-02-genome-canary/delivery-canary |
| recreated-rejected-20260908-03/workspace-repair | recreated-rejected-20260908-03-corrected/workspace-repair | hire-ledger-correction-prereqs-20260908/03-haunt-tinyfleet-receipt |
| recreated-rejected-20260908-04/charter-repair | recreated-rejected-20260908-04-corrected/charter-repair | hire-ledger-correction-prereqs-20260908/04-current-charter-fixture |
| recreated-rejected-20260908-05/test-isolation-repair | recreated-rejected-20260908-05-corrected/test-isolation-repair | hire-ledger-correction-prereqs-20260908/05-bounded-test-fixture |
| recreated-rejected-20260908-06/evidence-repair | recreated-rejected-20260908-06-corrected/evidence-repair | hire-ledger-correction-prereqs-20260908/06-durable-evidence-receipt |
| recreated-rejected-20260908-07/empty-pane-repair | recreated-rejected-20260908-07-corrected/empty-pane-repair | hire-ledger-correction-prereqs-20260908/07-bounded-health-sound-read |

## Audit rows

The deployed `mesh-task audit` returned these rows after all six `wait-for`
transitions:

```text
QUEUED hire recreated-rejected-20260908-02-corrected/delivery-repair waiting_for=recreated-rejected-20260908-02-genome-canary/delivery-canary dispatch=waiting
QUEUED hire recreated-rejected-20260908-03-corrected/workspace-repair waiting_for=hire-ledger-correction-prereqs-20260908/03-haunt-tinyfleet-receipt dispatch=waiting
QUEUED hire recreated-rejected-20260908-04-corrected/charter-repair waiting_for=hire-ledger-correction-prereqs-20260908/04-current-charter-fixture dispatch=waiting
QUEUED hire recreated-rejected-20260908-05-corrected/test-isolation-repair waiting_for=hire-ledger-correction-prereqs-20260908/05-bounded-test-fixture dispatch=waiting
QUEUED hire recreated-rejected-20260908-06-corrected/evidence-repair waiting_for=hire-ledger-correction-prereqs-20260908/06-durable-evidence-receipt dispatch=waiting
QUEUED hire recreated-rejected-20260908-07-corrected/empty-pane-repair waiting_for=hire-ledger-correction-prereqs-20260908/07-bounded-health-sound-read dispatch=waiting
```

The existing 02 prerequisite was confirmed present and `QUEUED` as
`recreated-rejected-20260908-02-genome-canary/delivery-canary`. The five new
prerequisite tasks were also created in
`hire-ledger-correction-prereqs-20260908`.
