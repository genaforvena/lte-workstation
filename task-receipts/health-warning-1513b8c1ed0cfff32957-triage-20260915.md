# Health-warning triage — 2026-09-15

Task: `health-warning/1513b8c1ed0cfff32957/triage`

## Disposition

This is a live chronic suppression roll-up for imac-rozalia SSH access, but
it is an external credential/authentication blind spot rather than a mesh-home
transport fault. The safe disposition is to preserve the warning and retry
when valid imac SSH credentials or an owner-authorized LAN path becomes
available. No routing, VPN, firewall, or service mutation is justified.

## Evidence

- `mesh-health` at 2026-09-15T14:52:17Z reports `PASS imac-rozalia`
  (100.121.88.110).
- `tailscale status` shows imac-rozalia active and direct at
  `192.168.8.214:56461`, proving current tailnet transport.
- A bounded SSH probe to `100.121.88.110` reaches the host but returns
  `Permission denied (publickey,password,keyboard-interactive)`.
- Prior receipts for the same chronic signature document the same transport
  reachable/authentication refusal and no safe substrate action.

The warning is therefore valid and unresolved externally; it is not rejected
as duplicate or cleared. The exact retry condition is valid SSH credentials
or an owner-authorized independent LAN/SSH path for imac-rozalia.

## Verification

- `mesh-dash --once check` at 2026-09-15T14:51:00Z returned; local node,
  supervised egress, and GPU were healthy, with known BT/mesh alarms.
- `mesh-task queue --dispatch --owner health` returned this exact row.
- `mesh-task check dispatch health-warning/1513b8c1ed0cfff32957/triage health`
  exited 0.
- `MESH_TASK_ACTOR=health mesh-task take health-warning/1513b8c1ed0cfff32957 triage`
  succeeded.

No code or substrate state changed.
