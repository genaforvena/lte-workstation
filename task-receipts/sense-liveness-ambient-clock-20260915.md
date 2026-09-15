# Sense liveness — ambient-clock — 2026-09-15

Decision: honestly decayed; no repair attempted. The source and crontab already carry the
`DECAYED`/orphan marker dated 2026-09-10/11. The live organ cannot be repaired on this node:
`/sys/class/bluetooth` is empty and `mesh-presence` reports no adapter.

## Bounded evidence

Windows are UTC and end at 2026-09-15T21:09:51Z.

| window | declared cadence slots | observed cron launch lines | real reads | empty/unreachable | fresh artifact coverage |
|---|---:|---:|---:|---:|---:|
| 24h: 2026-09-14T21:09:51Z → now | 48 | 0 | 0 | 1 current probe | 0/48 |
| 7d: 2026-09-08T21:09:51Z → now | 336 | 0 | 0 | 1 current probe; historical result rows absent | 0/336 |

The cadence slots are the declared `6-59/30 * * * *`; the current crontab line is commented
with `DECAYED`, so no current schedule is enacted. `syslog`, `syslog.1`, and archived
`syslog.*` contain no `mesh-ambient-clock` launch line in either bounded window. This is
history absent, not evidence of calm. The last real feeder artifact is `~/.mesh/presence.log`,
mtime 2026-08-30T07:10:12Z, 23,879 minutes old at the probe. The ambient state is only
`DATA-STALE`, mtime 2026-09-11T14:34:52Z; `ambient-clock.log` is zero bytes and unchanged
since 2026-07-14.

## Probes and fresh post-decision artifact

- `mesh-reflex-health --check`: smoke-green overall; no fresh ambient-clock real artifact.
- `mesh-sensorium --compact`: live therm/audio/card probes returned artifacts; presence and
  Wi-Fi were unavailable. This covered each node-local organ exposed by the compact sensorium.
- `mesh-ambient-clock --test`: PASS (classifier/smoke suite only; not hardware evidence).
- `mesh-presence --json` at 2026-09-15T21:09:51Z: `status=unreachable`,
  `reason=no BT adapter on this node`, exit 2.
- `mesh-ambient-clock --json` at 2026-09-15T21:09:51Z: `label=DATA-STALE`,
  `data_stale=true`, `scan_count=0`, `detail=presence.log ... > adaptive 20min threshold`,
  exit 2.

The two timestamped JSON results above are the fresh real post-decision artifact: they verify
the decay remains honest and that no stale BLE value is being presented as live.

No commit made.
