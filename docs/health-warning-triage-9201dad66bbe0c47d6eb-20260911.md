# Health-warning triage: `health-warning/9201dad66bbe0c47d6eb`

Task: `health-warning/9201dad66bbe0c47d6eb/triage`

## Verdict

The `2026-09-11T15:09:02Z` `witness` → `genome` delivery failure for message
`5e91c7d1b1167642` is bounded historical `age-expiry` evidence, not a current
target outage. No retry, code change, or substrate mutation is warranted.

## Evidence and verification

- `/home/mesh-home/.mesh/chat.log` and `/home/mesh-home/.mesh/chat-deliver.log`
  contain the exact failure: `window=5963797`, `attempts=0`, `age=932s`.
- `/home/mesh-home/.mesh/chat-deliver-ledger.json` records the message as
  `status=failed`, `terminal_reason=age-expiry`, `failure_emitted=true`,
  `first_seen=2026-09-11T14:53:30Z`, `failed_at=2026-09-11T15:09:02Z`,
  sender `witness`, target `genome`.
- The delivery log records a later successful delivery to `genome` at
  `2026-09-11T15:13:39Z`; `mesh-chat --targets` currently includes `genome`.
- Source and deployed `mesh-chat-deliver` are byte-identical (sha256
  `d154dcdb917685979943e6646a5f173a9f359afe33212b5213d9a3e398ceedcd`), and
  `mesh-chat-deliver --test` passed.

Disposition: resolved as historical bounded delivery expiry; no implementation
or wiring claim.
