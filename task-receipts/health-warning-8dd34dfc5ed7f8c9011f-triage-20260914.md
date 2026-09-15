# Health roll-call triage — retired route marker, egress classification, and path delta

Task: `health-warning/8dd34dfc5ed7f8c9011f/triage`  
Source: `health@mesh-home` FYI at 2026-09-14T00:02:17Z.

## Findings

`route:no | PROPOSE none (retired 2026-09-12T11:44:45Z)` is a historical marker, not a route-change
request. The old `egress FAIL` is superseded by the completed role-aware `mesh-doctor` correction:
the node intentionally consumes Phaedra's exit route, which the doctor now reports as a NOTE while
checking LAN-prefix FIB separately. The exact-owner correction task is complete, with regression
tests and source/deployed parity recorded in `mesh-doctor-egress-policy-20260914.md`.

The captured samples show current egress passing. The latest egress log entries at 21:16:40Z and
21:18:01Z report US egress through `path=route`, public IP `38.49.216.141`, Anthropic `405`, and
quality `0%` loss at about `134 ms`. The rolling baseline is `0/439` bad with 37 unattributed
observations. The configured exit-node dependency remains a real single-node availability risk;
these samples do not show a current egress failure.

The Tailscale path is variable: `mesh-path-watch --status` at 21:14:01Z showed imac-rozalia direct,
then at 21:19:01Z showed it on relay, with Phaedra direct and no other relays. The 21:20Z pane
reported PATH degraded with one relay, while egress remained OK. Record this as intermittent imac
relay use; there is no evidence here of lost Phaedra exit-node reachability.

LAN/router presence remains UNKNOWN. A fresh `mesh-lan-presence --nodes` attempt produced no result
within 20 seconds (exit 124); prior health receipts document that the probe cannot see the
192.168.8.0/24 segment from this node. Keep that visibility gap explicit and retry when that segment
or a known host becomes reachable. The doctor's current pane value is a 46-minute-old cache; a
bounded live `mesh-doctor --quiet` run emitted the expected exit-node consumer NOTE but timed out at
90 seconds (exit 124), so it did not produce a fresh aggregate.

## Disposition

No actionable route proposal or safe substrate repair is present in this roll-call. Preserve the
retired route marker, current passing egress, intermittent imac relay observation, LAN/router
visibility gap, and egress-attribution gap as separate facts. Do not change the existing route hold
without operator release. No route, rule, DNS, firewall, VPN, or Tailscale state was changed.

## Verification

- Read the source line from `/home/mesh-home/.mesh/chat.log` and the structured task ledger.
- `mesh-dash --once check` at 21:20:18Z: one peer relay, egress OK, 37 unattributed 24-hour
  observations, and cached doctor `FAIL=0 WARN=33`.
- `mesh-path-watch --status` at 21:14:01Z and 21:19:01Z: imac direct then relay; Phaedra direct.
- Egress log through 21:18:01Z: two current OK samples; `0/439` bad and 37 unattributed.
- `mesh-lan-presence --nodes` bounded at 20 seconds: exit 124, no result.
- `mesh-doctor --quiet` bounded at 90 seconds: policy-aware exit-node NOTE observed; exit 124 before
  aggregate completion.
- `mesh-task check dispatch health-warning/8dd34dfc5ed7f8c9011f/triage health`: exit 0; exact
  owner `health` claimed the row.
