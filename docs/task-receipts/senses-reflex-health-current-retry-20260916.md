# Current reflex-health retry — 2026-09-16

## Live probe

Command:

    timeout 120s /home/mesh-home/.local/bin/mesh-reflex-health --check

Started `2026-09-16T14:52:01Z`, ended `2026-09-16T14:53:28Z`, exit `1`, with initial
`/proc/loadavg` load1 `124.13` on 16 CPUs. Output was 3452 bytes at
`/tmp/senses-reflex-health-current-retry-20260916.out`; the real verdict was `STALE`.

## Predicate and classification

The current report identifies two placeable stale producer failures:

- `feed`: stale `14357s > 600s`, 2+ consecutive.
- `cam-watch`: stale `7929s > 120s`, 2+ consecutive; the report confirms it is launched by
  `reflexes.cron+crontab,user-units via=unit-ExecStart`, so scheduling is live but its writes fail.

It also reports observer-impaired `load-thrash(130.94/16c)`, `wifi-link` organ-blind (published
state frozen while its blind marker is fresh), and absent `kbd-activity`/`wifi-rf` organs with
their own `--test` exit 2. These are not promoted to dead reflexes.

## Artifact and wiring evidence

At the end of the probe:

    ~/.mesh/.reflex-health-state  size=6       mtime=2026-09-16 14:51:07Z
    ~/.mesh/reflexes.log          size=853632   mtime=2026-09-16 14:49:50Z
    ~/.mesh/wifiscan.log          size=1432523  mtime=2026-09-16 14:47:26Z

Source and installed tool hashes match:

    b514c2ba14974a9e48b33aebd0c425d5c4c993f40b7d56e7862586b976e0394d

for both `scripts/mesh-reflex-health` and `/home/mesh-home/.local/bin/mesh-reflex-health`.

## Retry edge

This is a machine-owned producer/write failure under severe measured load contention, not a
missing binary or source/deployed drift. Retry after the next `feed`/`cam-watch` cadence or
writer/service recovery, preferably when load1 is no longer thrashing; if still stale, inspect
the two producer writers and their launch units. No source or substrate mutation was performed.
