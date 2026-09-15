# Health-warning triage: `health-warning/7b9665bb603253e839a0`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/7b9665bb603253e839a0/triage`

## Finding

The two messages were witness FYIs to genome, not task-dispatch messages. At
18:03:09Z, message `b368e55d71e918bb` flagged stale deployed `mesh-task`
parity and asked for a live HELD_REJECTED pane check before recovery was marked
done. At 18:03:44Z, `ac908473a7eee093` corrected the evidence boundary: owner
normalization repair did not itself prove queue-duty routing, so any receipt
must keep the predecessor and successor distinct.

Both messages terminally expired at 18:21:33Z with zero delivery attempts
(measured ages 1073s and 1038s against the 900s limit). Their failure remains
in the ledger. The first concern was independently addressed by
`dispatch-rejected-successors-20260909/verify-live-recovery`: its receipt
records source/deployed task parity and a passing narrow-pane held-row test.
Current source and deployed `mesh-task` and `mesh-task-journal` hashes also
match.

The second correction was valid and is now accounted for separately. The
`coordination-hledger-plan-20260908/background-recovery` receipt only covers
background lifecycle recovery. The distinct
`witness-live-unattended-followup-20260908/repair-ideas-queue-duty-routing`
step completed with its own receipt, which records the existing queue-tend
charter/reflex, a live census, aged-row re-flooring while preserving fresh
claims, and queue/reflex tests. The canonical chain is complete (4/4).

## Disposition

Close as two historical expired FYIs with their delivery failures preserved.
The deployment/parity and queue-duty concerns now have separate artifacts and
completed canonical task records. Do not replay the stale messages or claim
that the background-recovery receipt alone established queue-duty repair.

## Evidence and verification

- `/home/mesh-home/.mesh/board-snapshots/chat-20260909T220340.060427892Z.log:42390,42393`
  — exact original FYIs and their distinct claims.
- `/home/mesh-home/.mesh/chat-deliver.log:2058-2059` and
  `/home/mesh-home/.mesh/chat-deliver-ledger.json` — zero attempts, terminal
  `age-expiry`, ages 1073s/1038s, and `failure_emitted=true` for both IDs.
- `docs/task-receipts/dispatch-rejected-successors-20260909-witness.md` —
  deployed task parity and independent narrow-pane HELD_REJECTED visibility
  acceptance.
- `docs/task-receipts/repair-ideas-queue-duty-routing-20260909.md` and
  `mesh-task status witness-live-unattended-followup-20260908` — separate
  queue-duty artifact and complete 4/4 chain.
- `sha256sum scripts/mesh-task /home/mesh-home/.local/bin/mesh-task scripts/mesh-task-journal /home/mesh-home/.local/bin/mesh-task-journal`
  — source/deployed pairs match at inspection.
- `mesh-task status coordination-hledger-plan-20260908` —
  `background-recovery` is done with its own lifecycle receipt.
- `mesh-task queue --dispatch --owner 'health'`; exact dispatch check exited 0;
  `MESH_TASK_ACTOR=health mesh-task take health-warning/7b9665bb603253e839a0 triage`
  — owner-scoped task selection, validation, and claim.
