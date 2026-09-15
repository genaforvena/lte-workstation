# Health-warning triage: `health-warning/2c63ee569e1bd25a3917/triage`

Date: 2026-09-11T20:56:55Z  
Task: `health-warning/2c63ee569e1bd25a3917/triage`

## Fresh read-only evidence

- `mesh-dash --once check` at 2026-09-11T20:56:16Z carried the source warning:
  `Redmi — UNREACHABLE`, tailnet last-seen 8d ago, `active=True`,
  `ASLEEP-OVERDUE`: unreachable 343m beyond its own 330m bound.
- `mesh-health` at 2026-09-11T20:56:55Z reported `OFFLINE Redmi 10` at
  `100.103.99.16`, with tailnet last-seen 8d ago and `active=True`.
- `tailscale status --json` identifies the peer as `Redmi 10`,
  `Online=false`, `Active=true`, last seen `2026-09-03T09:53:36.1Z`.
- `tailscale ping --c 1 100.103.99.16` timed out with no reply.

## Disposition

KNOWN EXTERNAL UNAVAILABILITY / KNOWN BLINDNESS: the Redmi peer remains
offline and overdue beyond its declared sleepy bound. There is no safe local
substrate action that can revive an unavailable body, and no routing, DNS,
firewall, VPN, WireGuard, Tailscale, or service mutation was made. Retry on a
new health delta or a named operator/body-revival decision.
