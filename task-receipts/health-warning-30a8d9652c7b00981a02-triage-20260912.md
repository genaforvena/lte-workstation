# Health warning triage: `health-warning/30a8d9652c7b00981a02`

Checked 2026-09-12 11:20–11:22 UTC on `mesh-home`. The exact-owner dispatch check exited 0 and health claimed `health-warning/30a8d9652c7b00981a02/triage`.

## Finding

The Sep 9 warning's relay observation is stale: `imac-rozalia` is direct in the current Tailscale status. The persistent conditions are LAN visibility UNKNOWN and default egress via `tailscale0` with exit node `phaedra`; the node's own LAN address still routes through Tailscale table 52. DNS A for `api.anthropic.com` remains `160.79.104.10`. The pane's doctor count is cached from 09:32Z (3 FAIL/34 WARN), so this pass does not claim a fresh comprehensive doctor total or validate the older 2F/33W delta.

## Evidence

- `mesh-dash --once check` (11:20:19Z) showed 10 nodes (2 SSH, 0 LAN, 8 down), LAN/probe uncertainty under `LOCAL LOAD HIGH`, egress via `tailscale0`, and exit-node `phaedra`. The doctor's displayed 3F/34W is explicitly cached at 09:32:30Z.
- `mesh-card` (live-refreshed 11:13:20Z) reports default egress `tailscale0`, exit-node `phaedra`, and the invariant violation that `100.74.0.1` is swallowed by Tailscale table 52 instead of the LAN link.
- `ip route get 100.74.0.1` returned `dev tailscale0 table 52 src 100.81.222.19`, confirming the card's route diagnosis.
- `mesh-health` (11:21:14Z) passed `mesh-home` and `phaedra`, reported `imac-rozalia` SSH authentication refused, and listed six peers offline. Its probes inherit the pane's stated local-load reachability uncertainty.
- `tailscale status` showed both `imac-rozalia` (`direct 5.227.25.156:55351`) and `phaedra` (`exit node; direct 38.49.216.141:41641`) direct. Recent `mesh-trace` also records a brief direct-to-relay transition involving phaedra followed by a recovery; the current status is direct.
- `dig +short A api.anthropic.com` returned `160.79.104.10`.
- `mesh-trace --tail 30` showed repeated `[exit-node-lan-heal] REFUSED` marks: the healer refuses the `100.74.0.0/16` LAN exclusion because its current eligibility rule accepts RFC1918 networks only. This explains a persistent known failure; no route, DNS, firewall, VPN, or other substrate state was changed.

## Disposition

Keep LAN visibility and Tailscale egress/exit-node dependency open as known health gaps. The imac relay finding is currently clear; its SSH authentication refusal is a separate probe limitation. A fresh full doctor total remains unverified because the pane only carries a cached total. No substrate mutation was in scope for this triage.
