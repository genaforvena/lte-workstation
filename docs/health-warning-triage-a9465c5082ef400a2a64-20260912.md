# Health-warning triage: `health-warning/a9465c5082ef400a2a64`

Task: `health-warning/a9465c5082ef400a2a64/triage`

## Verdict

The `2026-09-09T18:57:19Z` haunt → witness warning records one message that aged
past the delivery worker's 900-second limit before any send attempt. It is a
terminal historical expiry, not evidence by itself that the witness target is
currently unreachable. Do not retry the expired message.

## Evidence

- `/home/mesh-home/.mesh/chat.log` has the failure line for message
  `7b2548c5eb7e1e7f`, window `5963267`, with `attempts=0`,
  `reason=age-expiry`, and `age-limit=900s`.
- `/home/mesh-home/.mesh/chat-deliver.log` records `first_seen` in the ledger
  as `2026-09-09T18:41:53Z`, then `delivery-failed` at `18:57:18Z`,
  `attempts:0`, `age:909s`. The ledger marks it `status=failed`,
  `terminal_reason=age-expiry`, `failure_emitted=true`, sender `haunt`, target
  `witness`. The log does not retain the pre-send gate's specific reason, so the
  cause of the delay cannot be narrowed further from this event.
- The delivery log records another message delivered to `witness` at
  `2026-09-09T18:54:29Z`; current `mesh-chat --targets` also includes
  `witness`. These establish successful routing near the event and current
  target registration, not the state of the witness pane at `18:57`.
- `crontab -l` contains the one-minute `mesh-chat-deliver` worker. Source and
  deployed worker hashes match:
  `d154dcdb917685979943e6646a5f1739a5f359afe33212b5213d9a3e398ceedcd`.
- `python3 scripts/mesh-chat-deliver --test` passed with
  `smoke-test ok (stable message id, terminal controls, bounded ledger contract)`.

Disposition: settled as a bounded historical expiry. No delivery-policy or
substrate change is justified by this single record; the exact pre-send delay
reason remains unknown.
