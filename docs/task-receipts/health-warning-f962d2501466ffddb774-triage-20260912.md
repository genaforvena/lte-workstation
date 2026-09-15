# Health-warning triage: `health-warning/f962d2501466ffddb774`

- Checked: `2026-09-12T01:19Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/f962d2501466ffddb774/triage`

## Verdict

Historical sender-side age expiry. This is not evidence of a current target or
substrate outage. The specific receiver-side cause is unknown because the
original message body is not present in the retained chat history.

## Evidence

- `~/.mesh/chat-deliver.log` records message `e7ef45f727607b60`, from `witness`
  to `genome`, failing at `2026-09-09T19:26:44Z` with age `913s` and zero
  attempts.
- `~/.mesh/chat-deliver-ledger.json` records `status=failed`,
  `terminal_reason=age-expiry`, `attempts=0`, `first_seen=2026-09-09T19:10:50Z`,
  and `failure_emitted=true`. The configured age limit is 900 seconds; this
  failure happened before any delivery attempt.
- `mesh-chat --targets` lists `genome`, and `mesh-tell --peek genome` returned
  its live pane during this check. That establishes current target presence,
  not the cause of the old miss.
- The original body for `e7ef45f727607b60` was not found in retained chat
  history. No receiver-side explanation can be attributed from the available
  evidence.

## Disposition

The delivery record is terminal and outside its retry age window. Closed as a
historical bounded age expiry with the original content and receiver-side
cause unavailable. No delivery retry, source edit, or substrate change is
justified by this evidence.
