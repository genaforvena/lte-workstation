# Health-warning triage: `health-warning/0af97b3f057dc72d4dae`

Date: 2026-09-11  
Owner: health / mesh-home  
Task: `health-warning/0af97b3f057dc72d4dae/triage`

## Verdict

This is a bounded historical delivery miss, not a current `genome` outage.
The zero-attempt `age-expiry` warning is settled as historical evidence; no
retry, source change, or substrate mutation is warranted.

## Evidence

The exact delivery record is present in `~/.mesh/chat-deliver.log`:

```text
2026-09-11T14:12:04Z delivery-failed msg:71c134a63e397f80 sender:witness target:genome attempts:0 age:935s window:5963786
```

The ledger records `status=failed`, `terminal_reason=age-expiry`,
`attempts=0`, and `failure_emitted=true`. Later successful deliveries to
`genome` are present at 15:13:39Z, 17:11:05Z, 17:12:06Z, and 18:45:22Z,
showing that the target recovered/presented after the bounded miss. The
current `mesh-chat --targets` output includes `genome`.

## Current wiring and verification

- `mesh-chat --targets` — `genome` present.
- `python3 scripts/mesh-chat-deliver --test` — PASS.
- `bash tests/test-mesh-chat-deliver.sh` — PASS.
- `python3 tests/test-mesh-chat-deliver-attempts.py` — PASS.

No routing, DNS, firewall, VPN, Tailscale, or other substrate state was
changed. Known limitation: an idle-gated message can expire without an
attempt when its target has no stable eligible pane during the retry horizon.
