# Sense liveness re-probe — 2026-09-12 06:37 UTC

`mesh-reflex-health` identifies `lan-newdevice` as `organ-blind`: its scheduled runner is active,
but the last real LAN beat is stale. The organ remains honestly marked `DECAYED`; no false all-clear
or repair of the unreachable router/LAN was attempted.

Evidence:

- Crontab runs `mesh-perimeter --edge` every 15 minutes; that caller invokes
  `mesh-lan-newdevice --status` for its NETWORK axis.
- `mesh-reflex-health` (default and `--check`) reports `lan-newdevice` BLIND: its last real read
  froze at 2026-09-02 20:24:22 UTC. The blind marker was fresh at 2026-09-12 06:36:10 UTC, so the
  scheduled path is alive while the LAN reading is not current. The command exits 1 because the
  wider stale set is non-empty; this is not an all-clear.
- `mesh-lan-newdevice --test` passes 15 offline/parser/fusion groups. It is smoke evidence only,
  not a hardware read. The deployed and source files are byte-identical (SHA-256
  `0dfc0b6b986197f162c40968f041965150dfed2ecdb5d61a1db2c2a09318c7ad`) and both carry
  `orphan-ok: DECAYED 2026-09-12`.
- Sensor probes: `mesh-room-sense` and `mesh-body-motion` report phone/BLE unreachable (exit 2);
  `mesh-wifi-link` reports phone unreachable (exit 2); battery and battery-energy/voltage report no
  local battery (exit 2); `mesh-wifi-rf` and `mesh-kbd-activity` report absent organs (exit 2).
  Local probes passed: activity-light (fusion fixtures), battery-rate (fixtures), NVMe
  power-state (real runtime-PM read), NIC TX (real counter), link-speed (live sysfs), link-duplex
  (real `enp42s0` read), thermal-zone (sysfs present), and IRQ-rate (live split).
- After the survey, `mesh-nvme-power-state` wrote a fresh real artifact at 2026-09-12 06:36:35 UTC:
  `~/.mesh/.nvme-power-state` = `ACTIVE|2|2|0|2026-09-12T06:36:35Z`.
- `mesh-reflex-census --test` passes. No repository source or schedule was changed and nothing was
  committed.

Recovery for the decayed LAN sense: wait until router DHCP or local LAN ARP is reachable, then take
a fresh real `mesh-lan-newdevice --status` reading and reassess the decay marker.
