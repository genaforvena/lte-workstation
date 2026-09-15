# Health warning triage: `health-warning/f734bbfb45bce9c12a4d/triage`

Checked on `mesh-home` at 2026-09-12 15:21–15:23 UTC after the exact-owner dispatch check passed and `MESH_TASK_ACTOR=health` took the row.

## Evidence

- The task cites `mesh-journal-watch` at 2026-09-11 08:00:02Z, where `~/.mesh/journal-watch.log` records the LED brightness failure twice as a new `-p err` signature.
- `journalctl --list-boots` shows the boot containing that observation ended at 2026-09-12 07:13:46Z; the current boot began at 08:42:35Z.
- `journalctl -b -k -p err --grep='leds enp42s0-0::lan'` returned no entries (exit 1). A fresh `mesh-journal-watch --once` exited 0 and did not report the LED signature; its 15:20Z tape entries show only recurring PipeWire busy-device errors.
- No LED-setting mutation or hardware intervention was attempted. The evidence supports that this is no longer a current-boot fault; it does not identify why the prior boot logged the error.

## Disposition

Close as a stale warning after reboot, not as proof that the underlying LED/controller issue is permanently repaired. Reopen if the signature returns in the current boot. The active recurring PipeWire busy-device signatures are separate findings and are outside this task.
