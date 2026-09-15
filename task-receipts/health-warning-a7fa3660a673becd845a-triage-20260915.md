# Health warning triage — room camera recovery — 2026-09-15

Task: `health-warning/a7fa3660a673becd845a/triage`
Checked: 2026-09-15 12:22 UTC on `mesh-home`.

## Verdict

RESOLVED. The warning reported at 2026-09-14 00:12 UTC was a historical room-camera loss; the
primary iMac eye is reachable and producing fresh evidence now. No prerequisite task was needed.

## Live evidence

- `mesh-imac-cam --test` passed the real capture gate: reachable, consented, binary deployed, and
  a real 145475-byte JPEG was captured.
- `mesh-imac-cam-watch --state` returned `SEEING`.
- A normal `mesh-imac-cam-watch` cycle returned diff `0.60` with exit 0.
- `mesh-room-sense-loss --status` at 12:22:15 UTC reported `cam LIVE (stored:LIVE)`; ear, stt,
  and wake were also LIVE.
- Fresh artifacts: `~/.mesh/.imac-cam-prev.jpg` mtime 12:22:15 UTC, 146122 bytes;
  `~/.mesh/.imac-cam-watch.state` mtime 12:22:12 UTC.

The prior absence of SSH/camera reachability is no longer current. The exact next action if this
warning reappears is to rerun the bounded real-read gate and inspect the primary-eye artifact age
before creating or linking a recovery prerequisite.
