# Health-warning triage — `health-warning/1f64462081c3aa963b8a`

Checked 2026-09-16 05:30–05:34 UTC on `mesh-home`.

## Finding

The source warning at `/home/mesh-home/.mesh/chat.log:71833` reports two
targeted-delivery failures at 2026-09-16T04:59:20Z:

```text
[@wake] [delivery-failed] target:wake window:5965115 count:2
msg:53def82e22fe0e12,20de20716f21d2b7
attempts:53def82e22fe0e12=0,20de20716f21d2b7=0
reason:53def82e22fe0e12=age-expiry,20de20716f21d2b7=age-expiry age-limit:900s
```

The canonical delivery ledger records both IDs as `status=failed`,
`terminal_reason=age-expiry`, target `wake`, zero attempts, and first-seen
times 2026-09-16T04:43:52–53Z. The independent delivery log records both
failures at line 2615–2616 with the same target, zero attempts, and window.
This is a bounded delivery-edge expiry, not evidence of a routing, DNS,
firewall, VPN, Tailscale, or node failure. No substrate repair is warranted.

## Current wiring and verification

- `crontab -l` contains the active one-minute `mesh-chat-deliver` entry.
- `sha256sum` of `scripts/mesh-chat-deliver` and
  `/home/mesh-home/.local/bin/mesh-chat-deliver` matches:
  `dbab9c4caaf506178bcf83fb0579555b6ec846015e6155dcd1d461fcf32b62ae`.
- `python3 scripts/mesh-chat-deliver --test` — PASS.
- `bash tests/test-mesh-chat-deliver.sh` — PASS.
- `python3 tests/test-mesh-chat-deliver-attempts.py` — PASS.
- `mesh-health` — PASS for this node; GL-MT3000, Redmi 10, iMac-Rozalia,
  and Phaedra reachable. Several historical/offline peers remain offline.

`mesh-dash --once check` was explicitly attempted twice, including a bounded
TTY run, but produced no stream and required interruption after 10 seconds;
this is an unresolved dashboard-read anomaly, not a health-pass claim.

Disposition: **known delivery-edge age-expiry; no substrate repair warranted**.
The next actionable edge is a changed terminal reason or a delivery
log/ledger that stops advancing.

## Delegation and ownership

Delegation decision: no subagent was launched. This was one tightly coupled
live read-and-disposition task; task ownership, receipt writing, board voice,
substrate boundary, and final verification stayed local. Personally inspected
the chat event, delivery log, canonical ledger row, task journal, source and
deployed script identity, crontab, focused tests, and `mesh-health` output.
