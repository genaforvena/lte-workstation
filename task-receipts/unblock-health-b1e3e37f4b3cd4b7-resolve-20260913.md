# Root-cause access blocker resolver — 2026-09-13

Resolver task: `unblock/health/b1e3e37f4b3cd4b7/resolve`.

The missing prerequisite is external, not a mesh-owned registration or code path: at 17:13Z the GL-MT3000 Tailscale peer was offline, both the tailnet address and household gateway were silent from mesh-home, and the previously tried router SSH key had been rejected. No timestamped router log export was available. Mesh-home is on a separate uplink, so its own network status cannot substitute for household-router WAN or radio evidence.

The mesh-owned recovery is complete. The exact operator-owned prerequisite is registered as
`wifi-router-router-access-20260913/establish-router-readonly-access`: establish a router-authorized read-only SSH/API path reachable from mesh-home, or provide a timestamped export of WAN status, uptime, radio state, and system logs covering an outage. The parent `wifi-router-periodic-outage-20260913/root-cause-access` records this task ID in its blocker and remains typed-blocked until that task is satisfied.

There is no safe mesh-side action that can authorize access to the router or produce its logs from this node's separate uplink. No credentials were attempted, no router setting was changed, and no root cause is claimed. Leave the parent blocked; retry only when the operator-owned task supplies the authorized read path or timestamped export.

Evidence: [root-cause access receipt](root-cause-access-wifi-router-periodic-outage-20260913.md); [correlation receipt](correlate-outages-wifi-router-periodic-outage-20260913.md); current `tailscale status --json` and `mesh-peer-addr router` results.
