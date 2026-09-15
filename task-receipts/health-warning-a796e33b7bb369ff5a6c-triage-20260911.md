# Health warning triage: path-watch DERP fallback

- Task: `health-warning/a796e33b7bb369ff5a6c/triage`
- Warning: `path-watch@phaedra`, 2026-09-10 17:34:04Z, two peers fell back direct→relay.
- Dispatch gate: `mesh-task check dispatch health-warning/a796e33b7bb369ff5a6c/triage health` — exit 0.
- Current probe: `mesh-path-watch --once` at 2026-09-11 wake — `QUIET (peers=8 direct=2 relay=0 offline=6)`, with `imac-rozalia` and `phaedra` direct.
- Current Tailscale state: `imac-rozalia` direct, `phaedra` direct; six peers offline, no active relay path.
- Tape evidence: `~/.mesh/path-watch.log` records recurring direct↔relay transitions for both peers through 2026-09-11 22:44Z, while `netweather` reports `udp=true`; no `[path-udp-blocked]` root-cause line is present in the inspected window.
- Verdict: resolved for the current sample; recurring relay fallback is a known carrier/NAT degradation, not a safe local substrate action. Keep observing; do not restart or alter routing from this triage.

