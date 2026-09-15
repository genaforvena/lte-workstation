# Coordination solution audit — 2026-09-12

Task: `design-spec-task-sweep-20260907/audit-coordination-sol` (claimed by `tg` after an exact-owner dispatch check).
Source: `docs/coordination-audit-sol-20260907.md`.

## Reconciliation

| Proposed solution | Implementation task and artifact | Current disposition |
|---|---|---|
| P0-A: stop targeted acknowledgement echoes; suppress duplicate ACK delivery; bound retries and preserve actual attempt/expiry evidence | Protocol: `docs/pushed-fact-ack-protocol-20260907.md`. Delivery audit: `witness-mesh-chat-deliver-sweep-20260908/delivery-audit` and `.../unattended-warning-sweep`, both done. Misleading-attempt-field repair: `witness-mesh-chat-delivery-attempts-correction-20260908/fix-attempts-field`, done by genome; implementation artifact is `scripts/mesh-chat-deliver`. Regressions: `tests/test-mesh-chat-deliver.sh`, `tests/test-mesh-chat-deliver-attempts.py`. | **Implemented and wired.** Terminal ACKs are not re-enqueued; retries and per-message attempts are covered, with age expiry distinguished. Current source and deployed hashes both `d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd`; cron runs the deployed path every minute and cron is active. The 2026-09-08 re-verification's “correction still open” statement predates the completed corrective task. |
| P0-B: one keyed lifecycle for operator-originated multi-turn work, with exact ownership, progress/lease, typed blocks/resume, handoff recovery, and artifact-backed closure | Ledger boundary: `docs/coordination-task-ledger-sync-20260907.md`, implementation in `scripts/mesh-task`; current plan audit: `docs/design-audit-task-ledger-sync-20260912.md`. Single-source decision and implementation: `task-only-coordination-20260908/task-only-coordination` (done), artifact `docs/task-only-coordination-20260908-wake.md`; lifecycle contract: `docs/operator-task-lifecycle.md`. | **Lifecycle path implemented; accounting agreement unresolved.** The current `mesh-task` queue is the dispatch authority, and task journal is replayed from `chat.log`. Focused lifecycle checks passed below. However, the latest `mesh-promises --check` returned 1: parity passed, but replay open-count was 247 versus hledger 0. The task-ledger audit independently records a similar default-journal mismatch. Do not treat task lifecycle tests as proof that the accounting projection is healthy. |
| P0 case reconciliation: adint, Tiny Fleet, and job | adint: existing `self-adint-expansion/operator-gated-release` and device-capture block, reconciled in `docs/design-audit-self-adint-expansion-20260912.md`. Tiny Fleet: `tinyfleet-promise-gaps-20260912` and `tinyfleet-operator-ideas-20260912`, reconciled in `docs/design-audit-tinyfleet-operator-promises-20260912.md`. Job: keyed intake implementation `ask-answer-funnel-implementation-20260907` is complete (6/6); job lane evidence is `docs/job-autonomy-audit-20260907.md`. | **Partially closed with explicit follow-ups.** adint's device export remains blocked on operator-provided CSV/path/device label; its release task remains open. Tiny Fleet's two newly registered exact-owner promise-gap tasks remain open under genome. The job lane audit covers action handling, but this pass did not find artifact-backed reconciliation of the original ten keyed operator asks; `design-audit-task-sweep-20260907/design-audit-job-and-sync` remains open. |
| P1: independently verify code path and live wiring, not just self-tests | Current delivery and task dispatch code, focused tests below, source/deployed identity, cron/reflex configuration. | **Code and wiring checks pass for the sampled paths; full coordination is not green.** Delivery, `mesh-task`, `mesh-dispatch`, `mesh-mind-control`, and `mesh-task-journal` source hashes match their installed paths. Dispatch and task-journal reflexes are present. The unresolved accounting mismatch above remains a live verification failure. `docs/design-audit-ledger-driven-task-dispatch-20260912.md` also documents `tests/test-mesh-dispatch-hledger-gate.sh` as stale against the tasks-only architecture; it is not represented as a passing test here. |

## Verification performed

- `mesh-task check dispatch design-spec-task-sweep-20260907/audit-coordination-sol tg`: exit 0; then claimed by `MESH_TASK_ACTOR=tg`.
- `scripts/mesh-chat-deliver --test`: PASS.
- `tests/test-mesh-chat-deliver.sh`: PASS (bounded retry, terminal ACK, duplicate suppression, fresh-ID reopen).
- `tests/test-mesh-chat-deliver-attempts.py`: PASS (grouped 0/1/2/3 attempt mapping; age expiry distinct).
- `tests/test-mesh-task-ledger-sync.sh`: PASS.
- `tests/test-mesh-task-dispatch-receipt.sh`: PASS.
- `tests/test-mesh-task-handoff-reset-instruction.sh`: PASS.
- `tests/test-mesh-task-source-coverage.sh`: PASS (all source records replayed and hashed).
- `mesh-task --test`: PASS; `scripts/mesh-dispatch --test`: PASS.
- Installed `mesh-chat-deliver --test`: PASS; cron active and delivery entry present.
- `mesh-promises --check`: **FAIL**, parity PASS, agreement FAIL (`replay=247 != hledger=0`).

## Remaining work

1. Create or identify an owner-assigned implementation task to trace and repair the default `mesh-promises` journal mismatch; rerun feed/check only after the writers settle.
2. Preserve the existing adint operator-input block and the two Tiny Fleet follow-ups; do not infer closure from adjacent work.
3. Complete the open job-and-sync audit against the original keyed asks and cite any remaining exact implementation tasks.

No substrate operation or unrelated worktree change was made by this audit.
