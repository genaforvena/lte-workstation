# Ledger coverage and promise-status reconciliation — 2026-09-12

Task: `design-spec-task-sweep-20260907/audit-ledger-coverage` (owner `tg`).
Sources: `docs/ledger-coverage-audit-20260907.md` and
`docs/coordination-promises-status-20260907.md`.
Live checks below were run on 2026-09-12 between 05:19Z and 05:28Z. This artifact
supersedes their dated snapshots for current status; it does not retroactively change
their historical observations.

## Ledger-coverage findings

| Finding | Current evidence | Disposition |
|---|---|---|
| The 2026-09-07 14:50 operator scripts-audit ask bypassed intake. | `tg-operator-scripts-audit-20260907` is complete 1/1 with `docs/tg-operator-scripts-audit-intake-20260907.md`. The related `tg-scripts-layout-audit-20260907` is complete 3/3, including inventory/map/result artifacts. | **Intake and decomposition repaired.** Downstream work remains open: `tg-intake-coverage-followup-20260912` has two open Genome-owned steps; `tg-scripts-layout-migration-20260912` is open 1/9, Genome-owned, with eight later steps queued. These rows are the live follow-up; completion of intake/layout audits does not close implementation. |
| Historical asks were answered by Telegram adjacency without cited dispositions. | The source's 13-row count is stale. Live `mesh-promises --asks` reports 66 open asks, 0 unanswered and 66 answered-but-uncited; `mesh-promises --check` independently agrees at asks replay=66 / hledger=66. `docs/design-audit-historical-asks-20260912.md` handles two distinct historical asks and does not settle this backlog. | **Still open.** Each exact ask key needs an evidence-backed `[done]`, `[design]`, or `[declined]` disposition. Adjacency alone is not closure; do not bulk-close the 66. The exact-key ask ledger remains the current worklist. |
| Autonomous ideas queue entries lacked classification/owners. | `ideas-queue-escalations` is complete 4/4; `docs/ideas-queue-coverage-20260907.md` and `docs/ledger-coverage-followup-ideas-queue-20260907.md` contain the branch dispositions and verification. | **Closed.** The follow-up task and its owner-linked evidence exist; the 2026-09-07 count drift does not reopen that completed chain. |
| The stale `tg-operator-intake-owner` promise remained after the intake task completed. | `tg-operator-intake` is complete; `docs/ledger-reconciliation-20260907.md` and `docs/ledger-clearance-tg-operator-intake-20260907.md` record the exact keyed settlement and checks. Current promise report has no matching `tg-operator-intake-owner` row. | **Closed for this exact key.** No duplicate close is warranted, and this does not assert a globally empty promise ledger. |

The audit's later rechecks add two more reconciliations. The Genome
`ideas-queue-escalations-wifi-rf-disposit` liability was settled with the completed
ideas-queue chain. The scripts-layout frame-scope claim is now covered by the completed
three-step layout audit; its migration work is represented separately by the open
Genome-owned migration chain above.

## Coordination-promises status

The source's stale `RUNNING`/`findings=0` coordination summary was a display-freshness
defect, not a promise-ledger clearance. `docs/coordination-summary-freshness-20260907.md`
records the repair: `mesh-task audit` evaluates leases at read time, the summary writer
rebuilds atomically, and the renderer exposes its timestamp and chain rows. The expired
`witness-ledger-coverage-audit/ledger-coverage-audit` row is now `DONE` against
`docs/coordination-promises-status-20260907.md` in the live task audit. **The stale-row
finding is closed with regression evidence.**

## Current open obligations that remain visible

- `mesh-promises --report` still shows `witness-vpn` as partially discharged, with one
  residual obligation (`leaked historical-promise-drain-vpn…`) owed by `witness`. The
  earlier owner-authored decline closed a different item under the same key. The current
  `mesh-task audit` has no task-chain row for the residual. **Keep it open:** witness must
  either produce evidence for that exact residual or post a specific disposition through
  an owner-held task; do not close it with a generic acknowledgement.
- The current `crypthauntology-kids-followup-20260912` is blocked at `1/3`; one safety gate
  awaits two independent adult approvals, while offline-pilot reconciliation and
  independent release review remain open. These are exact owner-assigned obligations,
  not stale `RUNNING` rows. Preserve the no-live-campaign boundary recorded in
  `docs/design-audit-crypthauntology-kids-20260912.md`.
- The 66 answered-but-uncited asks remain the largest operator-intake backlog. The
  completed historical-ask audit and this design-spec audit do not discharge them; the
  exact-key ask ledger remains authoritative until each disposition is cited.

## Promise-ledger verification and limits

A batch of concurrent `mesh-promises` views briefly returned a holds mismatch
(`replay=60`, `hledger=0`). A later standalone `mesh-promises --check` exited 0 and
reported consistent counts: promises `209/209`, claims `147/147`, holds `61/61`, asks
`66/66`; parity and over-discharge checks passed. The concurrent result was not
reproduced, so this audit does not classify it as a persistent defect or infer its cause.

The passing check still reports roster findings: five unrouted promises, 141 claims
owed by non-roster debtors, and five unrouted holds. Thus accounting replay is
consistent, but the compatibility ledger is not empty and this result does not clear
those independent obligations. The report's 66 uncited asks and residual `witness-vpn`
remain open as stated above.

## Verification performed

- `mesh-task audit`: confirmed the historical witness audit step is done; surfaced the
  open Genome-owned intake-coverage and layout-migration steps, without an owner
  `[taking]` receipt for those current rows.
- `mesh-task status`: scripts-audit `1/1 complete`; scripts-layout-audit `3/3 complete`;
  ideas-queue-escalations `4/4 complete`; intake-coverage `open (1/2)`; layout migration
  `open (1/9)`; crypthauntology follow-up `blocked (1/3)`.
- `mesh-promises --asks`: `66 open`, `0 unanswered`, `66 answered-uncited`.
- `mesh-promises --report`: confirmed the residual `witness-vpn` item.
- Standalone `mesh-promises --check`: exit 0; parity and all four replay/balance counts
  agree, with the roster findings retained above.
- Reviewed each source finding and the current linked closure/follow-up artifacts. No
  source-data, routing, or other substrate configuration was changed by this audit.
