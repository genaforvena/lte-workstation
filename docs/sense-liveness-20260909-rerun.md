# Sense liveness rerun — 2026-09-09T04:34Z

## Disposition

`lan-newdevice` is honestly decayed/BLIND, not repaired. Its scheduled `--status` path
ran at 2026-09-09T04:34Z and returned:

```text
router DHCP + LAN ARP both unreachable — can't assess (not an alarm)
```

The source artifact is therefore not fresh: `mesh-reflex-health --check` reports the last
real LAN read frozen for `547827s`, while the declared blind marker was touched `34s` ago.
That proves the reflex is scheduled/alive but the organ is away; no fake LAN-clear was minted.

## Health and organ probes

`mesh-reflex-health --check`: rc 0; 38 per-run reflexes fresh; `lan-newdevice`, `proximity`,
and `wifi-link` are `organ-blind`; `kbd-activity` and `wifi-rf` are honest organ-absent.

Smoke matrix: `mesh-sensorium` rc 0; `mesh-wifi-motion` rc 0; `mesh-ambient-clock` rc 0;
`mesh-operator-state` rc 0; `mesh-sense-monitor` rc 0; `mesh-sensor-log` rc 0;
`mesh-arrivals` rc 0; `mesh-macsocks-health` rc 0. `mesh-location`, `mesh-light`,
`mesh-room-sense`, `mesh-situation`, and `mesh-lan-newdevice` timed out under the bounded
smoke probe; `mesh-body-motion` rc 2 (organ absent). A timeout is retained as UNKNOWN, not
called green.

## Fresh real artifact after disposition

`mesh-power --status` at 2026-09-09T04:34Z performed the local power read and returned:

```text
power: MAINS status=no-battery
```

No source, deployed script, router, or scheduler configuration was changed. No commit made.
