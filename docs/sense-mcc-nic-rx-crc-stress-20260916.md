# MCC closure: `mesh-nic-rx-crc` → `mesh-stress`

Date: 2026-09-16

Closed the previously under-consumed producer link. `mesh-stress` now reads the live
`mesh-nic-rx-crc` and `mesh-nic-physical` JSON producers and publishes the joint relation
`CRC_SEEN × UP-CARRIER-FAULT → nic_rx_crc_joint=yes`, raising only the advisory `WARM` level.
Either physical axis alone remains descriptive; missing or malformed producer output is
`UNKNOWN` and the machine-facing consumer exits 2.

Evidence:

- `scripts/mesh-nic-rx-crc --test` — PASS; fixture plus real `/sys/class/net/*/statistics/rx_crc_errors` read.
- `scripts/mesh-nic-physical --test` — PASS; four relation cases plus real sysfs read (`enp42s0`).
- Focused consumer arms — PASS: positive `CRC_SEEN × UP-CARRIER-FAULT` → `WARM`; negative CRC-only → `CALM`; malformed CRC → `UNKNOWN`.
- Live producer reads at `2026-09-16T19:08:18Z`: `CLEAN`, `interfaces=2`, `rx_crc_errors=0`; `UP-CLEAN`, `iface=enp42s0`, `tx_carrier_errors=0`.
- Live consumer read: exit 2 for an unrelated unavailable stress axis, while publishing `nic_rx_crc_state=CLEAN`, `nic_physical_state=UP-CLEAN`, and `nic_rx_crc_joint=no`.
- `bash -n scripts/mesh-stress` — PASS; `git diff --check` — PASS.
- `mesh-doctor --test` — PASS; no `mesh-nic-rx-crc` orphan warning.

No commit made. The producer and consumer are both executable, and `rg -l 'mesh-nic-rx-crc'
scripts/mesh-*` now returns exactly the producer and `mesh-stress`.
