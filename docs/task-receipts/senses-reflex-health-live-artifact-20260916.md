# senses-reflex-health-live-artifact — 2026-09-16

## Result

The installed reflex-health path is present and source-identical, but its real check is
currently unhealthy. `mesh-reflex-health --check` exited 1 and reported stale live
artifacts, including `feed` (15983s), `cam-watch` (11071s), and a frozen `wifi-link`
organ (2184s since its last real read). This is an honest failure, not a fabricated
green state.

## Commands and evidence

Run from `/home/mesh-home/lte-workstation` at 2026-09-16T09:02Z:

```text
command -v mesh-reflex-health
/home/mesh-home/.local/bin/mesh-reflex-health
sha256sum scripts/mesh-reflex-health /home/mesh-home/.local/bin/mesh-reflex-health
b514c2ba14974a9e48b33aebd0c425d5c4c993f40b7d56e7862586b976e0394d  both paths
timeout 30s /home/mesh-home/.local/bin/mesh-reflex-health --check
exit=1
```

The check emitted a complete status line to stdout. It classified `feed` and `cam-watch`
as `STALE`, `wifi-link` as `BLIND`, absent `kbd-activity` and `wifi-rf` as `n/a`, and
reported no co-failing cohort. Stderr was empty. The command completed before the 30s
timeout and did not write the liveness log.

## Wiring / retry edge

The source and deployed hashes match, proving the installed path is the checked source.
The next safe action is to inspect the producer paths for `feed` and `cam-watch` and rerun
their own real tests; do not clear the reflex-health failure until their artifacts become
fresh. The separate `mesh-dash --once senses` and `mesh-task queue --dispatch --owner
senses` probes timed out under current mesh contention, so their state remains UNKNOWN.
