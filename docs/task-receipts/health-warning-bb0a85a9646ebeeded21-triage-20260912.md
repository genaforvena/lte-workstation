# Health warning triage: `health-warning/bb0a85a9646ebeeded21`

Checked 2026-09-12 11:27–11:29 UTC on `mesh-home`. Exact-owner dispatch validation exited 0; health claimed `health-warning/bb0a85a9646ebeeded21/triage`. This was a read-only triage; no substrate state was changed.

## Finding

The warning's LAN and routing findings remain current. `mesh-lan-presence --nodes` reports router unreachable and LAN visibility `UNKNOWN`. A refreshed card and `ip route get 100.76.0.1` both show the LAN gateway address routed through `tailscale0` in table 52. Default egress remains `tailscale0` with exit node `phaedra`, so the exit-node dependency remains a SPOF. The healer is still refusing the exclusion because `100.76.0.0/16` is outside its RFC1918-only eligibility rule; do not treat its green/pass state as recovery.

Tailscale state is dynamic: `imac-rozalia` is currently relayed through `hel`, while `phaedra` is direct and carries the exit node. The trace records a short relay transition for the data-server peer and phaedra followed by recovery to direct; it does not prove the iMac relay is fixed. DNS A for `api.anthropic.com` is still `160.79.104.10`, matching the warning's baseline.

The warning's `2F/34W` doctor count was not independently verified. The pane's `3F/34W` is cached from 09:32Z; a live `mesh-doctor` run printed the two known egress FAILs and the mic-default-device WARN but did not complete within the observation window, so it was interrupted. Do not infer a fresh total from the partial output. This establishes that the increase in the warning is not evidence the routing/LAN gaps recovered; the count itself remains an observation gap.

## Evidence

- `mesh-dash --once check` (11:27:44Z) showed default egress on `tailscale0`, supervised loops 4UP/0DOWN, 10 fleet nodes with 2 SSH/0 LAN/8 down, and `LOCAL LOAD HIGH` making reachability probes unreliable. The displayed doctor total is cached from 09:32:30Z.
- `mesh-lan-presence --nodes` (11:28Z) returned `UNKNOWN` with `router unreachable`; no host answered ICMP and the local node has no address in `192.168.8.0/24`.
- `mesh-card --refresh` (11:28:55Z) reported default egress `tailscale0`, exit node `phaedra`, and `100.76.0.1` swallowed by Tailscale table 52. `ip route get 100.76.0.1` confirmed `dev tailscale0 table 52 src 100.81.222.19`.
- `tailscale status` (11:29Z) showed `imac-rozalia` relayed via `hel`; `phaedra` direct at `38.49.216.141:41641` and active as exit node. `mesh-trace --tail 15` recorded a transient relay/recovery and repeated `[exit-node-lan-heal] REFUSED` for `100.76.0.0/16`.
- `dig +short A api.anthropic.com` returned `160.79.104.10`.
- Live `mesh-doctor` output exposed 2 egress FAILs and a mic default device WARN, but did not finish before interruption; full current totals remain unknown.

## Disposition

Keep LAN visibility UNKNOWN and Tailscale egress/exit-node SPOF open as known health gaps. The relay is a fluctuating observation, currently present for the iMac, and should be rechecked on a later pane. The doctor's warning count has a known freshness gap; do not claim the `2F/34W` delta as freshly reproduced. No substrate mutation was requested by this triage.
