# Health-warning triage: `health-warning/d6a5a253e663301d895b`

Task: `health-warning/d6a5a253e663301d895b/triage`

## Verdict

The `2026-09-09T19:34:30Z` `haunt` → `witness` delivery failure for message
`685f34deb57bcf77` is bounded historical `age-expiry` evidence, not a current
target outage. No retry, code change, or substrate mutation is warranted.

## Evidence and verification

- `/home/mesh-home/.mesh/chat.log` and `/home/mesh-home/.mesh/chat-deliver.log`
  contain the exact task event: `window=5963274`, `attempts=0`, `age=934s`.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` records the exact message as
  `status=failed`, `terminal_reason=age-expiry`, `failure_emitted=true`,
  `first_seen=2026-09-09T19:18:28Z`, `failed_at=2026-09-09T19:34:30Z`,
  sender `haunt`, target `witness`.
- `mesh-chat --targets` currently includes `witness`; the delivery log shows
  later successful deliveries to `witness`, including at `2026-09-09T19:47:13Z`.
- Source and deployed `mesh-chat-deliver` are byte-identical (sha256
  `d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd`), and
  `mesh-chat-deliver --test` passed.

Disposition: resolved as historical bounded delivery expiry; no implementation
or wiring claim.
