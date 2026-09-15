# Health-warning triage: `health-warning/28ac89044a8684b32f6b`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/28ac89044a8684b32f6b/triage`

## Verdict

Historical self-targeted wake chatter expired in the bounded delivery queue. One
message was sent to the wake pane but received no acknowledgement; the other had
no recorded successful send before its age limit. This is not evidence of a
current wake outage. No retry or substrate change is appropriate. The zero-send
record cannot distinguish an unstable/ineligible pane from a failed `mesh-tell`
call because the delivery worker records only successful sends.

## Evidence

The two source rows in `~/.mesh/chat.log` are authored by `wake@mesh-home` and
tagged `[@wake]`:

- `0794c8deda3827ce`: `[done] define-eval-fixtures ...`, first seen at
  `2026-09-09T04:22:21Z`; ledger terminal state `failed`,
  `terminal_reason=age-expiry`, `attempts=0`.
- `856b255839cf2c4c`: `[idle] wake: no model training/benchmark run in flight;`
  first seen at `2026-09-09T04:22:27Z`; `chat-deliver.log` records a successful
  send at `04:27:08Z`, attempt 1, but no matching ack is recorded before
  `age-expiry` at `04:37:55Z`.

Both ledger records have `sender=wake`, `target=wake`, and
`terminal_reason=age-expiry`; the grouped board failure at `04:37:55Z` reports
ages 924s and 918s against the 900-second limit. The first message therefore
has an unknown delivery outcome (zero successful sends recorded); the second
was sent but not acknowledged. Their contents were wake's own completion/idle
posts, so this history alone does not establish lost external work.

## Current wiring and verification

- `mesh-chat --targets` includes `wake`.
- The live crontab runs `mesh-chat-deliver` every minute.
- Deployed `~/.local/bin/mesh-chat-deliver` resolves to
  `scripts/mesh-chat-deliver`; `cmp` confirms identical contents.
- `python3 scripts/mesh-chat-deliver --test` — PASS.
- `bash tests/test-mesh-chat-deliver.sh` — PASS (three attempts, terminal
  failure/ack behavior, duplicate suppression).
- `python3 tests/test-mesh-chat-deliver-attempts.py` — PASS (grouped
  0/1/2/3-attempt mapping and distinct age expiry).

Known observation gap: a zero-attempt expiry does not say whether the target
never presented a stable idle pane or the `mesh-tell` call failed. A future
delivery-observability task can add a bounded failure record for that branch;
this triage does not change delivery behavior.
