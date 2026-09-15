# iMac room-eye unblock — 2026-09-13

Task: `unblock/health/d2d6ef7f613f5532/resolve`
Parent: `health-warning/25a35aa3f04ecad1655e/triage`
Checked: 2026-09-13 14:37 UTC on `mesh-home`.

## Root cause

The retry condition's LAN address was stale for this node's current route. `ip route get
192.168.8.214` routes via `100.76.0.1` on `enp42s0`, and the exact bounded SSH retry timed out
(`timeout 8s ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@192.168.8.214 true`, rc 124).
The mesh card lists the same iMac (`imac-rozalia`) online at `100.121.88.110`; its node context
also records that address as the Mac's mesh endpoint. A separate BatchMode `ssh ... true` probe
to that address also timed out, but the camera adapter's own SSH policy completed the full capture
when tested with `MESH_IMAC_HOST=ilya@100.121.88.110`.

`scripts/integrations/mesh-imac-cam` defaulted `MESH_IMAC_HOST` to the stale LAN address. Changed
that fallback to `ilya@100.121.88.110`; the environment override remains available. The installed
`~/.local/bin/mesh-imac-cam` compatibility wrapper resolves this repository implementation.

## Verification and recovery

- `mesh-imac-cam --test` passed its settle-core checks and completed a real, consented 155,140-byte
  JPEG capture using the new default.
- `mesh-imac-cam-watch --test` passed and completed a real cycle with state `SEEING`.
- Enabled and started the previously disabled `mesh-imac-cam-watch.service`; it is active and
  enabled. `~/.mesh/.imac-cam-prev.jpg` was a fresh 156,738-byte frame at 14:36:53 UTC.
- `mesh-room-sense-loss` now reports camera `LIVE` with `stored:LIVE`; the room-eye recovery was
  posted at 14:37:02 UTC.

The resolver's original retry IP was incorrect for the current node path. The concrete remaining
retry, if needed, is `timeout 8s ssh -o BatchMode=yes -o ConnectTimeout=5 ilya@100.121.88.110 true`,
followed by `mesh-imac-cam --test`.
