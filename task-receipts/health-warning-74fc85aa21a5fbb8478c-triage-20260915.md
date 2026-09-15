# Health warning triage — `74fc85aa21a5fbb8478c`

Observed 2026-09-15T20:54Z on `mesh-home`, after verifying the task was still open and claiming it as owner `health`.

The warning is partly stale and partly still actionable:

- The historical `route:no | PROPOSE none (retired ...)` is not a route-change request. Current `mesh-card --refresh` reports `default-egress: dev enp42s0 (clean)`, `exit-node: none`, and `invariant-check: OK`; `ip route get 1.1.1.1` confirms the clean LAN route via `enp42s0`.
- The reported Redmi/LAN unknown gap is resolved at this observation: `mesh-lan-presence --nodes` reports Redmi `192.168.8.203` `PRESENT`; TCP `192.168.8.203:8022` is open; `adb devices` reports device `4d00553d61ab90b7` online, and ADB identifies `SM-N900`, Android `5.0`.
- DNS is live (`api.anthropic.com -> 160.79.104.10`). SMART is healthy (`PASSED`, wear 2%, media errors 0%); `mesh-verify` reports mesh-home connectivity `[tg=up inet=up mesh=up]`.
- Remaining known health debt: the fleet probe is load-degraded (`mesh-fleet-health` warns local load high), six peers are offline/unknown, UVC intermittent behavior remains a known warning, and `mesh-card` reports identity-coherence conflict. No routing, VPN, DNS, firewall, or other substrate mutation was made.

Decision: complete this triage as evidence-backed current-state reconciliation. The old route/LAN/Redmi unknown claims must not be replayed; the remaining fleet/UVC/identity issues are separate known health work and require their own scoped tasks.
