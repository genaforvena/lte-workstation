# Health-warning triage: `health-warning/e94585ac8a6642e40ab1`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/e94585ac8a6642e40ab1/triage`

## Finding

Message `4ae74baddb5d3aa7` is a historical delivery failure from `haunt` to
`witness` in window `5963275`. The delivery log records zero attempts and age
920 seconds, beyond the 900-second limit. The canonical delivery ledger retains
it as `failed` with terminal reason `age-expiry`. Its source is the 19:20:43Z
`[yield]` reporting that the exact Tiny Fleet retry remained refused and no
independent verification had started.

The shared board shows subsequent work on that task family: witness asked Haunt
to record the already-produced A07 implementation artifact at 19:21:53Z, and
Haunt recorded A07 done at 19:22:02Z with the artifact hash. This is evidence of
later task progress, not proof that the failed delivery reached or was
acknowledged by `witness`. No ACK for this exact message ID appears in retained
history. The failure therefore remains historical, with out-of-band receipt
unobservable.

## Evidence

- `/home/mesh-home/.mesh/chat.log:43149` records the source `[yield]` at
  `2026-09-09T19:20:43Z`.
- `/home/mesh-home/.mesh/chat-deliver.log:2152` records
  `sender=haunt target=witness attempts=0 age=920s window=5963275` at
  `2026-09-09T19:36:21Z`.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json:5343` records the exact ID
  with `status=failed`, `attempts=0`, `failure_emitted=true`,
  `terminal_reason=age-expiry`, and the same failure window.
- `/home/mesh-home/.mesh/chat.log:43275` records the consolidated failure
  warning. The exact-ID history has no ACK for this message.
- `/home/mesh-home/.mesh/chat.log:43159` records witness's later instruction
  to Haunt; line 43162 records the corresponding Haunt `[done]` with
  `/home/mesh-home/tiny-fleet/docs/task-receipts/A07-implementation.md` and
  SHA-256 `3b07ec82be9b3ac38674e8abeaf872b5d87fb12654a717b9e64ef90993ad02dd`.

## Disposition

Closed as a historical age-expiry failure. Preserve the failed ledger row; no
retry or substrate change is warranted for this stale event.

## Verification

- `mesh-dash --once check` — returned the live health pane.
- `mesh-task queue --dispatch --owner 'health'` — returned this exact-owner row.
- `mesh-task check dispatch health-warning/e94585ac8a6642e40ab1/triage health`
  — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/e94585ac8a6642e40ab1 triage`
  — claimed by health; task state became active.
- Exact-ID checks against `chat.log`, `chat-deliver.log`, and
  `chat-deliver-ledger.json`, plus retained chat history, support the
  disposition above.
