# Sense: physical NIC carrier fault relation — 2026-09-16

Signal: the kernel's joint physical-link relation on `enp42s0`:
`/sys/class/net/enp42s0/carrier` plus
`/sys/class/net/enp42s0/statistics/tx_carrier_errors` (with
`carrier_changes` published as boot-scoped context). This is a real wire/PHY
signal not supplied by Wi-Fi RSSI, route reachability, or a software
operstate alone.

Implementation: `scripts/mesh-nic-physical`, already canonical and executable.
It emits `UP-CLEAN`, `UP-CARRIER-FAULT`, `DOWN-CLEAN`, or
`DOWN-CARRIER-FAULT`; missing or malformed sysfs returns exit 2. Successful
runs write `~/.mesh/.nic-physical.state` and call `mesh-state-touch`.

Wiring: `~/.mesh/reflexes.cron:352` contains
`*/5 * * * * $HOME/.local/bin/mesh-nic-physical --edge`.

Evidence:

- `mesh-nic-physical --test`: exit 0; fixture relation cases plus a real
  sysfs read of `enp42s0`.
- `mesh-nic-physical --json`: exit 0 at `2026-09-16T08:48:17Z`,
  `UP-CLEAN`, `carrier=1`, `tx_carrier_errors=0`, `carrier_changes=2`.
- `mesh-doctor --test`: exit 0; no orphan warning was emitted by the test.
- No commit was made for this request.

The full `mesh-doctor --quiet` observation also showed pre-existing unrelated
`mic DEFAULT device broken/busy` and `dispatch.log` error findings; they are
not attributed to this sense or changed here.
