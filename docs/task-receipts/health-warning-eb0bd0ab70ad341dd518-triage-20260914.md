# Health roll-call triage: retired route and known visibility findings

Task: `health-warning/eb0bd0ab70ad341dd518/triage`  
Source warning: 2026-09-12T10:01:52Z roll-call

## Current evidence at 2026-09-14 19:43–19:48Z

- `route:no | PROPOSE none` refers to a retired marker; the warning reports no proposed route
  action. Current `ip -4 route get 100.76.0.1` returns `dev enp42s0`, table 52 has the connected
  `throw 100.76.0.0/16`, and refreshed `mesh-card` reports `exit-node-lan: ok` and
  `invariant-check: OK`. The live route repair receipt records the same verified state.
- The roll-call's `check 2 FAIL/33 WARN` is historical. The one-shot check pane at 19:35Z reports
  `FAIL=0 WARN=33`; the role-aware doctor receipt records why the configured Phaedra exit-node
  consumer is allowed and independently checks the local gateway FIB.
- `mesh-lan-presence --nodes` remains `UNKNOWN` (exit 1): no local address in `192.168.8.0/24`,
  ARP cannot observe the segment, and no known host answered ICMP. This is a recorded visibility
  blind, not evidence of a route regression. Earlier health triages already preserve this limit.
- The older Claude/storage warning was explicitly described as triaged/resolved and this new line
  provides no new device or storage observation to reopen it.

## Disposition

This row is a duplicate historical roll-call: its retired route proposal is inactive, its old
doctor count is superseded, and its remaining LAN-presence unknown is already documented. Reject
it as stale/duplicate; retain the named LAN visibility blind. No route, DNS, VPN, firewall,
storage, device, or service state was changed.

## Verification

- `mesh-card --refresh` at 19:43:36Z: local gateway route healthy; invariant check OK.
- `ip -4 route get 100.76.0.1`: `dev enp42s0`; `ip -4 route show table 52` contains the
  connected-prefix throw and Tailscale peer routes.
- `mesh-dash --once check` at 19:35Z: doctor `FAIL=0 WARN=33`.
- `mesh-lan-presence --nodes`: exit 1 and `UNKNOWN` with the visibility limits above.
- Canonical ledger confirms the cited route-policy repair and prior health triages are complete.
