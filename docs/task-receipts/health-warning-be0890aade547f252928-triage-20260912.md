# Health-warning triage: `health-warning/be0890aade547f252928`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/be0890aade547f252928/triage`

## Finding

Message `bd24d1d0ec7f102d` is a historical `tg` FYI addressed to `witness` in
window `5963274`. The canonical delivery ledger records it as terminal
`failed`, with zero attempts and reason `age-expiry`. The delivery log reports
age 935 seconds against the 900-second limit.

The source is the 19:14:28Z `tg` FYI about the ask-answer funnel: it says the
operator directive had already been applied, the canonical final-funnel task
was DONE, and terminal ACK `52e14ee385fc7576` had been posted. The referenced
final verification receipt records that the full deployed gate and focused
mutation test passed before closure. This establishes later workflow state,
not receipt of this exact FYI by `witness`; no exact-ID ACK appears in retained
chat history.

## Disposition

Close as a historical age-expiry delivery failure. Preserve the failed ledger
row; no retry or substrate change is warranted for this stale notification.

## Evidence

- `/home/mesh-home/.mesh/chat.log:43113` — source FYI, including the already
  posted terminal ACK and claimed canonical task completion.
- `/home/mesh-home/.mesh/chat-deliver.log:2147` — exact ID failed at
  `2026-09-09T19:30:34Z`, sender `tg`, target `witness`, zero attempts, age
  935 seconds.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json:14155` — exact ID is
  terminal `failed`, with `age-expiry`, zero attempts, and
  `failure_emitted=true`.
- `/home/mesh-home/.mesh/chat.log:43237` — consolidated exact-ID failure
  warning. Exact-ID search in retained `chat.log` found no ACK.
- `docs/task-receipts/final-funnel-verification-20260909.md` — final closure
  verification records the focused test and deployed full gate at `rc=0`.

## Verification

- `rtk mesh-dash --once check` — returned the live health pane.
- `rtk mesh-task queue --dispatch --owner 'health'` — returned this exact-owner
  row.
- `rtk mesh-task check dispatch health-warning/be0890aade547f252928/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health rtk mesh-task take health-warning/be0890aade547f252928 triage`
  — claimed by health; active state recorded in `~/.mesh/chat.log`.
- Exact-ID inspection of retained chat history, delivery log, and delivery
  ledger supports the disposition above.
