# Health triage ledger reconciliation

- Checked: `2026-09-12T23:50Z` on `mesh-home`
- Corrective task: `health-triage-ledger-reconcile-20260912/reconcile-missing-ledger-completion`
- Source task: `health-warning/504c0323782bea4f8b13/triage`

The source triage remains active because the repeat evidence still shows
`imac-rozalia` offline from `mesh-home`, while the physical state and cause of
the missing peer path remain unknown. The 23:34Z sample and the new 23:48Z
follow-up are recorded in
`docs/task-receipts/health-warning-504c0323782bea4f8b13-triage-20260912.md`.
At 23:50:44Z, the source task ledger row was refreshed against that receipt:
`last_progress=23:50:44Z`, `next_update=2026-09-13T00:05:00Z`, and the next
action is to repeat status/path/UDP after the 23:59Z path-watch pass. The row
remains active with its lease through `00:20:44Z`.

The first take attempt was correctly refused while the source triage occupied
the single active health claim. After the requested repeat sample, the source
triage was completed against its updated receipt with the evidence-bounded
`UNREACHABLE from mesh-home` disposition and the remote-state limitation. The
corrective row was then claimed by `health` and is being settled against this
artifact. The stale progress/deadline mismatch has been reconciled, and the
terminal state now matches the receipt.

The 21:41Z witness correction remains valid: the source row was not overdue at
that time; the concrete issue now corrected was its stale progress/deadline
after the later repeat sample. No network state was changed.

## Verification

Before terminal settlement, `mesh-task audit` reported the source row as
`RUNNING` with lease through `00:20:44Z`; it no longer appeared overdue. The
source ledger then transitioned to `DONE` against the triage receipt. The
corrective row is now `DONE` against this reconciliation artifact; final audit
and `tasks.journal` verification follow that transition.
