# Independent verification — connected LAN route repair

Task: `exit-node-lan-cgnat-live-repair-20260914/independently-verify-live-cgnat-repair`  
Observed: 2026-09-14 06:38–06:40 UTC

## Deployment and reflex

The repository source and deployed `/home/mesh-home/.local/bin/mesh-exit-node-lan-heal` have the
same SHA-256: `b80b07442647cb4807f296ee045ab6d9c153db4a5a952c7785144614af93e9b2`. The deployed
`--test` passed, covering the live-connected RFC6598 gate, refusal arms, dry-run no-write, and
more-specific tailnet peer precedence; `bash -n scripts/mesh-exit-node-lan-heal` passed. A live
`--check` reported no action required in the LAN, Docker, rescue, or extra-prefix legs and stated
that it writes no run row.

The actual cron wiring is present in `/home/mesh-home/.mesh/reflexes.cron`:
`* * * * * $HOME/.local/bin/mesh-exit-node-lan-heal ...`. The separate unconditional run tape
advanced through `2026-09-14T06:40:06Z` with `RUN exit-node=present peer=phaedra lan=ok ... rc=0`;
its mtime advanced with those rows. `mesh-reflex-health` also reported an overwrite-only
`value-frozen` note for `exit-node-lan-heal` (the content axis). That axis is the last-application
state (`last-applied=2026-09-14T05:47:04Z`, last applied net `100.76.0.0/16`), not the cadence
artifact. The fresh one-minute RUN tape is the explicit liveness denominator and records the
current `lan=ok` result. This is a stable no-action state, not a dead reflex; no freshness repair is
warranted by this warning.

## Current route and reachability

`mesh-card --refresh` at 06:38:23Z reported `exit-node-lan: ok` for live address
`100.74.139.143/16` on `enp42s0`, public IP `38.49.216.141`, upstream `ok`, and
`invariant-check: OK`. Fresh main-table reads showed default via `100.74.0.1 dev enp42s0` and the
connected route `100.74.0.0/16 dev enp42s0`. Table 52 has default on `tailscale0`, retains throw
routes for the current `100.74.0.0/16` and former `100.76.0.0/16` local ranges, and keeps the
listed tailnet peer `/32` routes on `tailscale0`. The policy rule still selects table 52 for
unmarked traffic.

FIB lookups returned:

- `100.74.0.1` and `100.74.254.254` → `dev enp42s0`.
- Phaedra `100.94.116.17` → `dev tailscale0 table 52`.
- Exit-node public endpoint `38.49.216.141` → `via 100.74.0.1 dev enp42s0` (rescue path).
- Public target `1.1.1.1` → `dev tailscale0 table 52`.

`curl -fsS --max-time 15 https://api.ipify.org` returned `38.49.216.141`, matching the refreshed
card. `mesh-health` exited 0 with mesh-home and phaedra reachable; the other previously listed
peers remain offline. No route or policy-rule write was performed.

## Disposition and verification

All route, deployed-source, reflex-wiring, freshness, card, and host-egress gates pass. The earlier
100.74/100.76 poll difference was a real DHCP prefix change; each verification used the prefix,
gateway, interface, and source address live at that reading. The healer's own current run tape and
`--check` agree with the fresh FIB. The overwrite-only note describes an unchanged last-application
record and does not justify changing the healer or reflex-health mapping.

Commands read during verification: `sha256sum`, deployed `mesh-exit-node-lan-heal --test`,
`bash -n`, `mesh-exit-node-lan-heal --check/--runs`, `mesh-card --refresh`, `mesh-health`, current
`ip -4 addr/route/rule` reads and FIB lookups, the one-minute reflex stanza and run tape, and the
read-only public-IP request. No DMS was armed or cancelled because no substrate mutation was
attempted.
