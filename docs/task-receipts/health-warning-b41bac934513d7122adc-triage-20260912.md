# Health-warning triage: `health-warning/b41bac934513d7122adc`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/b41bac934513d7122adc/triage`

## Finding

Message `c35638440782d64e` is a historical delivery failure from `tg` to
`witness` in window `5963273`. The canonical delivery ledger records terminal
status `failed`, reason `age-expiry`, and zero attempts. The delivery log
records age 922 seconds against the 900-second limit. Exact-ID search in the
retained chat log finds the consolidated failure warning and task records but
no ACK or original source message; the content cannot be reconstructed from
retained chat history.

## Disposition

Close as a historical age-expiry failure. The delivery is terminal; no retry
or substrate change is warranted. Keep the missing original message content
explicit as a retention blind spot.

## Evidence

- `/home/mesh-home/.mesh/chat-deliver.log:2143` — exact ID failed at
  `2026-09-09T19:28:36Z`, sender `tg`, target `witness`, zero attempts, age
  922 seconds.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` — exact ID is terminal
  `failed`, reason `age-expiry`, zero attempts, failure emitted; first seen at
  `2026-09-09T19:12:40Z`.
- `/home/mesh-home/.mesh/chat.log:43220` — consolidated exact-ID failure
  warning; exact-ID search found no ACK or original source content.

## Verification

- `mesh-dash --once check` — returned the live health pane.
- `mesh-task check dispatch health-warning/b41bac934513d7122adc/triage health`
  — exit 0 before claim, using the full chain/step ID.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/b41bac934513d7122adc triage`
  — claimed by health.
- Targeted inspection of the canonical chat log, delivery log, and delivery
  ledger supports the terminal age-expiry disposition.
