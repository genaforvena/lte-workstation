# Health roll-call triage: iMac path, exit-node route, and DNS

Task: `health-warning/0447bfa92acf25dfc926/triage`  
Source warning: 2026-09-12T12:06:10Z roll-call

## Current evidence at 2026-09-14 19:43–19:52Z

- Current `tailscale status` shows imac-rozalia active and direct at
  `5.227.24.249:42772`; `tailscale ping -c 3 imac-rozalia` reached it directly in 5 ms. The
  warning's inactive/relayed snapshot is stale. Prior strict SSH attempts failed host-key
  verification, so the current direct tailnet path does not establish authenticated SSH access.
- Phaedra is currently active and directly connected as the selected exit node. Public egress via
  `tailscale0 table 52` remains expected for this consumer role and is a known single-exit
  availability dependency. The 19:52Z pane reports egress `OK loss=0%` and doctor `FAIL=0 WARN=33`.
- The local gateway is separate and healthy: refreshed card at 19:43Z says
  `100.76.0.1 -> dev enp42s0`, `exit-node-lan: ok`, and `invariant-check: OK`.
- DNS for `api.anthropic.com` currently resolves to `160.79.104.10` on the system resolver and
  both queried public resolvers. A credential-free HTTPS request to the hostname completed TLS
  and returned HTTP/2 404 at the API root; that verifies reachability without claiming an
  authenticated API call.
- `mesh-lan-presence --nodes` remains `UNKNOWN` because this host lacks a local
  `192.168.8.0/24` address, ARP cannot observe that segment, and no known host answered ICMP.

## Disposition

This old roll-call repeats peer-path, egress, DNS and LAN findings already reconciled in the
completed health receipts `health-warning-1aa3693a102855b922e4/triage`,
`health-warning/dc221f87143bc683b504/triage`, and
`health-warning/17d878bb98da052bc55c/triage`. The peer is now direct and ping-responsive; the
egress route is working and policy-expected; the independent LAN-presence blind and exit-node SPOF
remain named; SSH authentication is still unverified. Reject this stale duplicate. No route,
DNS, firewall, VPN, peer, or service state was changed.

## Verification

- `tailscale status` and `tailscale ping -c 3 imac-rozalia`: direct peer, 5 ms pong.
- `ip -4 route get 1.1.1.1`: `dev tailscale0 table 52`; configured exit-node consumer path.
- `mesh-dash --once check` at 19:52Z: egress loss 0%, doctor FAIL=0 WARN=33.
- `mesh-card --refresh` at 19:43Z: local gateway FIB and invariant check OK.
- `getent`, `resolvectl`, `dig @1.1.1.1`, `dig @8.8.8.8`, and HTTPS root probe: current DNS and
  TLS reachability as stated.
- `mesh-lan-presence --nodes`: exit 1, `UNKNOWN` with the visibility limit stated above.
