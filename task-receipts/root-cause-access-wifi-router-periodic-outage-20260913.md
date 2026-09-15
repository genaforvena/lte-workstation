# Router root-cause access gate — 2026-09-13

At 2026-09-13 17:13Z, `wifi-router-periodic-outage-20260913/root-cause-access` was still open in the live chain and was assigned to `health`. The prior actuator and correlation receipts remain current for the relevant window: no direct router writer or actuator timing match was found, and router-side cause is unproven.

## Current access check

- `tailscale status --json` reports `GL-MT3000` (`100.105.241.84`) offline.
- `mesh-peer-addr router` reports the tailnet address and household gateway `192.168.8.1` silent from mesh-home. The returned tailnet address is only a guess, not evidence of reachability.
- The correlation receipt records that the prior router SSH key was rejected. No new router-authorized read-only SSH/API identity or router log export is present in the repository or active task ledger.
- The health charter says this node is on a separate mobile/wired tether path. It is not a synchronized household-LAN vantage, and no outage is currently being reported for a contemporaneous sample.

I did not retry the rejected key, attempt credentials, or infer router state from mesh-home's separate uplink. The requested WAN, uptime, radio, and system-log evidence is unavailable through authorized access at this time.

## Exact external prerequisite and retry

There was no existing active task for the router authorization gate, so I created
`wifi-router-router-access-20260913/establish-router-readonly-access` (owner `operator`). It requires either:

1. router reachability from mesh-home plus a router-authorized read-only SSH/API identity that can read WAN state, uptime, radio state, and system logs; or
2. a timestamped export of those same router fields and relevant system logs covering a reported outage.

No credential or private key should be posted to chat or committed. `root-cause-access` is linked behind this exact prerequisite and remains queued until it completes. Retry this step when the authorized read path is usable or the timestamped router export is available; then capture the requested evidence and preserve source timestamps.

The downstream `repair-verify` step must remain closed to execution until router evidence establishes a cause and the applicable repair authority is clear.

Evidence: live task-chain status; `tailscale status --json`; `mesh-peer-addr router`; [correlation receipt](correlate-outages-wifi-router-periodic-outage-20260913.md); [actuator audit](audit-actuators-wifi-router-periodic-outage-20260913.md).
