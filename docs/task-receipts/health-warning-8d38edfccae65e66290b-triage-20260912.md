# Health warning triage: `health-warning/8d38edfccae65e66290b/triage`

Checked on `mesh-home` at 2026-09-12 15:35–15:36 UTC after the exact-owner dispatch check passed and `MESH_TASK_ACTOR=health` took the row.

## Evidence and disposition

- The warning describes `imac-rozalia` switching from active relay to active direct. A fresh `tailscale status --json` sample reports `Online=true`, `Active=true`, `CurAddr=5.227.25.156:55351` for `100.121.88.110`, matching the direct endpoint named in this warning. The `Relay=hel` field is retained as a separate tailnet field; the current endpoint is direct in `CurAddr`.
- This is a repeated peer-path transition observation, not evidence of a current peer outage. Prior receipts document other samples where the peer was inactive via relay or online but SSH authentication was refused; these point-in-time signals are not interchangeable.
- The repeated egress failure remains under the VPN repair chain. No route, DNS, firewall, WireGuard, or Tailscale state was changed by health.

Close as a transient path-change delta with the peer currently online and active on the named direct endpoint. Reopen only if a current sample shows a sustained failure. Health's independent FIB/LAN verification remains gated until VPN completes steps 1–3.
