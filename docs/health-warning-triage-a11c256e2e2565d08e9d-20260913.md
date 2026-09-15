# Health warning triage: path-watch relay fallback (2026-09-13)

Task: `health-warning/a11c256e2e2565d08e9d/triage`

The reported transition for `phaedra` is no longer live. The edge tape records
`phaedra mode=relay was=direct` at 16:19:01Z and recovery to
`phaedra mode=direct was=relay` at 16:29:01Z. The board alert at 16:24:01Z is
consistent with the watcher’s two-consecutive-pass debounce: relay at the
16:19 and 16:24 passes. At the current check (16:29:48Z), `mesh-path-watch
--status` reports `phaedra=direct`; live `tailscale netcheck` reports `UDP: true`.

The latest preceding netcheck sample in `~/.mesh/path-watch.log` is
`2026-09-13T15:49:01Z netweather udp=true derp=Helsinki lat_ms=33`. There is no
netweather sample at 16:24, so the tape cannot establish UDP’s value exactly at
the incident. The current code in `scripts/mesh-path-watch` derives relay from
an online peer with empty `CurAddr`; it boards the aggregate crossing when its
last cached UDP value is not `false`, and only boards `[path-udp-blocked]` on a
netcheck transition to UDP false. Thus this event records a peer path fallback,
not proof of a local UDP failure. Available state does not establish that
`phaedra` and `mesh-home` were on the same LAN, so that part of the alert text
cannot be validated from this node.

Disposition: stale for the reported `phaedra` episode because the peer
recovered to direct and the current UDP probe succeeds. No substrate change is
justified by this evidence. The state has since shown another peer (`imac-rozalia`)
on relay, so path instability may recur; if it does, inspect the paired peer
edges and contemporaneous netweather sample before attributing it to local UDP
or a same-LAN path.

Evidence gathered 2026-09-13 16:29–16:30Z:

- `~/.mesh/path-watch.log`, lines 3962 and 3964: `phaedra` relay at 16:19 and
  direct at 16:29; line 3963 records a separate `imac-rozalia` relay edge.
- `~/.mesh/path-watch.log`, latest preceding netweather sample: UDP true at
  15:49:01Z.
- `tailscale netcheck`: UDP true at 16:29:48Z.
- `mesh-path-watch --status`: `phaedra=direct` at 16:29:48Z.
- `scripts/mesh-path-watch`: peer-mode classifier and UDP alert/suppression
  logic (`cheap_lane`, `heavy_lane`).
