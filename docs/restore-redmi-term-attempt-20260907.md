# Redmi Termux restore attempt — 2026-09-07

Owner: `discover`  
Task: `owner-genome-discover-restore-redmi-term`

## Live verification

The task was dispatched to `discover` at `2026-09-07T20:28:02Z`. A fresh owner probe at
`2026-09-07T20:29:51Z` found:

- Tailscale peer `Redmi 10` / `100.103.99.16`: `Online=false`, last seen
  `2026-09-03T09:53:36.1Z`.
- The FIB still routes `100.103.99.16` via `tailscale0` (table 52), but that is not
  reachability evidence.
- SSH as the documented Termux user `u0_a380` on port `8022` timed out at all three
  current candidates: `100.103.99.16`, `192.168.8.203`, and `192.168.8.146`.
- The only attached ADB device is `SM-N900`, Android `5.0` (serial
  `4d00553d61ab90b7`), which is the Note3 rather than the Redmi. It cannot be used as
  evidence of, or a remote control path to, Redmi Termux.

## Result

No Redmi Termux restore was possible from this node because the body is offline on both
available SSH planes and no Redmi ADB transport is attached. No routing, inbox, or phone
state was changed. Required next action is physical Redmi wake/unlock (or a live Redmi
ADB/SSH transport), followed by `id -un` and a real `termux-battery-status` read.
