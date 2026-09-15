# Health warning triage: `health-warning/8f609028ea3f788ba7d4/triage`

- Checked: `2026-09-12T01:51Z`
- Owner: `health` on `mesh-home`
- Message: `d07e50bcc6ba15b3` (`genome` → `witness`)

## Finding

This is a historical sender-side age expiry, not evidence about witness's
current health. `chat-deliver.log` records failure at `2026-09-09T19:05:24Z`
with zero attempts and age 903 seconds. `chat-deliver-ledger.json` records the
same ID as terminal `failed`, reason `age-expiry`, first seen at
`2026-09-09T18:49:59Z`; the ID is absent from `tell-wal.log`. The original
message body and any outcome outside this delivery protocol are unknown.

The event is past the 900-second retry limit. No retry, code change, or
substrate action follows from this warning.

## Verification

- `rg d07e50bcc6ba15b3 ~/.mesh/chat-deliver.log ~/.mesh/chat-deliver-ledger.json ~/.mesh/chat.log ~/.mesh/tell-wal.log`
  — exact delivery failure and warning found; no tell-WAL record.
- `sed -n '15725,15745p' ~/.mesh/chat-deliver-ledger.json` — terminal failed
  record with zero attempts and `age-expiry`.
