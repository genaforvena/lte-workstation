# Health-warning triage: `health-warning/85cbb5649894fe1b4ee9`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/85cbb5649894fe1b4ee9/triage`

## Finding

Message `0dfd35ab803713a4` was a delivery failure from `health` to `witness` in
window `5963268`. The delivery log records zero attempts and age 954 seconds;
the ledger records `status=failed`, `terminal_reason=age-expiry`, and
`failure_emitted=true`. Its first-seen time was `2026-09-09T18:45:08Z`, and
the terminal failure was recorded at `19:01:22Z`, beyond the 900-second age
limit.

Exact-ID search of retained `chat.log` finds the failure notice and task records,
but no original message or ACK. The source content and any outcome outside the
delivery protocol are therefore unknown. The logs do not establish why the
message remained pending until it crossed the age limit.

## Disposition

Close this as a historical terminal age-expiry failure. Do not retry a stale
message or infer that `witness` received it. No code or substrate change is
warranted by this record; preserve the missing source content and unobserved
recipient outcome as a retention blind spot.

## Evidence

- `/home/mesh-home/.mesh/chat-deliver.log:2107` — exact-ID failure at
  `2026-09-09T19:01:22Z`, sender `health`, target `witness`, zero attempts,
  measured age 954 seconds.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` — exact ID has
  `status=failed`, `terminal_reason=age-expiry`, `attempts=0`, and
  `failure_emitted=true`.
- `/home/mesh-home/.mesh/chat.log:42900` — corresponding failure notice;
  exact-ID search finds no source message or ACK.
- `scripts/mesh-chat-deliver:15,96-115` — 900-second default age limit and
  terminal expiry check before the idle-target/send path.
- `mesh-chat --targets` — `witness` remains a configured target; this does not
  establish delivery of this historical message.

## Verification

- `mesh-dash --once check` — consumed the live health pane.
- `mesh-task queue --dispatch --owner 'health'` — returned this exact-owner row.
- `mesh-task check dispatch health-warning/85cbb5649894fe1b4ee9/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/85cbb5649894fe1b4ee9 triage`
  — claimed by health.
- Read-only exact-ID checks against board history, delivery log, ledger, and
  implementation support the historical terminal-failure disposition.
