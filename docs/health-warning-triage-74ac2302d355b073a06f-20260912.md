# Health warning triage — 74ac2302d355b073a06f

The failed delivery was an expired historical FYI, not an outstanding request.

- Message `4b100348ad05cccf` is the 2026-09-09T18:32:07Z genome-to-witness FYI:
  “exact task already terminal: mesh-task take refused because
  blocked-ledger-visibility-20260909/separate-blocked-from-queued is done; receipt
  and focused verification are present.” The message ID was independently matched
  to its original `chat.log` line by the delivery script's SHA-256/16 ID rule.
- `chat-deliver-ledger.json` records `first_seen=18:32:07Z`, `attempts=0`,
  `status=failed`, `terminal_reason=age-expiry`; `chat-deliver.log` records expiry
  at 18:48:28Z with age 955s. `scripts/mesh-chat-deliver` sets the default maximum
  age to 900s and terminally records age expiry without another push attempt.
- `mesh-task status blocked-ledger-visibility-20260909` reports the chain
  complete and `separate-blocked-from-queued` done. Its receipt is
  `docs/task-receipts/separate-blocked-from-queued-20260909.md`, documenting the
  focused regressions and deployed checks as passing.

Disposition: stale FYI after the referenced task was resolved. The expiry behaved
as configured; do not retry this terminal message. `rtk python3
scripts/mesh-chat-deliver --test` passed (bounded-ledger smoke test).
