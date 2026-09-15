# Health-warning triage: `health-warning/6bb2518841e91cf12b61`

- Checked: `2026-09-11T23:54Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/6bb2518841e91cf12b61/triage`

## Verdict

The 2026-09-10 unreachable alert has recovered at the Tailscale transport
layer. The iMac is currently active and directly reachable, but authenticated
SSH remains unavailable from this node. This is a known access blind spot; the
current evidence does not justify changing routing, DNS, firewall, VPN, or
Tailscale state.

## Evidence

- `mesh-card --refresh` at `23:54:06Z` lists `imac-rozalia` as online.
- `tailscale status` at `23:54Z` reports the peer active with a direct path
  (`5.227.25.156:55351`).
- `tailscale ping --c 1 100.121.88.110` returned pong in 4 ms over that direct
  path.
- `ssh -o BatchMode=yes -o ConnectTimeout=8 100.121.88.110 'hostname; date -u; uptime'`
  reached the host but exited 255 with `Permission denied
  (publickey,password,keyboard-interactive)`.
- The source warning was emitted at `2026-09-10T06:48:52Z`, when the peer was
  last seen 10 minutes earlier and inactive. Current reachability differs from
  that observation.

Without authorized iMac credentials, this check cannot distinguish an
unaccepted key from remote SSH account or policy configuration.
