# Health-warning triage: `health-warning/5a1fd4103ba0b7f8ee4f`

- Checked: `2026-09-12T05:20Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/5a1fd4103ba0b7f8ee4f/triage`
- Source: `health@mesh-home`, `2026-09-09T01:37:44Z`, check-stream delta against `2026-09-08T19:33:55Z`: stale doctor count, LAN/router UNKNOWN, imac-rozalia changed from active/direct to offline, GL-MT3000 relay/offline, phaedra active/direct exit, and egress/DNS reported unchanged.

## Current read-only findings

- `mesh-dash --once check` at `05:19:46Z` reports 10 nodes, 2 SSH, 0 LAN, 8 down. It labels local reachability probes unreliable due to high load. The doctor result is cached from `04:32:09Z` and now reads `FAIL=3/WARN=33`, including egress over `tailscale0`, the configured exit-node SPOF, and a real `mesh-ble-heal` smoke failure. This is not a fresh comprehensive doctor run.
- `mesh-health` at `05:20:47Z` passes mesh-home and phaedra; it reports GL-MT3000, Redmi 10, ilya, imozerov-Default-string, imozerov-IdeaPad-3-15IIL05, and rip offline. It skips imac-rozalia because SSH authentication was refused.
- `tailscale status` shows phaedra active/direct and still the exit node. GL-MT3000 remains active-but-offline-last-seen-84d via relay. imac-rozalia is now active via relay `hel`; it is not currently offline, though mesh-health cannot authenticate over SSH. This is a real change from the source delta's offline observation, not proof of working SSH access.
- `mesh-lan-presence --nodes` returns rc=1 and `UNKNOWN (no local address in 192.168.8.0/24; router unreachable)`. Preserve UNKNOWN; this probe does not prove the host or router is down.
- `resolvectl status` currently lists `213.87.2.89` and `217.66.16.35` on `enp42s0`, plus Tailscale DNS `100.100.100.100` on `tailscale0`. No DNS mutation was made; this observation alone does not establish a historical DNS delta.
- Current `enp42s0` is `100.76.236.106/16` with main default via `100.76.0.1`, but policy rule 5270 selects table 52 first. `ip route get 1.1.1.1` and `ip route get 100.76.0.1` both choose `tailscale0`/table 52. A source-pinned ping to the current gateway on `enp42s0` gets 0/3 replies. Public egress is currently reachable according to the pane, but this does not verify the local gateway/LAN path.

## Disposition

Reconcile the historical check-stream report with the current evidence: the fleet remains degraded, LAN/router state remains UNKNOWN, egress still uses the Tailscale policy-table default, and the imac's tailnet presence has recovered to relay while SSH authentication remains refused. Keep the old `2F/33W` doctor count historical; the current pane carries a different cached `3F/33W` result. No routing, DNS, firewall, VPN, or peer mutation was made. Any route repair remains a separate single-writer operation requiring the health charter's `mesh-trace` claim, peer-route collision checks, and independently verifiable reachability before and after.

## Verification

- `mesh-dash --once check` — exit 0; current health pane consumed.
- `mesh-task queue --dispatch --owner 'health'` — returned this exact-owner row.
- `mesh-task check dispatch health-warning/5a1fd4103ba0b7f8ee4f/triage health` — exit 0 before claim.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/5a1fd4103ba0b7f8ee4f triage` — claimed by the exact owner.
- `mesh-health`, `tailscale status`, `mesh-lan-presence --nodes`, and `resolvectl status` — current read-only observations above.
- `ip route show table main`, `ip route show table 52`, `ip rule`, and `ip route get` — current policy-routing observations above.
- `ping -I enp42s0 -c 3 -W 1 100.76.0.1` — 3 transmitted, 0 received.
