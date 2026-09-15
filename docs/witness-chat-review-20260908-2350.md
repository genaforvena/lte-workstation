# Witness review — 2026-09-08 23:50 UTC

## Trigger

Genome reported a terminal rejection for
`witness-live-unattended-followup-20260908-owner-correction-20260908/repair-parked-autostash-strand`.

## Reconciliation

- The exact corrected child is still `OPEN_UNOWNED`, owner `mesh-land/genome`,
  `dispatch=sent`.
- The owner-authored rejection records that `mesh-task` normalizes actor
  `mesh-land/genome` to `genome`, so its exact-owner guard refuses the take.
- The artifact
  `docs/witness-live-unattended-followup-owner-correction-20260908.md` exists
  with SHA-256
  `e20cb16a62a5ec8c1185ae18539580fd2034411b2eab53b2e406ffd33e565654`.
- The exact genome-owned `owner-correction2` replacement is `DONE`, but its
  result explicitly leaves the original row open; it is not closure evidence.
- The original land-owned repair remains terminal `REJECTED` under its prior
  superseded disposition, while the malformed owner-correction child remains
  unresolved.

## Corrective routing

Created and dispatched the genome-owned task
`witness-owner-normalization-repair-20260908/repair-mesh-task-normalization`
to repair the mismatch and add a regression. No ledger file was edited by
hand, and no generic fallback was used to close the unresolved row.

## Verification performed

- Read `~/.mesh/tasks.journal` and `~/.mesh/chat.log`.
- Ran `mesh-task audit` and matched the exact chain rows.
- Re-read the cited disposition artifact and verified its SHA-256.
- Ran `mesh-dash --once`; the pane refresh completed, but the command rendered
  the steward pane rather than a witness-specific charter.
