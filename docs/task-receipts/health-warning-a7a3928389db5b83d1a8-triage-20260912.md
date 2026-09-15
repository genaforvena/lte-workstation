# Health-warning triage: `health-warning/a7a3928389db5b83d1a8`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/a7a3928389db5b83d1a8/triage`

## Finding

This is a historical age-expiry event for three `vpn` messages addressed to
`witness` in delivery window `5963275`. The canonical ledger records all three
as failed with zero attempts and terminal reason `age-expiry`. Their first-seen
times are 16 minutes before the common failure timestamp, beyond the 900-second
age limit. Exact-ID searches found no ACK. The delivery evidence does not show
whether any message was delivered outside this recorded protocol.

## Evidence

- `/home/mesh-home/.mesh/chat.log:43298` records the consolidated warning at
  `2026-09-09T19:39:09Z`, with IDs `242b92b81490e2dd`,
  `64654ce1603b5aa4`, and `267a5e0a896c3147`, target `witness`, and
  `age-expiry` for each.
- `/home/mesh-home/.mesh/chat-deliver.log:2157-2159` records zero attempts and
  ages 952s, 949s, and 948s respectively; the limit was 900s.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` retains each exact ID with
  `status=failed`, `attempts=0`, `terminal_reason=age-expiry`, and
  `failure_window=5963275`.
- Exact-ID search across current board history found the warning and this task's
  creation/claim records, but no ACK for any of the three IDs.

## Disposition

Closed as a historical age-expiry failure with unknown outcome beyond the
recorded protocol. No retry or substrate change is warranted for these stale
messages.

## Verification

- `mesh-dash --once check` — exit 0; live health pane consumed.
- `mesh-task queue --dispatch --owner 'health'` — returned the exact-owner row.
- `mesh-task check dispatch health-warning/a7a3928389db5b83d1a8/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/a7a3928389db5b83d1a8 triage`
  — claimed by the exact owner.
- Read-only exact-ID checks in `chat.log`, `chat-deliver.log`, and
  `chat-deliver-ledger.json` support the disposition above.
