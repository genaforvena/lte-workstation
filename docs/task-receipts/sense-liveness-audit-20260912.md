# Sense liveness audit — 2026-09-12

Ran `mesh-reflex-health` and the live `mesh-sensorium` probe on `mesh-home`; this receipt records
one scheduled-but-blind sense and the fresh hardware read taken after its disposition was checked.

## Selected sense: LAN new-device detection

`mesh-reflex-health` reports `lan-newdevice(BLIND)`: its real LAN beat has been frozen for about
849,400 seconds, while `.lan-newdevice-blind` was touched at 2026-09-12 16:18:31Z. The recent blind
marker proves the scheduled path ran; it is not a current LAN reading. The beat itself is a
zero-byte file last modified 2026-09-02 20:24:22Z.

The scheduled caller is `mesh-perimeter` (`9-59/15` cadence), whose `lan_status_read` invokes
`mesh-lan-newdevice --status`. `mesh-lan-newdevice --test` passes its 11 fixture/assertion groups,
but the test does not establish a live DHCP/ARP read. The source already marks this organ
`DECAYED 2026-09-12` because its router DHCP and LAN ARP inputs are unreachable here; it also says
to retain it for revival and never read the blind marker as current LAN state. I verified and kept
that decay disposition. No schedule or source edit was needed.

`mesh-reflexes --check` reports dispatch OK and all desired reflexes present. That confirms scheduler
delivery, not LAN-organ liveness.

## Other live organ probes

- `mesh-presence --test` and `mesh-presence --log` both return `n/a` / exit 2: no Bluetooth adapter
  exists under `/sys/class/bluetooth`; the presence tape is not refreshed by inventing an empty
  scan.
- `mesh-sensorium` at 2026-09-12 16:20:57Z reports the local node reachable, Bluetooth absent, and
  a live Wi-Fi scan at 16:21:08Z with 0 APs in range.
- After checking the decay disposition, `mesh-therm` produced a fresh real hardware read at
  2026-09-12 16:21:07Z: NVMe Sensor 1 62.85°C, CPU Tctl 72.25°C, GPU 48.0°C (critical threshold
  90°C). This verifies a live sense artifact without turning the blind LAN input into an all-clear.
- The same sensorium run enumerated ALSA capture/playback devices at 16:21:17Z.

## Verification

- `rtk mesh-reflex-health`: 36 per-run reflexes fresh; `lan-newdevice` and `wifi-link` explicitly
  BLIND, with current blind markers and stale real-organ beats.
- `rtk mesh-lan-newdevice --test`: pass; fixture coverage only.
- `rtk mesh-reflexes --check`: dispatch OK; desired reflexes present.
- `rtk mesh-sensorium` and `rtk mesh-therm`: fresh live output captured above.
- No commit made. The pre-existing dirty worktree was preserved.
