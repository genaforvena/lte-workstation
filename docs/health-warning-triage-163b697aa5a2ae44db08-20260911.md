# Health-warning triage: 163b697aa5a2ae44db08

Date: 2026-09-11T19:27:26Z  
Task: `health-warning/163b697aa5a2ae44db08/triage`

## Fresh read-only evidence

- `mesh-dash --once check` at 19:26:46Z reported cached doctor `FAIL=2/WARN=33`; the
  visible failures remain egress via `tailscale0` and an active exit-node SPOF
  (`n2sbt7yy6t11CNTRL`). The current stream did not show the source warning's
  `mesh-historical-ask-ledger` failure.
- The same dash stream reports current egress `OK`, 0% loss, and 143.973ms average
  latency; this is a live egress check and does not clear the route/exit-node
  topology warnings.
- `mesh-health` at 19:27:26Z reports `mesh-home` PASS and GL-MT3000, Redmi 10, and
  ilya OFFLINE. `tailscale status --json` reports 3 online peers.
- `mesh-egress-health` completed with rc=0 and no output; no substrate mutation was
  performed.

## Disposition

KNOWN DEGRADED STATE / RECONCILED WARNING: the historical 2->3 FAIL delta is not
present in the current cached doctor stream, while the persistent egress
topology/exit-node warnings and offline peers remain visible. No routing, DNS,
firewall, VPN, WireGuard, Tailscale, or service mutation is authorized by this
triage. Reopen on a new health delta or a named substrate-owner decision.
