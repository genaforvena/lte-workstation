# ds thermal watch + card freshness wired (and a new genome reflex: mesh-therm-watch)

Date: 2026-06-12
Tools: `scripts/mesh-therm-watch` (NEW) + card-watchdog timer activation on ds

## The gap (12:59 rotation finding)

ds — the production box (foxible, 11 containers) — hit a 91°C transient with **zero**
thermal monitoring: `mesh-therm` deployed but unwired, `mesh-card-watchdog.timer` inactive,
card stale ~12h. The staleness bit twice today (04:04-stale card hid the mic-fix result
until a full-path refresh; see [[mic-device-enumeration-2026-06-12]]).
`mesh-router-watch` covers the fanless router over SSH; **nothing covered the node a
watcher runs on**.

## What was built/wired

1. **`mesh-therm-watch` (new genome tool)**: node-local thermal edge-trigger in the
   body-power pattern — runs `mesh-therm`, appends to `~/.mesh/therm.log` (per-run
   artifact for mesh-reflex-health), edge-triggers `[therm-hot]`/`[therm-cool]` at
   `MESH_THERM_HOT` (default 85°C) with a 5°C hysteresis band, `MESH_ALERT_DRYRUN` gate
   (chaos-drill lesson), TG+chat alerts, cheap 2000→1000-line log rotation.
2. **Cron-wired every 10min on BOTH nodes** (IdeaPad + ds).
3. **ds card-watchdog activated**: `.sh` + systemd user units installed,
   `enable --now`, `Linger=yes` confirmed (survives logout; `OnBootSec=10min` covers reboot).

## Verification

- Edge transitions exercised in DRYRUN on both nodes (forced HOT at threshold 10 → one
  alert; recovery → `[therm-cool]`; state file transitions; no real alerts sent).
- ds was **genuinely at 86°C during wiring** (above default threshold — the gap is not
  hypothetical). Dipped to 84°C on the live run → correct no-alarm.
- **Dryrun gotcha worth keeping**: a dryrun run still writes the state file, so it can
  CONSUME the real edge (next live run sees prev=HOT and stays silent). After dryrun
  testing on a node that is actually hot, reset the state file before the first live run.
- ds card-watchdog: timer listed, immediate service run refreshed the card (mtime moved),
  `--test` ok (with PATH — non-login ssh PATH strikes again, the unit itself uses absolute paths).

## Stale-audit correction

Genome-lean audit claimed exec-bit missing in genome for `mesh-card-watchdog.sh`,
`mesh-chaos-verify`, `mesh-steward-deadman` — **stale**: all three are already 100755 in
the git index. Don't re-chase.
