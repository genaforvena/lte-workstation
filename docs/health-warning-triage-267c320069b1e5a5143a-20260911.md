# Health-warning triage: `health-warning/267c320069b1e5a5143a`

Date: 2026-09-11T19:53:10Z  
Task: `health-warning/267c320069b1e5a5143a/triage`

## Fresh read-only evidence

- `mesh-dash --once check` at 19:53:07Z reports cached doctor `FAIL=2/WARN=33`.
  The visible failures remain egress via `tailscale0` and an active exit-node
  SPOF (`n2sbt7yy6t11CNTRL`).
- The same stream reports current egress `OK`, 0% loss, and 140.998ms average
  latency. This confirms reachability at the sample, not a healthy LAN route.
- Fleet path remains degraded: 10 nodes total, 2 SSH, 0 LAN, and 8 down;
  LAN presence is therefore still not established. Local load is high
  (`load1=124.94/16c`), making reachability probes explicitly unreliable.
- The source warning's historical-ledger failure and its 2026-09-08 delta are
  not visible in the current stream. No routing, DNS, firewall, VPN, WireGuard,
  Tailscale, or service mutation was made.

## Disposition

KNOWN STALE WARNING / KNOWN BLINDNESS: the reported historical warning is
reconciled, while the persistent egress topology failure, exit-node SPOF, and
LAN UNKNOWN state remain current. High local load is an additional reason not
to infer peer failure from non-answers. Reopen on a new health delta or a named
substrate-owner decision.
