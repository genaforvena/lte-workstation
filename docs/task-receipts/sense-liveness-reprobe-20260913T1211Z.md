# Sense liveness re-probe — 2026-09-13 12:11 UTC

The `senses` pane showed `lan-newdevice` and `wifi-link` as blind. Re-read both live paths:

- `mesh-lan-newdevice --status` returned `router DHCP + LAN ARP both unreachable — can't assess
  (not an alarm)`. Fresh marker: `/home/mesh-home/.mesh/.lan-newdevice-blind`, mtime
  2026-09-13 12:11:44 UTC. This is a fresh unreachable attempt, not a real LAN reading; keep the
  verdict UNKNOWN/BLIND.
- `mesh-wifi-link --edge` exited 2 without a reading. Fresh offline marker:
  `/home/mesh-home/.mesh/.wifi-link-offline`, mtime 2026-09-13 12:10:50 UTC. The last state artifact
  `/home/mesh-home/.mesh/.wifi-link.state` remains at 2026-09-03 09:47:02 UTC, 5 bytes; it is stale,
  not a current Wi-Fi reading.

No eligible state recovery was visible. Re-probe when either organ becomes reachable; retain UNKNOWN
until it produces a fresh real read.

Wake prediction sharpened in `/home/mesh-home/.mesh/wake-expect/senses`: only the normalized CPU
frequency line with full `16/16` readability and the `(2m)` window is predicted as routine telemetry
jitter. Sensor verdicts, freshness changes, coverage changes, and board/task lines remain wake-worthy.
