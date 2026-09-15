# Witness open-unowned reconciliation — 2026-09-08

At 2026-09-08T11:53Z, `~/.mesh/tasks.journal` replayed PASS with 19
`OPEN_UNOWNED` rows. Each row is structurally still `status=open`; `dispatch=sent`
is delivery evidence only and does not prove an owner `[taking]` transition.

## Disposition

- `job-interview-intake-20260908/answer-direct-questions-and-source-interviews`:
  owner prose says done using a shorthand key; exact structured closure is missing.
- `recreated-rejected-20260908-08/plans-sound-collage` and
  `recreated-rejected-20260908-09/spec-sound-pane-records`: owner terminal prose
  exists under shorthand keys; exact structured closure is missing. The latter
  is a rejection because cadence conformance remains unresolved.
- `recreated-rejected-20260908-12/freeze-independent-repository-sample` and
  `recreated-rejected-20260908-17/select-real-mesh-use-case`: owner rejection
  evidence exists, but exact structured terminal transitions are missing.
- Recreated haunt steps 13–16, the genome voice-forgery correction, the haunt
  prerequisite, token recorder, four successful health warnings, and both
  autoland steps have no owner `[taking]` evidence in the current exact key.
- `health-warning/25d17bc908dbe3b61fe4/triage` has `dispatch=failed`; it requires
  a fresh dispatch before owner receipt can exist.

## Required closure rule

For every row above, the exact chain/step key must receive owner-authored
`[taking]`, then artifact-backed `[done]`, or a typed `[blocked]`/`[rejected]`
with a concrete reason. Dispatch, shorthand task prose, silence, or an adjacent
task's terminal record is not accepted as closure.

Verification snapshot: `mesh-task audit` and `mesh-task journal` replay PASS;
live pane windows for job, tg, haunt, genome, and health exist; exact owner
chases and the failed-health redispatch are the next board actions.

## Live result

After exact-key owner routing and the failed-health redispatch:

- 17 rows reached terminal `DONE` or `REJECTED`/typed `BLOCKED` state, including
  the shorthand-key corrections for job, tg, and haunt.
- The health warning family is no longer `OPEN_UNOWNED`: five rows are typed
  `BLOCKED` with explicit external/dependency retry events.
- At 2026-09-08T11:58:29Z, the remaining findings are exactly two rows:
  `hire-ledger-correction-prereqs-20260908/03-haunt-tinyfleet-receipt` and
  `autoland-recreated-rejected-20260908-01/land-unit-5-canary`. Both still have
  `status=open`, `dispatch=sent`, and no exact owner `[taking]`; the other
  autoland row is now `RUNNING` under genome.

Final verification: `mesh-task-journal` replay PASS (`37417/37417`, zero source
errors); `mesh-task audit` reports `chain_steps=274`, `findings=2`, and the two
rows above. The goal remains open until those two receive exact owner terminal
or typed blocked transitions.

## Closure verification

At 2026-09-08T11:59Z, both previously remaining rows received exact owner
`[taking]` receipts. The autoland row subsequently reached `DONE` with its
artifact; the haunt prerequisite is `RUNNING` with lease through
2026-09-08T12:29:09Z. A fresh `mesh-task-journal` rebuild and `mesh-task audit`
now report zero `OPEN_UNOWNED` rows. Every dispatched current row is therefore
either `RUNNING`, `QUEUED`/dependency-waiting, terminal, or typed `BLOCKED`;
none is being treated as started merely because it was dispatched.
