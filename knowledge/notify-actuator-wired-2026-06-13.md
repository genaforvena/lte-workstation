# mesh-notify is now the shared notify probe

Date: 2026-06-13

I found that `mesh-organ-keepalive` had been probing the notification daemon directly with `dbus-send`,
which left `mesh-notify` as an orphan even though the actuator itself worked.

Fix chosen:
- add a quiet `mesh-notify --check` path for daemon liveness, without a popup
- make `mesh-organ-keepalive` call `mesh-notify --check` instead of duplicating the D-Bus probe

Live verification:
- `scripts/mesh-notify --check` exits 0 on this node
- `scripts/mesh-organ-keepalive --status` reports `notify — LIVE`

This keeps the actuator and the keepalive probe on the same code path, so the board can now
distinguish a real notify regression from a probe bypass.

