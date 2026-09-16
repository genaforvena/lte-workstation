# senses-reflex-health-feed-cam-followup — 2026-09-16

## Result

The live `mesh-reflex-health --check` initially exited 1 because `feed` was stale. The
`cam-watch` producer was not stale; its state was fresh but correctly classified as a
sample. The feed producer was exercised live and its real artifact refreshed. A follow-up
reflex-health check exited 0.

## Evidence

Commands run from `/home/mesh-home/lte-workstation`:

```text
timeout 60 mesh-reflex-health --check
exit=1
... feed(stale 22566s>600s, 2+ consecutive) ... cam-watch(aliased ... reads a SAMPLE not a state) ...

timeout 45 mesh-feed --test
exit=0
smoke-test: ok (idle-cap + stimulus-stall + lazy-pace + paced-skip-heartbeat + pressure-gradient + driftability tie-break wired)

timeout 45 mesh-cam-watch --test
exit=0
smoke-test: ok (... real frame/diff and device-mutex gates ...)

mesh-feed
exit=0
assigned 0, 1 backlog remain [STIMULUS-STALL: unmet demand, 0 recruited]

stat ~/.mesh/feed.log
mtime=2026-09-16 10:53:42Z size=1299159
stat ~/.mesh/.cam-watch.state
mtime=2026-09-16 10:53:20Z size=44

timeout 45 mesh-reflex-health --check
exit=0
reflex-health: ok (39 per-run reflex(es) fresh ...)
```

The remaining `wifi-link` blind and absent `kbd-activity`/`wifi-rf` lines are explicit
UNKNOWN/n/a capability states, not repaired or cleared by this task.
