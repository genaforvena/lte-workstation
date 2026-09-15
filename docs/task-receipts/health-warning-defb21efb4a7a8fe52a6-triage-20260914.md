# Health warning triage: Redmi / table-52 / inward LAN

Task: `health-warning/defb21efb4a7a8fe52a6/triage`  
Source warning: 2026-09-12T05:32:05Z health FYI

## Live evidence at 2026-09-14 19:42–19:43Z

- `mesh-health` still reports Redmi 10 `OFFLINE`, tailnet IP `100.103.99.16`, last seen
  `2026-09-03T09:53:36Z`, and its configured off-tailnet fallback unanswered. This is the same
  external reachability gate already represented by
  `discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`, blocked on
  `event:first-successful-redmi-ssh-port-8022-probe`. Its 09:24Z three-endpoint SSH attempts all
  timed out; the linked resolver records that no local ADB/SSH path can wake or pair the handset.
  No changed reachability state justifies repeating those probes.
- The old card claim that table 52 swallows the local gateway is stale. Live `ip route get
  100.76.0.1` returns `dev enp42s0`; table 52 contains `throw 100.76.0.0/16`. The refreshed
  19:43Z `mesh-card` says `exit-node-lan: ok`, gateway `100.76.0.1 -> dev enp42s0`, and
  `invariant-check: OK`. This matches the live repair verification in
  `task-receipts/exit-node-lan-cgnat-live-repair-20260914.md`.
- Inward LAN/router presence remains a separate known blind. `mesh-lan-presence --nodes` returned
  exit 1 and `UNKNOWN`: no local address in `192.168.8.0/24`, ARP cannot see that segment, and no
  known host answered ICMP. This has already been named in the completed health triages
  `health-warning/f72e0fff6dbfe173ee86/triage` and
  `health-warning/8b69362a3a0d32f75c2d/triage`; the route repair did not establish router
  presence.

## Disposition

This re-dispatched warning adds no new safe mesh-owned action: its Redmi portion duplicates the
already blocked exact follow-up, its gateway-swallow assertion is superseded by the verified live
route repair, and its inward-LAN uncertainty is a previously documented blind. Reject this
warning as a stale duplicate, retain the Redmi event gate, and keep LAN/router presence explicitly
unknown. No SSH probe, route, DNS, firewall, VPN, device, or service change was made.

## Verification

- `mesh-health` at 19:42:35Z: Redmi remains offline, last seen 11 days earlier.
- `ip -4 route get 100.76.0.1`: `dev enp42s0`; `ip -4 route show table 52`: connected-prefix
  throw plus Tailnet peer routes.
- `mesh-card --refresh` at 19:43:36Z: `exit-node-lan: ok`, `invariant-check: OK`.
- `mesh-lan-presence --nodes`: exit 1, router/LAN presence `UNKNOWN` for the stated visibility
  reasons.
- Canonical ledger: Redmi follow-up is blocked on the first successful port-8022 SSH probe;
  both cited earlier health-warning triages are complete.
