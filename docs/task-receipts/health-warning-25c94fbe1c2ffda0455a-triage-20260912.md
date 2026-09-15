# Health warning triage: `health-warning/25c94fbe1c2ffda0455a`

Checked 2026-09-12 14:56–14:58 UTC on `mesh-home`, resuming the exact owner claim
`health-warning/25c94fbe1c2ffda0455a/triage` (`health`, lease to 15:09:04Z).

## Finding

The source [fyi] from 2026-09-11 05:01Z says `route:no | PROPOSE none (retired
2026-09-07T08:59:10Z) | CHANGED wip parked c8a6cca6 | GAP health work remains parked`.
The retired route proposal remains retired, but a fresh card refresh confirms that the
underlying LAN-routing invariant is still violated: the local LAN gateway `100.74.0.1`
resolves through `tailscale0` in table 52 while `phaedra` is the configured exit node.
The local LAN address is now `100.74.16.184`; the live card reports the same swallowed
LAN route and marks the invariant violated. This is a known blindness, not a repaired
alarm.

## Evidence

- `mesh-dash --once health` at 14:56:47Z refreshed the pane; its health data frame was
  empty apart from the node card metadata, so it supplied no current fleet-health rows.
- `mesh-card --refresh` at 14:58:05Z reported default egress `tailscale0`, exit node
  `phaedra`, and `100.74.0.1` swallowed by table 52 rather than the LAN link; its output
  explicitly reported an invariant violation.
- `mesh-health` at 14:57:36Z passed `mesh-home` and `phaedra`; it reported six offline
  peers (GL-MT3000, Redmi 10, ilya, imozerov-Default-string,
  imozerov-IdeaPad-3-15IIL05, rip) and skipped `imac-rozalia` because SSH authentication
  was refused. This is the observed fleet state, not a full reachability guarantee.
- `mesh-reflex-health` found 36 per-run reflexes fresh, while explicitly marking
  `lan-newdevice` and `wifi-link` organ-blind, `kbd-activity` and `wifi-rf` organ-absent,
  and `exit-node-lan-heal` value-frozen for 22,070 seconds. Recent trace marks repeatedly
  say the healer refuses the LAN exclusion because `100.74.0.0/16` is outside its
  RFC1918-only eligibility rule.
- `git show c8a6cca6` identifies the cited object as a WIP snapshot from
  2026-09-11 04:55:02Z. The current working tree contains extensive unrelated dirty and
  untracked work, which this triage left untouched.

## Disposition

Close this exact investigation with the confirmed violation recorded as a known health
blindness. No routing or other substrate state was changed: this receipt is the
read-only triage, and a route repair must follow `docs/coordination.md`'s single-writer,
trace claim, tmux coordination, and `mesh-dms` procedure as its own scoped action. The
next concrete action is to repair the healer's CGNAT/LAN-prefix eligibility and re-apply
only the verified LAN exclusion under that procedure, then verify with
`ip route get 100.74.0.1`, `mesh-health`, and `mesh-card --refresh`.
