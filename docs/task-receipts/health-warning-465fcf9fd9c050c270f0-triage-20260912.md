# Health warning triage: `health-warning/465fcf9fd9c050c270f0/triage`

Checked on `mesh-home` at 2026-09-12 15:33 UTC after the exact-owner dispatch check passed and `MESH_TASK_ACTOR=health` took the row.

## Evidence and disposition

- The 2026-09-11 delta reports `imac-rozalia` becoming offline after an active direct connection. A fresh `tailscale status --json` sample reports `Online=true`, `Active=false`, and `Relay=hel` for `100.121.88.110`; this does not support a current offline verdict, and the direct path is no longer present in this sample.
- This repeats the time-sensitive iMac status already recorded in `health-warning-527459a9da5311d52698-triage-20260912.md`. The SSH-authentication and LAN-presence limits remain separate from tailnet online status.
- The two egress failures and four doctor warning categories are carried forward, with no new category. The LAN gateway route remains an already-owned VPN repair obligation; health made no network or substrate change.

Close this keyed delta as stale. Reopen the peer fault if a current tailnet sample reports it offline; after VPN completes steps 1–3, health must independently verify FIB and LAN reachability.
