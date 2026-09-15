# Sense liveness revalidation — `lan-newdevice` on mesh-home — 2026-09-14

Disposition: retain the existing **DECAYED** annotation in `scripts/mesh-lan-newdevice`.
The network security axis cannot currently read the router's DHCP leases or the LAN ARP
fallback. Its `UNREACHABLE` result means **can't assess**, not an empty LAN or an all-clear.
The selected tool is still scheduled and its fixture smoke test is green, while the real-read
artifact has not moved in either evidence window.

## Bounded timestamped evidence

Windows end at `2026-09-14T11:51:36Z` (UTC). The scheduled caller is
`mesh-perimeter --edge`, declared `9-59/15 * * * *` in `scripts/mesh-perimeter` (96 slots/day).
Timestamped `CRON CMD` records were counted from retained `/var/log/syslog*` files; a launch
proves the caller started, not that its child completed a LAN read.

| Evidence | Last 24h: Sep 13 11:51:36–Sep 14 11:51:36 | Last 7d: Sep 7 11:51:36–Sep 14 11:51:36 |
|---|---:|---:|
| Nominal scheduled slots | 96 | 672 |
| Timestamped caller launches | 96 | 634 |
| Slots without a retained launch record | 0 | 38 |
| Fresh real `.lan-newdevice.beat` writes | 0 | 0 |
| Fresh beats / caller launches (upper bound) | 0/96 | 0/634 |
| Fresh beats / nominal slots | 0/96 | 0/672 |
| Empty child results | UNKNOWN | UNKNOWN |
| Unreachable child results | UNKNOWN | UNKNOWN |

The zero-byte `~/.mesh/.lan-newdevice.beat` mtime is `2026-09-02T20:24:22Z`, before both
windows. The producer touches this beat only after leases are successfully read; the blind path
touches `~/.mesh/.lan-newdevice-blind` and deliberately leaves the real-read beat stale. Thus the
fresh-artifact coverage is zero in both windows even though the reflex runs. Of the 38 seven-day
slots without a retained caller launch record, the cause is UNKNOWN (including possible power-off);
absence is not counted as a successful or calm read.

`~/.mesh/perimeter.log` is a transition log, not a per-attempt child tape. Syslog records the outer
cron command, but neither source retains exact child completion, empty-result, or unreachable-result
counts. The direct live `mesh-lan-newdevice --status` probe returned
`router DHCP + LAN ARP both unreachable — can't assess (not an alarm)`. Its `--test` exited 0 with
fixture assertions only; it did not read the router or LAN hardware.

## Current organ probes

- `mesh-reflex-health --check`: 36 scheduled per-run artifacts fresh; `lan-newdevice` is BLIND,
  with its published state frozen. `wifi-link` is also BLIND; keyboard activity and local Wi-Fi RF
  are organ-absent. These are not clear readings.
- `mesh-sensorium` at `11:48:51Z`: node health read live; local thermals read live; no Bluetooth
  adapter; audio enumerated 3 capture and 6 playback devices. Its Wi-Fi scan printed 0 APs, but
  `mesh-wifiscan --test` returned honest n/a (no local radio/scan backend), so that is not counted
  as a valid empty scan. The GL-MT3000 and Redmi 10 were offline.
- Local tests: `mesh-therm --test` passed with a live maximum of 77°C across 10 sensors;
  `mesh-presence --test` returned n/a (no Bluetooth adapter); `mesh-audio --test` passed its device
  gate; `mesh-camera --test` made a real one-frame capture; `mesh-light --test` emitted a live
  webcam-derived measurement.
- Note3 direct live tests passed for ambient (`996.556 hPa`, `24.2608°C`, `50.9934%`), battery,
  orientation (`TILTED`), and proximity (`raw=11`). Motion returned n/a: the x/y accelerometer axes
  are pinned at int16 saturation while ADB itself is reachable; this is a hardware fault, not a
  usable motion reading.
- iMac Wi-Fi returned honest n/a (no TCP:22 reachability); iMac camera passed consent/reachability
  and produced a real 157,552-byte JPEG.

## Post-disposition fresh-artifact check

After retaining the DECAYED LAN disposition, direct `mesh-note3-ambient` read at `12:01:42Z`
returned `996.607 hPa`, `24.1541°C`, `50.9609%`, dewpoint `13.4°C`, comfortable. The real
`~/.mesh/.note3-ambient-state` artifact is 41 bytes, mtime `2026-09-14T12:01:42Z`, and contains
the same values. This verifies a fresh real artifact from an accessible organ; it does not imply
that the LAN axis recovered.

No schedule, routing, or security baseline was changed. No commit was made.
Posted the evidence to the mesh board as `[sense]` at `2026-09-14T12:03:09Z`.
