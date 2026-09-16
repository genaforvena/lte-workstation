# Unblock receipt — ambient BLE feeder

- Task: `unblock/senses/b6da3cdc48237943/resolve`
- Checked: `2026-09-16T01:14:23Z`

## Live checks

- `mesh-dash --once senses` returned immediately but emitted no captured text in this shell.
- `/sys/class/bluetooth` has no controller entries.
- `bluetoothctl show` reports `No default controller available`.
- `scripts/mesh-presence --test` reports `n/a (no BT adapter on this node)` and exits 2.
- `~/.mesh/presence.log` mtime is `2026-08-30 07:10:12 UTC` (1,341,845 bytes); it was not touched
  or replayed.

## Disposition

No safe software-only prerequisite or repair exists: the required BLE radio/producer capability is
absent. Preserve the parent ambient state as `DATA-STALE`; retry only on
`event:first-successful-BLE-adapter-or-fresh-presence.log-write`.
