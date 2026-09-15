# Health-warning triage: `health-warning/5cc78ecf528f73fa5972`

Date: 2026-09-11T19:57Z  
Task: `health-warning/5cc78ecf528f73fa5972/triage`

## Fresh read-only evidence

- `mesh-dash --once check` at 19:55:27Z reports fleet reachability degraded: 10
  nodes, 2 SSH, 0 LAN, and 8 down. It explicitly marks local-load probes as
  unreliable. The stream reports `FAIL=2/WARN=33` from the cached doctor:
  egress via `tailscale0` and an active exit-node SPOF.
- `mesh-health` at 19:56:13Z passes this node and `phaedra`, while reporting the
  same known fleet offline/SSH-unreachable rows. This is a sample, not proof of
  LAN health.
- `mesh-doctor` reaches the same two egress failures and passes Anthropic
  reachability; all supervised loops are up. It also reports the known broken or
  busy default microphone while the explicit `plughw:2,0` capture path passes.
- `mesh-hw-health` reaches thermal/disk evidence (`74C`, SMART PASSED, wear 2%,
  media errors 0) before timing out under load. `mesh-verify` reaches the local
  row (`linger=Y`, cron/tools/session/connectivity up) before timing out.
- Direct read-only checks confirm `ExitNodeID=n2sbt7yy6t11CNTRL`,
  `ExitNodeAllowLANAccess=true`, and `ip route get 1.1.1.1` returns `dev
  tailscale0 table 52`. Current load is `25.47/34.92/27.27` on 16 CPUs.

## Disposition

KNOWN PERSISTENT CONDITION / KNOWN BLINDNESS: the 2026-09-08 warning is
reproduced as the same two egress-topology failures, while reachability and
supervision remain operational at the sampled paths. LAN presence remains
UNKNOWN, and high load makes negative probe results unreliable. No routing, DNS,
firewall, VPN, WireGuard, Tailscale, or service mutation was made. A substrate
owner decision is required before any topology change; reopen on a new health
delta or that decision.
