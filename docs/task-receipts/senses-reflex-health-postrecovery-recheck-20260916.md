# Senses reflex-health post-recovery recheck — 2026-09-16

## Result

The live installed probe completed in 62 seconds with exit 1 (typed `STALE`, not a timeout
or fabricated success). The command was:

    timeout 120s /home/mesh-home/.local/bin/mesh-reflex-health --check

Captured output: `/tmp/senses-reflex-health-postrecovery.out`, 3006 bytes. The real verdict
reported `feed` stale (11140s > 600s) and `cam-watch` stale (4712s > 120s), while explicitly
stating both are launched by `reflexes.cron+crontab,user-units` and their writes are failing.
It also reported observer-impaired load-thrash `94.98/16c`, and classified absent `kbd-activity`
and `wifi-rf` as organ-absent (`--test` exits 2), not dead reflexes. `wifi-crossval` remained
value-frozen at 1488567s with power-off UNKNOWN.

## Freshness and wiring evidence

At probe completion:

    ~/.mesh/.reflex-health-state  size=6       mtime=2026-09-16 13:50:54Z
    ~/.mesh/reflexes.log          size=852016   mtime=2026-09-16 13:56:32Z
    ~/.mesh/wifiscan.log          size=1431443  mtime=2026-09-16 13:57:26Z

Source and installed hashes match:

    scripts/mesh-reflex-health
    /home/mesh-home/.local/bin/mesh-reflex-health
    b514c2ba14974a9e48b33aebd0c425d5c4c993f40b7d56e7862586b976e0394d

## Retry edge

This is a machine-owned live producer failure. Retry after the next `feed`/`cam-watch` producer
cadence or service/log-writer recovery event; if still stale, inspect those producer writers and
their launch units. No source or substrate mutation was performed.
