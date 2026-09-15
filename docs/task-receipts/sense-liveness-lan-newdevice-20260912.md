# Sense liveness — `lan-newdevice` — 2026-09-12

`mesh-reflex-health` reports `lan-newdevice` as `BLIND`: its last real LAN reading is frozen,
while the scheduled run's blind marker is fresh. The sense was already explicitly declared
`DECAYED` in `scripts/mesh-lan-newdevice`; this live recheck confirmed that disposition, so I
refreshed the declaration date rather than presenting the old LAN reading as current.

Evidence from 2026-09-12 around 02:23 UTC:

- `~/.mesh/reflexes.cron` schedules `mesh-perimeter --edge` every 15 minutes; `mesh-perimeter`
  calls `mesh-lan-newdevice --status` for its NETWORK axis.
- `mesh-lan-newdevice --test` — PASS (offline parser/fusion assertions; not treated as hardware
  evidence).
- Live `mesh-lan-newdevice --status` — exit 0, output:
  `router DHCP + LAN ARP both unreachable — can't assess (not an alarm)`.
- The live attempt left the fresh blind marker
  `~/.mesh/.lan-newdevice-blind` (final verification mtime `2026-09-12 02:25:31 UTC`); the last real LAN beat
  `~/.mesh/.lan-newdevice.beat` remains at `2026-09-02 20:24:22 UTC`. Source and deployed tool
  are byte-identical.
- `mesh-reflex-health --check` continues to classify `lan-newdevice` as `BLIND`, explicitly
  distinguishing the fresh scheduled attempt from the stale published LAN value.
- Final verification: `mesh-lan-newdevice --test` passed; a second live `--status` again reported
  both sources unreachable. `mesh-reflex-health --check` exited 1 for the existing stale set and
  node load warning, while its `lan-newdevice` line said the blind marker was touched 2s ago.

This is a decayed/unavailable LAN sense, not a clean-network verdict. Recovery requires the router
DHCP or local LAN-neighbor organ to become reachable, followed by a fresh real `--status` read.

Sensorium organ survey (`mesh-sensorium`, 02:17 UTC): thermal and audio devices produced live
readings; Bluetooth has no adapter on this node; Wi-Fi scan found 0 APs. `mesh-sense-monitor`
reported phone/Wi-Fi inputs unreachable and the room state uncertain. No unreachable organ was
interpreted as quiet or clear.
