# Router root-cause access blocker — health resolver — 2026-09-13

Task: `unblock/health/065ff847758a2d55/resolve`.

## Live evidence

At 17:27Z, `mesh-dash --once check` showed GL-MT3000 in the down fleet list and the
router investigation still lacked router-side telemetry. The same stream reported a high local
load and warned that reachability probes were unreliable, so I treated its fleet summary as a
lead and checked the target directly.

- `tailscale status --json` reported `GL-MT3000 100.105.241.84 false` (offline; last seen
  `2026-06-19T07:11:27.1Z`).
- `mesh-peer-addr router` reported the tailnet peer and `192.168.8.1` both silent; it returned
  `100.105.241.84` explicitly as a guess, not a reachability result.
- `ping -c 2 -W 2 192.168.8.1` received 0/2 replies; `tailscale ping --c 1 100.105.241.84`
  timed out.
- `wifi-router-router-access-20260913/establish-router-readonly-access` remains open and owned by
  `operator`. The upstream `wifi-router-periodic-outage-20260913/root-cause-access` remains typed
  blocked pending that prerequisite.

## Exact operator action

Complete the operator-owned access task by supplying either of these:

1. Make the GL-MT3000 reachable from mesh-home and establish an operator-authorized **read-only**
   SSH/API identity that can retrieve WAN status, uptime, radio status, and system logs. Keep
   credentials out of chat and the repository; provide only the authorized account/endpoint
   locator through the approved credential mechanism.
2. Provide a timestamped export of those same fields plus system logs spanning the reported
   2026-09-13 interruption(s). Preserve the router's source timestamps and identify the time zone;
   exact onset/recovery are currently unknown, and existing reports were around 16:11Z and 16:26Z.

Once either input is available, mark `wifi-router-router-access-20260913/establish-router-readonly-access`
complete with its evidence artifact. Then resume `wifi-router-periodic-outage-20260913/root-cause-access`
and correlate the router evidence against the existing host-side timeline. Do not retry the rejected
SSH key, infer router health from mesh-home's separate uplink, or execute a repair before a cause and
repair authority are established.

No router credential was attempted and no router or mesh configuration was changed. This resolver
cannot satisfy the operator-owned prerequisite from this node; leave the parent outage task blocked
until the access task is actually satisfied.

Evidence: direct live probes above; [root-cause access receipt](root-cause-access-wifi-router-periodic-outage-20260913.md);
[correlation receipt](correlate-outages-wifi-router-periodic-outage-20260913.md); operator prerequisite
chain status captured at 17:27Z.
