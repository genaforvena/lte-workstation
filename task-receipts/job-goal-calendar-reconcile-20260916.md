# Job calendar reconciliation — 2026-09-16

## Evidence

- `mesh-job-cal --agenda --json` returned the valid JSON value `[]` (zero durable agenda rows).
- `awk -F '\t' 'NR>1 && $5=="interview"' ~/.mesh/job-board.tsv` returned 24 board rows.
- Therefore 24 board rows labelled `interview` have no corresponding durable calendar evidence.

## Disposition

No calendar row was added: the board notes do not establish a confirmed date/time, participants,
and exactly one link/place for these rows. Inventing those fields would violate the job charter.
The safe next action is to reconcile each employer confirmation through the live employer channel,
then use `mesh-job-cal --confirm` only with complete source-backed fields.
