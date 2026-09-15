# Health warning triage: iMac path and historical egress findings

Task: `health-warning/f5177bd862c89b2fdb90/triage`  
Source warning: 2026-09-12T09:57:36Z check-stream delta

## Current evidence at 2026-09-14 19:48Z

- `tailscale status` reports `imac-rozalia` active and direct at
  `5.227.24.249:42772`. A fresh `tailscale ping -c 3 imac-rozalia` returned one pong via that
  direct endpoint in 5 ms. The historical idle/offline edge is not the current peer state.
- The same live Tailscale sample reports Phaedra active and directly reachable as the configured
  exit node. Public egress on `tailscale0 table 52` remains intentional for this node's consumer
  role; the refreshed card separately reports a healthy local gateway route and invariant check.
- The historical doctor count of two egress FAILs predates the role-aware policy correction. The
  fresh dashboard pane at 19:35Z reports doctor `FAIL=0 WARN=33`; the current live egress path and
  policy are documented in `mesh-doctor-egress-policy-20260914.md` and
  `health-live-egress-doctor-recheck-20260914T1442Z.md`.
- `mesh-lan-presence --nodes` still exits 1 with router/LAN state `UNKNOWN` because this node has
  no local address in `192.168.8.0/24` and no known host answered ICMP. This remains an explicit
  visibility limit; the successful gateway FIB lookup does not establish router presence.

## Disposition

The warning accurately captured a historical delta, but its peer and doctor findings are now
superseded by current direct iMac reachability and the role-aware zero-FAIL doctor result. The
separate inward-LAN unknown remains named in prior health receipts. No DNS, route, VPN, firewall,
or peer configuration was changed; no SSH authentication was attempted.

## Verification

- `tailscale status`: iMac active direct; Phaedra active direct as exit node.
- `tailscale ping -c 3 imac-rozalia`: direct pong in 5 ms.
- Current dashboard cache: doctor `FAIL=0 WARN=33`.
- Current refreshed card and prior live egress receipt: gateway FIB healthy, configured exit-node
  egress intentional.
- `mesh-lan-presence --nodes`: exit 1, `UNKNOWN`; exact visibility limit recorded above.
