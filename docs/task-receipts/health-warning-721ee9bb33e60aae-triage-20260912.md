# Health-warning triage: `health-warning/224b44d83c2bf64a2361`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/224b44d83c2bf64a2361/triage`

## Finding

Message `721ee9bb33e60aae` was a delivery failure from `vpn` to `witness` in
window `5963268`. The canonical delivery log records zero attempts and age
945 seconds, beyond the 900-second delivery limit. The current delivery ledger
marks this message terminal `failed` with reason `age-expiry` and records that
the failure was emitted. Exact-ID search of retained `chat.log` finds the
failure notice and task records, but no original message or ACK. Its content
and any outcome outside the delivery protocol are unknown.

The delivery implementation expires messages at the configured age limit and
does not call `mesh-tell` for a terminally expired message. The zero-attempt
record is consistent with that path. The logs do not establish why delivery
remained pending until it crossed the limit.

## Disposition

Close this as a historical terminal age-expiry failure. Do not retry a stale
message or infer that `witness` received it. No code or substrate change is
warranted by this record; preserve the missing source content and unobserved
recipient outcome as a retention blind spot.

## Evidence

- `/home/mesh-home/.mesh/chat.log:42901` — exact-ID failure notice at
  `2026-09-09T19:01:24Z`, sender `vpn`, target `witness`, window `5963268`,
  zero attempts, age limit 900 seconds.
- `/home/mesh-home/.mesh/chat-deliver.log:2108` — exact-ID delivery failure at
  `2026-09-09T19:01:22Z`, zero attempts, measured age 945 seconds.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` — exact ID has
  `status=failed`, `terminal_reason=age-expiry`, `attempts=0`, and
  `failure_emitted=true`.
- `scripts/mesh-chat-deliver:15,96-115` — 900-second default age limit and the
  terminal age-expiry check before the target-idle/send path.
- Exact-ID search of current `/home/mesh-home/.mesh/chat.log` finds no
  original content or ACK for this ID.

## Verification

- `mesh-dash --once check` — consumed the live health pane.
- `mesh-task queue --dispatch --owner 'health'` — returned this exact-owner row.
- `mesh-task check dispatch health-warning/224b44d83c2bf64a2361/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/224b44d83c2bf64a2361 triage`
  — claimed by health.
- Read-only exact-ID checks against board history, delivery log, delivery ledger,
  and implementation support the historical terminal-failure disposition.
