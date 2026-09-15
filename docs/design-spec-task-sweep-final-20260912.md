# Design/spec sweep — final verification, 2026-09-12

## Scope and result

The two source manifests are `docs/plans/2026-09-07-design-audit-task-sweep.tsv` (18 rows) and
`docs/plans/2026-09-07-design-spec-task-sweep.tsv` (25 rows). The canonical `mesh-task replay --json`
records map all 43 manifest slugs to task promises with non-empty owners. Each completed row has a
non-empty terminal result and an artifact path that exists. The three manifest rows whose original
owner differs from the current canonical record were transferred to `wake`: audit `plans-window-lease`
and spec `spec-clear-on-claim` / `spec-hledger-coordination` (the spec manifest records `tg` for both).

The audit-sweep row matrix and its per-row artifact links are in
[`design-audit-task-sweep-final-20260912.md`](design-audit-task-sweep-final-20260912.md). The table
below records the spec-sweep task promise, current owner, terminal audit disposition, and evidence
artifact. `DONE` closes the audit task; a result may explicitly leave implementation or a separate
follow-up open, as shown in the disposition column.

## Spec-sweep row matrix

| Step / promise key | Owner | Task disposition | Artifact | Explicit final result |
|---|---|---|---|---|
| `spec-ask-answer-funnel` | tg | DONE | `docs/ask-answer-funnel-dispositions-20260907.md` | Units 1–4 remain open as implementation tasks; Unit 5 is deferred by design. |
| `spec-model-swap` | tg | DONE | `docs/design-spec-model-swap-20260907.md` | Marked-line STT swap and restore path verified, including consumer resolution. |
| `spec-models-channel` | tg | DONE | `docs/design-spec-models-channel-20260907.md` | Obligation-to-evidence map complete; restore condition and repository push remain explicit follow-up boundaries. |
| `spec-sound-pane-records` | tg | DONE | `docs/design-spec-sound-pane-records-20260907.md` | Cadence resolved against the approved */10 change; tests, wiring, and fresh reflex artifact verified. |
| `spec-sound-collage` | tg | DONE | `docs/design-spec-sound-collage-20260912.md` | Source/deployed parity, live cron, and two decoded MP3 artifacts verified. |
| `spec-crash-recovery` | tg | DONE | `docs/design-audit-crash-proof-recovery-20260912.md` | P1/P2 verified; P3 has no runtime wiring; P4 remains explicitly unperformed pending an isolated shadow window. |
| `spec-mind-recycle` | tg | DONE | `docs/design-audit-mind-recycle-20260912.md` | Audit and tests complete; policy measurement remains a separate task, and existing shadow is not claimed. |
| `spec-uxn-predicate` | tg | DONE | `docs/audits/uxn-predicate-design-audit-20260912.md` | Implementation drift and body-power wiring/parser gaps recorded as open. |
| `spec-clear-on-claim` | wake | DONE | `docs/design-audit-clear-on-claim-20260912.md` | As-built trigger audited; old spec marked historical; first-claim-after-idle remains an open design boundary. |
| `spec-hledger-coordination` | wake | DONE | `docs/design-audit-hledger-reactive-coordination-20260912.md` | Task-only authority verified; prior hledger-reactor architecture marked superseded. |
| `spec-promise-writeoff` | tg | DONE | `docs/design-audit-promise-writeoff-20260912.md` | Components A–D remain in scope; implementation chain and accounting distinction recorded. |
| `spec-witness-labour` | tg | DONE | `docs/design-spec-witness-labour-20260912.md` | Audit complete; promise footer and fused-pane integration remain unresolved in the artifact. |
| `audit-labour-trigger-cron` | tg | DONE | `docs/design-audit-labour-trigger-cron-20260912.md` | Findings reconciled; superseded detector declined; current no-work wake correction verified. |
| `audit-genome` | tg | DONE | `docs/design-audit-genome-20260912.md` | Historical drift rechecked; two genome repairs opened; dependency edges deferred until that row is current. |
| `audit-coordination-sol` | tg | DONE | `docs/design-audit-coordination-solution-20260912.md` | Proposals reconciled to implementation tasks; live journal mismatch and case follow-ups remain explicit. |
| `audit-coordination-result` | tg | DONE | `docs/design-audit-coordination-result-20260912.md` | Prior timeout superseded by a passing keyed rerun; unrelated status-tagged follow-ups remain open. |
| `audit-record-button` | tg | DONE | `docs/design-audit-record-button-20260912.md` | Delivery and push verified in the sibling repository; the explicit operator defer gate remains. |
| `audit-adfox` | tg | DONE | `docs/design-audit-adfox-20260912.md` | Prior-art collision reconciled; evidence-only follow-up opened; no new collection. |
| `audit-tg-intake` | tg | DONE | `docs/design-spec-audit-tg-intake-20260912.md` | Intake/dispatch closed; semantic-coverage and isolated acceptance evidence remain open in a successor. |
| `audit-tg-layout` | tg | DONE | `docs/tg-scripts-layout-migration-audit-20260912.md` | Current tree reconciled; exact-owner migration chain verified; no file moves made. |
| `audit-ledger-coverage` | tg | DONE | `docs/design-audit-ledger-coverage-20260912.md` | Intake bypass and ideas-queue findings closed; stale intake key/summary cleared; remaining asks stay open. |
| `audit-job-autonomy` | tg | DONE | `docs/job-autonomy-recheck-20260912.md` | Wiring and parity verified; HH apply/reply checks exposed a down driver and reply-path follow-up. |
| `audit-repo-sync` | tg | DONE | `docs/repo-sync-recheck-20260912.md` | Fresh fetches and repo states recorded; prism divergence, timeouts, and root dirtiness remain explicit. |
| `audit-vsm-scheduler` | tg | DONE | `docs/design-audit-vsm-scheduler-20260912.md` | Cron audit verified; missing live auditor caused the runtime follow-up now recorded at `docs/vsm-scheduler-runtime-followup-20260912.md`. |
| `final-design-spec-verification` | tg | ACTIVE while this receipt is written; close with this artifact | `docs/design-spec-task-sweep-final-20260912.md` | All manifest rows reconciled; the final task transitions to DONE after this artifact is registered. |

## Live ledger and promise verification

- `mesh-task status design-audit-task-sweep-20260907`: 18/18 DONE; every row has a ledger owner and existing artifact.
- `mesh-task status design-spec-task-sweep-20260907`: 24 DONE plus this active final-verification step before close; all 25 manifest slugs map to ledger steps.
- `mesh-task audit` exited 0. The filtered audit contained all 18 audit-chain and 25 spec-chain rows; unrelated global OPEN_UNOWNED, BLOCKED, and OVERDUE rows remain outside these chains.
- `mesh-promises --feed` exited 0. Its compatibility journal snapshot reported `open=201`, `kept=1982`, and the existing unrelated unrouted liabilities.
- `mesh-promises --check` exited 0: parity and replay/balance agreement passed for promises (201/201), claims (149/149), holds (62/62), and asks (66/66). The report still lists 5 unrouted promises, 142 unrouted claims, and 5 unrouted holds; none is one of the 43 sweep tasks.
- Every completed row has a non-empty task result and an artifact file with an explicit disposition/status/decision in its text. The one audit-owner transfer and two spec-owner transfers are shown with their current canonical owner above and in the audit matrix.

This closes the final spec-sweep audit row. It does not claim that every underlying design implementation is complete: each row's artifact preserves its own PASS, OPEN, BLOCKED, DECLINED, or SUPERSEDED outcome and any successor obligation.
