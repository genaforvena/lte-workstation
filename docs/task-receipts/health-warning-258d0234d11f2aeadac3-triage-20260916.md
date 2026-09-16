# Health warning triage: imac-rozalia unreachable

Task: `health-warning/258d0234d11f2aeadac3/triage`

Fresh read-only evidence at `2026-09-16T07:43:28Z`:

- `mesh-health --once` reported `OFFLINE imac-rozalia 100.121.88.110`, with
  tailnet last-seen `43m ago`, `active=False`, and no off-tailnet fallback.
- `tailscale status --json` reported `HostName=imac-rozalia`, `Online=false`,
  `Active=true`, `Relay=hel`, empty `CurAddr`, and
  `LastSeen=2026-09-16T07:00:00.1Z`.
- `tailscale ping --c 2 --timeout 5s imac-rozalia` timed out twice with no reply.

Disposition: confirmed current unreachable state. No safe local actuator exists:
the target has no LAN fallback and this node has no SSH path. Preserve as a
known fleet blind spot rather than changing routing, DNS, VPN, or firewall state.

Retry edge: rerun `mesh-health --once` and the two-ping Tailscale probe after the
iMac returns online/active or a LAN fallback is registered; then verify SSH and
reassess whether the warning clears.

Delegation: none. This was tightly coupled single-warning triage; I personally
inspected the live command outputs above and this receipt.
