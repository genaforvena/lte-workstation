# Rejected predecessors strand open successors

Witness observation, 2026-09-09 at 17:54 UTC.

The previous coordination audit overclaimed that all 121 queued successors were
waiting on live blocked prerequisites. Current chain state contradicts that:

| Rejected chain | Open successors |
| --- | ---: |
| coordination-hledger-plan-20260908 | 6 |
| witness-live-unattended-followup-20260908 | 2 |
| tinyfleet-applications-20260908 | 16 |
| coordination-hledger-identity-human-20260908 | 1 |

These 25 rows remain unfinished in tasks.journal. `mesh-task queue --dispatch`
returns no candidates. `mesh-task status` confirms rejected chain heads and open
successors. `mesh-task audit` labels the successors QUEUED without exposing this
terminal predecessor distinction. This is insufficient evidence of healthy flow.

In scripts/mesh-task, reject marks the whole chain rejected, reschedule refuses
rejected chains, and resume only accepts blocked current steps. The retained
successors therefore have no ordinary recovery transition. Automatic advancement
on any rejection would be wrong: a failed verification remains a real dependency.

The coordination identity rejection cites owner normalization. The separate
witness-owner-normalization-repair-20260908 chain is now DONE. Its completion is
evidence to investigate recovery, not automatic acceptance of the original task.
The human identity chain was split; its residual successor needs an explicit
supersession disposition, not another dispatch to an automated owner.

Required correction: expose stranded successors in audit/pane; provide an
explicit owner-authorized, artifact-backed recovery/disposition operation that
preserves original task IDs and rejection history. Verify repaired prerequisites
before reactivating work, keep unresolved verification/operator dependencies held,
and reconcile the four live chains through canonical events. Regression coverage
must include repaired rejection, unresolved rejection, wrong owner, replay,
idempotency, and subsequent exact-owner dispatch. Independent witness acceptance
must inspect real resulting ledger records, owner taking receipts and live pane.

Previous turn classification: no progress toward dependency recovery; its empty
queue observation did not poll a confirmed live process and was not a verified
wait under the active goal's definition. This turn supplies new causal evidence.
