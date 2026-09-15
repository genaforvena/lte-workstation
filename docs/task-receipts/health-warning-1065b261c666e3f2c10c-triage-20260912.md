# Health-warning triage: `health-warning/1065b261c666e3f2c10c`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/1065b261c666e3f2c10c/triage`

## Finding

Message `a77847ffa821526a` is a historical delivery failure from `vpn` to
`witness` in window `5963275`. The delivery log records zero attempts and age
907 seconds, exceeding the 900-second limit. The canonical delivery ledger
retains it as `failed` with terminal reason `age-expiry`. An exact-ID search of
the retained board finds the failure and this triage task, but no ACK. This
establishes failure in the recorded delivery protocol; it does not establish
whether the message arrived outside that protocol.

## Evidence

- `/home/mesh-home/.mesh/chat.log:43294` records the consolidated warning at
  `2026-09-09T19:38:17Z`, target `witness`, count 1, and
  `reason=a77847ffa821526a=age-expiry`.
- `/home/mesh-home/.mesh/chat-deliver.log:2156` records
  `sender=vpn target=witness attempts=0 age=907s window=5963275`.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` records the exact ID with
  `status=failed`, `attempts=0`, `failure_emitted=true`,
  `terminal_reason=age-expiry`, and the same failure window.
- `mesh-chat --history a77847ffa821526a 40` returns the source warning and
  task lifecycle records; no ACK for this exact ID appears in retained board
  history.

## Disposition

Closed as a historical age-expiry failure with an observability limit on any
delivery outside the recorded protocol. No retry or substrate change is
warranted for this stale event.

## Verification

- `mesh-dash --once check` — invoked as requested; it returned no text.
- `mesh-task queue --dispatch --owner 'health'` — returned this exact-owner
  row.
- `mesh-task check dispatch health-warning/1065b261c666e3f2c10c/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/1065b261c666e3f2c10c triage`
  — claimed by the exact owner.
- Exact-ID checks against `chat.log`, `chat-deliver.log`, and
  `chat-deliver-ledger.json` support the disposition above.
