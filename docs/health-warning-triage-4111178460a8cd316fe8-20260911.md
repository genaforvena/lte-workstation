# Health-warning triage: `health-warning/4111178460a8cd316fe8`

Task: `health-warning/4111178460a8cd316fe8/triage`

## Verdict

The `2026-09-11T15:00:08Z` `genome` → `witness` delivery failure for message
`36c5c838276b68fd` is bounded historical `age-expiry` evidence, not a current
target outage. No retry, code change, or substrate mutation is warranted.

## Evidence and verification

- `/home/mesh-home/.mesh/chat.log` contains the exact warning at
  `window=5963796`, with `attempts=0`, `reason=age-expiry`, and `age-limit=900s`.
- `/home/mesh-home/.mesh/chat-deliver.log` records the terminal event with
  `age=920s`, `attempts=0`, and the same window/message identity.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` records the message as
  `status=failed`, `failure_emitted=true`, `failed_at=2026-09-11T15:00:08Z`,
  `first_seen=2026-09-11T14:44:45Z`, sender `genome`, target `witness`.
- `mesh-chat --targets` currently includes `witness`; the delivery log shows
  later successful deliveries to `witness`, including through `2026-09-11T20:39:06Z`.
- Live cron wiring is `* * * * * $HOME/.local/bin/mesh-chat-deliver >> $HOME/.mesh/chat-deliver.log 2>&1`.
- Source and deployed `mesh-chat-deliver` are byte-identical, SHA-256
  `d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd`.
- `mesh-chat-deliver --test` passed.
- `bash tests/test-mesh-chat-deliver.sh` passed.
- `python3 tests/test-mesh-chat-deliver-attempts.py` passed.

Disposition: resolved as historical bounded delivery expiry; no implementation
or wiring claim.
