# Health warning triage — `health-warning/dd4efd0509f5fd62eb2c/triage`

- Time: 2026-09-15T20:42Z
- Owner: health
- Live state: `mesh-dash --once check` reports local load high/unreliable probes, egress OK, VPN degraded observe-only, and cached doctor `FAIL=1 WARN=34` with a recent `dispatch.log` error.
- Warning subject: `mesh-ble-heal` remains live-broken, not historical-only.
- `scripts/mesh-ble-heal --status` exited 0: `verdict=DAEMON-SICK wedges=1157 last_outcome=cooldown`.
- `scripts/mesh-ble-heal --test` exited 1: live `bluetoothctl show` has no parseable `Powered` flag.
- Direct probe: `bluetoothctl show` exited 1 with `No default controller available`.
- `systemctl status bluetooth` confirms `bluetooth.service` active/running (PID 2797037); therefore the evidence is a missing controller/adapter, not a stopped daemon.
- Wiring: the reflex is scheduled by `~/.mesh/reflexes.cron.bak-mesh-home` at 15-minute cadence; no substrate changes made.
- Action: ran `scripts/mesh-ble-heal`; it correctly held because the 90-minute heal cooldown was active (`66m/90m`). No further mutation was performed.
- Known blindness / next action: controller absence is not recoverable by the healer while cooldown is active and needs hardware/USB or host-level investigation after cooldown; keep the warning open and re-run the live test/status then.
