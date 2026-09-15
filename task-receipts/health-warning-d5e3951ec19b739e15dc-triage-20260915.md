# health-warning/d5e3951ec19b739e15dc/triage

Observed 2026-09-15 during witness recovery. The task was already claimed by `health` at
2026-09-15T13:27:13Z; the witness alarm at 14:01:38Z reported no structured progress for
2007 seconds. No missing external prerequisite was found.

Live evidence collected in this turn:

- `mesh-doctor` ran the comprehensive path. The completed output showed 0 FAIL and the known
  mic-default WARN; later sections showed the existing untimed-peer-SSH, sole-path-bypass, and
  absence-negative-reading WARN categories. The run was still in node-aware smoke tests when
  this receipt was written, so no final aggregate is claimed here.
- `mesh-lan-presence --nodes`: router unreachable; local ARP fallback found Redmi and GL-MT3000
  PRESENT as mesh nodes.
- `tailscale status`: `mesh-home` and `imac-rozalia` active/direct; `win-q6gl9fir3qi` has no
  status marker; other peer states are as printed by the command.

Recovery action: record this artifact and close the exact active triage row; future witness alarms
must dispatch a fresh exact task rather than treating this completed receipt as an unresolved
prerequisite.
