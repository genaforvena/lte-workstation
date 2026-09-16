# Unblock receipt — ambient BLE feeder

- Task: `unblock/senses/bf3fab35cab3210f/resolve`
- Parent: `senses-ambient-stale-followup-20260916/diagnose-stale-ambient`
- Checked: `2026-09-16T01:07:46Z`

Evidence:

- `/sys/class/bluetooth` is empty on `mesh-home`.
- `bluetoothctl show` returns `No default controller available`.
- `mesh-presence --test` exits `2` with `no BT adapter on this node`.
- A live `mesh-presence --json` exits `2` and reports `status=unreachable`, `reason=no BT adapter`.
- The only reachable alternate checked, `ilya@192.168.8.214` (`iMac-Rozalia.lan`), has no `bluetoothctl` command; no existing mesh BLE producer is available there.
- `~/.mesh/presence.log` remains historical (last write `2026-08-30T07:10:10Z`); it was not touched or replayed.

Disposition: no safe in-scope prerequisite or software-only repair exists. The blocker is an absent
radio/producer capability, not a power or wiring fault. Keep the parent `DATA-STALE` and retry only
on `event:first-successful-BLE-adapter-or-fresh-presence.log-write`.
