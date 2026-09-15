# health-warning/57cda9cdceeffe216822 — triage

Date: 2026-09-12 (UTC)  
Owner: `health`

## Verdict

The warning is still live: this node's default egress uses `tailscale0`, and its
configured exit node is `phaedra`, so the single-exit dependency remains. The
historical `ownership pending` note is outdated. VPN owns the repair chain, but
its requested `100.74.0.0/16` route target was rejected because the live LAN is
`100.76.0.0/16`; the task ledger still shows VPN's first step active after its
lease expired, so the repair remains unresolved. Health made no substrate
changes.

## Current evidence

- `mesh-dash --once check` at 15:46:36Z still showed egress on `tailscale0`,
  exit-node SPOF, local load making reachability probes unreliable, and eight
  fleet nodes down.
- `mesh-card --refresh` at 15:48:35Z exited 2 and reported `default-egress: dev
  tailscale0`, `exit-node: phaedra`, and the LAN gateway `100.76.0.1` swallowed
  by Tailscale table 52. Its live LAN address was `100.76.69.106`.
- `tailscale debug prefs` reported `ExitNodeID: n2sbt7yy6t11CNTRL`; current
  `tailscale status --json` identifies `phaedra` as `Online=true`, `Active=true`,
  `ExitNode=true`, with relay `tor`.
- `ip route get 1.1.1.1` returned `dev tailscale0 table 52`.
- `mesh-task status exit-node-lan-cgnat-repair-20260912` showed step 1 owned by
  `vpn`, active with lease through 15:33:07Z; health's independent verification
  remains open behind it. Dispatch checks for both steps returned 2 (refused).
- `docs/task-receipts/prove-and-restore-live-route-rejected-20260912.md` records
  VPN's rejection: the repair task targets `100.74.0.0/16`, while the connected
  LAN is `100.76.0.0/16`. The ledger still has not recorded the rejection as a
  structured transition.

## Disposition

Close this warning investigation as current and confirmed. Keep the known
egress/exit-node dependency open; health has no substrate claim and did not
change routing. The repair owner must reconcile the rejected step against the
live `100.76.0.0/16` scope before health's independent verification can become
eligible.
