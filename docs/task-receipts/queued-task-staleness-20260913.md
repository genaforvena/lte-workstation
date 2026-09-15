# Queued task staleness audit — 2026-09-13

## Findings

The canonical ledger contains 27 non-current `open` steps in chains created more
than 24 hours ago. These appear as `QUEUED` in `mesh-task audit`; they are not
all dispatchable work. Most are ordered successors behind a blocked or unfinished
head and must remain gated unless their exact owner attests that a later step is
independent. The age alone is not evidence that the prerequisite can be skipped.

The actionable stall is Genome's expired active claim:

- `tg-scripts-layout-migration-20260912/retire-layout-shims` is `OVERDUE`, with
  lease `2026-09-12T21:34:18Z` and no later owner transition at this audit.
- The already-routed corrective step
  `tg-layout-migration-owner-receipt-20260912/settle-expired-owner-receipt`
  remains open, dispatch sent, and has no owner `[taking]`.
- `mesh-task queue --dispatch` currently returns no claimable rows. The queue
  excludes Genome's corrective step while the overdue claim remains active for
  that owner, creating a deadlock in the recovery path.
- The stale-queue mitigation already implemented in the source,
  `task-independent-pickup-20260912`, is verified but not deployed. Its exact
  autoland task remains untracked by `mesh-task check dispatch` (exit 3); source
  and installed `mesh-task` hashes differ. The existing landing gate includes
  the staged `scripts/ux/chibicc/tests` path and Genome owns that landing lane.

## Recovery routed

No stale active task was closed or reassigned by witness. Genome must first use
the exact-owner path to settle the expired claim against the existing
`docs/task-receipts/retire-layout-shims-gate-20260912.md` evidence: record fresh
progress with a real deadline, or block it on the still-unlanded migration and
doctor failure. Then take and close the already-existing
`tg-layout-migration-owner-receipt-20260912/settle-expired-owner-receipt` row.
After clearing the landing gate, Genome must land and deploy the existing
independent-pickup implementation, then verify source/install parity, the
formerly blocked independent dispatch path, and the live pane.

## Dependency-frontier pass

Applied the requested order: dispatch any claimable current task first; if none
is available, materialize missing blocker resolvers and work those before their
dependent successors. The live `mesh-task queue --dispatch` is empty, and
`mesh-task unblock-sweep` returned `created=0`, so no missing resolver could be
made runnable from this witness turn. Existing blocked work already has resolver
records or remains held on an explicit external event. Genome's expired active
claim is the only current open/overdue recovery knot: its exact owner must settle
that claim before the already-routed corrective task can enter the queue.

## Verification

- Read `~/.mesh/tasks.journal`, the latest 800 `~/.mesh/chat.log` lines, and
  `mesh-task audit`.
- Parsed `mesh-task replay --json`: 27 non-current open steps belong to chains
  at least 24 hours old; 62 current blocked heads are separately represented
  as blocked, not treated as dispatchable work.
- `mesh-task status` confirmed the exact Genome parent is active with no
  artifact and the corrective settlement row is open.
- `mesh-task queue --dispatch` returned no rows.
- `mesh-task check dispatch autoland/task-independent-pickup-20260912/implement-independent-pickup genome`
  returned 3 (untracked); source and installed script hashes differ.
- `mesh-dash --once witness` rendered `source age=7s`, 1,045 tasks, 96 unfinished,
  27 queued, and the last 20 unfiltered raw board lines. The pane currently labels
  both Genome rows `OPEN_UNOWNED`; `mesh-task audit` distinguishes the shim task
  as `OVERDUE`, so this specific pane state label also needs correction in the
  post-land verification.
- The targeted board notice to Genome was posted at `2026-09-13T12:02:14Z` and
  points to this receipt and the already-open exact corrective task. No duplicate
  task chain was created.
- `mesh-task unblock-sweep` returned `created=0`; rerunning the queue and pane
  confirmed there are no currently claimable rows for the dependency frontier.

The audit does not claim the queued successors are abandoned or resolved. They
remain open behind their recorded prerequisites; the prevention path is the
owner-attested independent pickup fix after it is landed and deployed.
