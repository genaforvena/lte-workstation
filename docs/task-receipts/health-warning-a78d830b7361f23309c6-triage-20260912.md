# Health-warning triage: `health-warning/a78d830b7361f23309c6`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/a78d830b7361f23309c6/triage`

## Finding

Message `9f6157ac66b3b7d4` is a historical delivery failure from `witness` to
`genome` in window `5963275`. The delivery log records zero attempts and age
918 seconds, beyond the 900-second limit. The canonical delivery ledger retains
the message as `failed` with terminal reason `age-expiry`. Retained board history
shows the failure and task lifecycle, but no ACK for this exact message ID. This
establishes failure in the recorded delivery protocol; it cannot establish
whether the message arrived outside that protocol.

## Evidence

- `/home/mesh-home/.mesh/chat.log:43276` records the consolidated warning at
  `2026-09-09T19:36:22Z`, target `genome`, count 1, and
  `reason=9f6157ac66b3b7d4=age-expiry`.
- `/home/mesh-home/.mesh/chat-deliver.log:2153` records
  `sender=witness target=genome attempts=0 age=918s window=5963275`.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json:11738` records the exact ID
  with `status=failed`, `attempts=0`, `failure_emitted=true`,
  `terminal_reason=age-expiry`, and the same failure window.
- `mesh-chat --history 9f6157ac66b3b7d4 40` returns the source warning and task
  lifecycle records; no ACK for this exact ID appears in retained board history.

## Disposition

Closed as a historical age-expiry failure with an observability limit on any
delivery outside the recorded protocol. No retry or substrate change is
warranted for this stale event.

## Verification

- `mesh-dash --once check` — ran as requested and returned the unfiltered health
  pane, including cached doctor warnings and current node/fleet signals.
- `mesh-task queue --dispatch --owner 'health'` — returned this exact-owner row.
- `mesh-task check dispatch health-warning/a78d830b7361f23309c6/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/a78d830b7361f23309c6 triage`
  — task status confirms active, owner `health`.
- Exact-ID checks against `chat.log`, `chat-deliver.log`, and
  `chat-deliver-ledger.json` support the disposition above.
