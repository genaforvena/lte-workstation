# Health live-state follow-up — 2026-09-13

At 18:59Z, `mesh-dash --once check` returned the full `check` stream. It showed the local-load warning and cached doctor failures for egress via `tailscale0` and the configured exit node. The doctor section was 26 minutes old, so I refreshed the node card.

At 19:01:40Z, `mesh-card --refresh` exited 2 and regenerated `/home/mesh-home/.mesh-card`. The live invariant is violated: gateway `100.76.0.1` routes via `tailscale0 table 52`; exit node `phaedra` carries default egress; the connected `100.76.0.0/16` route is on `enp42s0` in the main table. `ip route get 100.76.0.2` independently returned `dev tailscale0 table 52`. The wired `mesh-exit-node-lan-heal` continues refusing this RFC6598 prefix under its RFC1918-only guard.

No route was changed. The exact prior route task, `exit-node-lan-cgnat-repair-20260912/prove-and-restore-live-route`, was rejected because it targeted stale `100.74.0.0/16`; its receipt says a corrected `100.76.0.0/16` write needs an explicit current scope and peer-route collision proof. The old health successor `independent-route-verification` still refuses dispatch (exit 2), and the old chain remains rejected/held. Existing health receipt `health-warning-391ad277f062ccf7c921-triage-20260912.md` independently records this same LAN-visibility blind.

I briefly wrote a `mesh-trace` claim while checking coordination, then withdrew it before any mutation. The trace records both the claim and withdrawal. No DMS switch was armed. The current alarm remains a known, live routing blind until a new route-proof/CGNAT-healer chain explicitly targets `100.76.0.0/16`, preserves more-specific Tailscale peer routes, and passes coordinated `mesh-dms` verification.

Verification: `mesh-card --refresh` exit 2; `ip route get 100.76.0.2` selected table 52; main-table route confirmed `100.76.0.0/16 dev enp42s0`; `mesh-task check dispatch exit-node-lan-cgnat-repair-20260912/independent-route-verification health` exit 2 (refused). No claim of recovery is made.
