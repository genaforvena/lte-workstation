# Witness dispatch coverage repair — 2026-09-08

The operator requires every open promise to reach implementation and completed
work to disappear from the witness worklist. This repair is progress toward that
objective; it does not certify that the outstanding promises are implemented.

## Reproduced defects and changes

- The dispatcher inspected only the first four candidates. At 03:49:15Z its
  live log reported all four held with 47 promises still open; those four were
  genome tasks. The production offer-loop fixture reproduced starvation of an
  available owner behind five busy tasks. The loop now visits the finite open
  queue, stopping at its first delivery. Held attempts remain unsealed and
  available for retry. Existing pacing and ownership gates still apply.
- Witness searched a hyphen-normalized promise key as a literal substring of
  board prose. A `chain/step` owner receipt was missed, while a foreign owner's
  or sibling task's substring could satisfy the check. Receipt matching now
  reads the lifecycle marker, explicit task key (or leading identity), and
  author. Canonical slash and hyphen forms agree; owner and full key must agree.
  An owner yield withdraws start evidence.
- The coordination pane printed every cached audit row, including DONE. It now
  excludes DONE rows while keeping all unfinished rows and the full on-disk
  audit. Installed renderer verification returned zero DONE rows and 133
  unfinished rows. This changes display only, not measurement or settlement.
- The existing failed-ledger regression exposed continued routing after a
  ledger/check failure. Witness now publishes the failed summary and exits
  before routing or task recovery.

## Verification

Observed failing before the corresponding changes:

- `python3 tests/test-dispatch-busy-prefix.py`: offered only busy1 through busy4.
- `bash scripts/mesh-witness-promises --test`: canonical chain receipt missed.
- `python3 tests/test-witness-open-pane.py`: completed task still shown.
- `bash tests/test-mesh-witness-hledger-gate.sh`: dispatch occurred despite failed check.

After repair, all four pass, as do `tests/test-mesh-witness-promises.sh` and
`tests/test-mesh-witness-lifecycle.sh`. Shell syntax and scoped diff checks pass.
The busy-prefix fixture executes the production offer loop with controlled
delivery outcomes; it does not prove live pane delivery. The pane fixture runs
the real renderer in an isolated HOME and checks audit bytes are unchanged.

Installed mesh-witness, mesh-witness-promises and mesh-dispatch resolve to the
edited repository scripts through canonical symlinks. Live witness audit session
21482 exited 0: `audited alerts=2 retry_candidates=34`. The 03:51:19Z dispatch
pass remained PACE-SKIP, so no new live delivery is claimed. Live ledger check
passed parity and replay agreement (47 promises, 5 claims, 28 holds, 45 asks),
with `unrouted:next` still reported. The actual witness.0 pane shows the new
unfinished-steps heading and no DONE rows in its captured frame/scrollback.

## Remaining obligations and next actions

- Check the live audit's exit and the subsequent dispatch log, then obtain the
  selected owner's actual taking receipt and eventual artifact.
- Reconcile all 47 open ledger promises against executable tasks. Live chain
  audit currently has 70 DONE, 113 QUEUED, 18 BLOCKED and 2 RUNNING steps.
  QUEUED or BLOCKED does not prove implementation.
- Recover original task text for older ledger rows whose dispatch payload is
  merely `promise opened: ...`; mesh-board currently searches only retained
  chat.log by timestamp, despite archived promises surviving retention.
- Resolve `unrouted:next` from its original consume-authored event at
  2026-09-07T21:12:19Z with a traceable owner/identity disposition.
- Recheck dependency-blocked chains whose stated prerequisite already has a
  verification receipt. Do not silently equate a typed block with completion.

The full objective remains active.
