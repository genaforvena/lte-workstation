# Health-warning triage: `health-warning/15d798438dd6bab21e0a`

Date: 2026-09-12  
Owner: health / mesh-home  
Task: `health-warning/15d798438dd6bab21e0a/triage`

## Verdict

This warning records a terminal, historical delivery expiry for message
`06b93f0b2256ccc3` from `witness` to `tg`. The message's owner disposition is
documented and independently verified; `tg` is currently listed as a chat
target. The expiry remains in the delivery ledger as historical evidence. No
retry or source/substrate change is warranted from this warning.

## Evidence

The canonical board and delivery tape record the same zero-attempt failure:

```text
2026-09-09T18:22:27Z mesh-home/mesh-chat-deliver@mesh-home :: [@witness] [delivery-failed] target:tg window:5963260 count:1 msg:06b93f0b2256ccc3 attempts:06b93f0b2256ccc3=0 reason:06b93f0b2256ccc3=age-expiry age-limit:900s
2026-09-09T18:22:27Z delivery-failed msg:06b93f0b2256ccc3 sender:witness target:tg attempts:0 age:955s window:5963260
```

`/home/mesh-home/.mesh/chat-deliver-ledger.json` records `first_seen` at
18:06:07Z, `failed_at` at 18:22:27Z, `attempts=0`, `status=failed`, and
`terminal_reason=age-expiry`. This establishes the 900-second expiry outcome;
it does not establish why the message remained pending until the age limit.

The one-to-one owner answer at
`docs/task-receipts/resolve-06b93f0b2256ccc3-20260910.md` identifies the
message as a `witness` FYI about the `HELD_REJECTED` renderer lists. It records
the owner's disposition as accepted and independently verified, with focused
regression evidence. The same receipt preserves the delivery ledger's
terminal failure rather than rewriting it. `rtk mesh-chat --targets` currently
lists `tg`.

## Disposition

The requested health triage is complete. The owner receipt resolves the
message's work disposition, while the delivery failure remains visible as a
historical terminal event. No routing, DNS, firewall, VPN, Tailscale, or other
substrate state was changed. No code change was made, so no code test was run.
