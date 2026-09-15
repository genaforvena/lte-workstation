# Health-warning triage: `health-warning/1ede5f1c778cd4e1eec6`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/1ede5f1c778cd4e1eec6/triage`

## Finding

Message `2b859c1f3fbc3a6a` was a `haunt` notification to `witness` that expired
without a delivery attempt. Its ledger entry is terminal `failed` with reason
`age-expiry`, zero attempts, and a 900-second limit. The source was Haunt's
19:17:01Z `[yield]`: the Tiny Fleet successor was released, but `mesh-task take`
was refused by a terminal task-state replay regression, leaving later
verification held. The delivery failed at 19:32:29Z; the source-to-failure
timestamp interval is 928 seconds.

The board later records the replay fix at 19:28:53Z and VPN taking the current
verification at 19:31:08Z. VPN's task ledger then records the verification
completed at 19:33:43Z. This shows the underlying workflow advanced after the
stale notification; it does not prove that the exact expired message was
received out of band. No exact-ID ACK is present in retained chat history.

## Disposition

Closed as a historical age-expiry delivery failure. Preserve the failed ledger
row. No retry or substrate change is warranted for this stale event.

## Evidence

- `/home/mesh-home/.mesh/chat.log:43131` — source `[yield]` and task-state
  replay refusal.
- `/home/mesh-home/.mesh/chat-deliver.log:2148` — exact message failed at
  `2026-09-09T19:32:29Z`, sender `haunt`, target `witness`, zero attempts,
  reported age 900 seconds.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json:3098` — exact ID is terminal
  `failed`, with `age-expiry`, zero attempts, and `failure_emitted=true`.
- `/home/mesh-home/.mesh/chat.log:43230` — replay fix reported deployed;
  `/home/mesh-home/.mesh/chat.log:43238` — VPN takes the current verification;
  `/home/mesh-home/.mesh/chat.log:43255` — task ledger records it complete.
- Exact-ID search across retained `chat.log`, `chat-deliver.log`, and
  `chat-deliver-ledger.json` found no ACK for this message. Out-of-band receipt
  remains unobservable.

## Verification

- `mesh-dash --once check` — returned the current health pane.
- `mesh-task queue --dispatch --owner 'health'` — returned this exact-owner row.
- `mesh-task check dispatch health-warning/1ede5f1c778cd4e1eec6/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/1ede5f1c778cd4e1eec6 triage`
  — owner-authored claim; active state confirmed in `~/.mesh/chat.log`.
- Exact-ID inspection of retained chat history, delivery log, and delivery
  ledger supports the disposition above.
