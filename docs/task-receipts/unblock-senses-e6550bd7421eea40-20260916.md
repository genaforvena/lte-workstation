# Unblock receipt — ambient BLE feeder

- Task: `unblock/senses/e6550bd7421eea40/resolve`
- Parent: `senses-ambient-stale-followup-20260916/diagnose-stale-ambient`
- Checked: `2026-09-16T01:22:31Z`

## Live evidence

- `/sys/class/bluetooth` has no adapter entries.
- `bluetoothctl` is installed at `/usr/bin/bluetoothctl`, but `bluetoothctl list` exposes no controller.
- `mesh-presence --test` reports `no BT adapter on this node` and exits `2`.
- `/home/mesh-home/.mesh/presence.log` is unchanged since `2026-08-30 07:10:12 UTC` (size `1341845` bytes).
- The log contents are historical observations; they were not replayed or fabricated as a fresh reading.

## Disposition

No safe software-only prerequisite or fix is available in this node's scope: the required BLE radio or
fresh producer is absent. Keep the parent ambient sense `DATA-STALE` and retry only after
`event:first-successful-BLE-adapter-or-fresh-presence.log-write`.
