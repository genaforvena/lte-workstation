# Health-warning triage: `health-warning/0ec6f3df6907f304c18a`

- Checked: `2026-09-12T01:23Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/0ec6f3df6907f304c18a/triage`

## Verdict

Historical sender-side age expiry. The delivery subsystem marked message
`9d1ada37d9fa5c8f` from `witness` to `genome` failed after 956 seconds with
zero attempts, beyond its 900-second age limit. The original message body is
not present in retained chat or tell-WAL history, so the receiver-side cause
and whether it was seen outside this delivery protocol are unknown. This is
not evidence of a current target outage.

## Evidence

- `/home/mesh-home/.mesh/chat-deliver.log:2133` records the exact ID failing
  at `2026-09-09T19:21:39Z`, `sender=witness`, `target=genome`,
  `attempts=0`, `age=956s`, `window=5963272`.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` retains the exact ID as
  `status=failed`, `terminal_reason=age-expiry`, `attempts=0`,
  `failure_emitted=true`, first seen `2026-09-09T19:05:06Z`.
- `/home/mesh-home/.mesh/chat.log:43158` records the consolidated warning
  with the same message ID and `age-limit=900s`.
- Exact-ID searches of retained `chat.log` and `tell-wal.log` found no source
  body or ACK; only the failure warning and this task's lifecycle records
  remain in `chat.log`.

## Disposition

Closed as a historical bounded age expiry with the original content and
receiver-side cause unavailable. The terminal record is outside its retry
age window. No delivery retry, code change, or substrate action is warranted.

## Verification

- `mesh-dash --once check` returned the live health pane.
- `mesh-task queue --dispatch --owner 'health'` returned this exact-owner row.
- `mesh-task check dispatch health-warning/0ec6f3df6907f304c18a/triage health`
  exited 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/0ec6f3df6907f304c18a triage`
  claimed the exact-owner task.
- Exact-ID inspection of `chat.log`, `tell-wal.log`, `chat-deliver.log`, and
  `chat-deliver-ledger.json` supports the disposition above.
