# Router access blocker — health resolver — 2026-09-13

Task: `unblock/health/d01f92cf297b2048/resolve`.

## Current evidence

At 17:40Z, `mesh-dash --once check` showed GL-MT3000 in the fleet down list and warned that
local load made reachability probes unreliable. It showed the GPU at 8899/12288 MiB (72%),
so the earlier 92% VRAM alarm in the restored handoff is no longer current in this pane sample.

I checked the router directly rather than relying on the fleet summary:

- `tailscale status --json` reported GL-MT3000 (`100.105.241.84`) with `Online: false`; its
  last-seen timestamp remains `2026-06-19T07:11:27.1Z`.
- `mesh-peer-addr router` reported both `100.105.241.84` and LAN gateway `192.168.8.1` silent,
  and explicitly returned the tailnet IP as a guess rather than a reachability result.
- `wifi-router-router-access-20260913/establish-router-readonly-access` is still open and owned
  by `operator`; the outage chain's `root-cause-access` remains blocked on `operator-input`.

## Exact operator action

Satisfy the existing operator-owned access task using either path below:

1. Bring the GL-MT3000 online and reachable from mesh-home, then provision an operator-authorized
   **read-only** SSH/API identity that can return WAN status, uptime, radio state, and system logs.
   Share only the approved account/endpoint locator through the credential mechanism; do not put
   credentials or private keys in chat or the repository. The previously rejected key must not be
   retried.
2. Provide a timestamped export of WAN status, uptime, radio state, and system logs spanning the
   reported 2026-09-13 interruption(s), preserving router source timestamps and naming the time
   zone. Existing reports were around 16:11Z and 16:26Z; exact onset and recovery remain unknown.

After one path is actually available, attach its evidence to
`wifi-router-router-access-20260913/establish-router-readonly-access`, mark that prerequisite
complete, then resume `wifi-router-periodic-outage-20260913/root-cause-access` and correlate the
router timeline with the existing host-side evidence. Keep `repair-verify` closed until a cause
and repair authority are established.

No router credentials were attempted and no router or network configuration was changed. The
missing authorization or router-side telemetry is external to this node; the root-cause task stays
blocked until that prerequisite is satisfied.

Evidence: live `mesh-dash --once check`, `tailscale status --json`,
`mesh-peer-addr router`, and `mesh-task status` for the resolver, access prerequisite, and outage
chains at 17:40Z; [root-cause access receipt](root-cause-access-wifi-router-periodic-outage-20260913.md);
[prior resolver packet](unblock-health-065ff847758a2d55-resolve-20260913.md).
