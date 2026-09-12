# Health warning triage: load, local inference, and temperature

Task: `health-warning/1dd6d282dffb54b6e468/triage`

## Current readings

- The latest check pane (13:17Z) showed the fleet path `OK`, local-load probes flagged unreliable,
  `load1=14.88/16`, and CPU load attributed to organ work. Fleet reachability remained partial:
  mesh-home and phaedra were up; the other eight nodes were down/unknown, with no LAN peers.
- `mesh-hw-health` completed at 13:18Z: thermal max 69°C, ambient about 25°C, gap 44°C, overall
  `HW: OK`; SMART passed with 2% wear and no critical warnings. This does not support a current
  thermal fault.
- `mesh-load` returned `unattributed: busy`; current process evidence showed a local
  `llama-server` using about 8.8 GiB RSS, but that does not identify the process behind the older
  OOM or make llama its cause.
- At 13:20Z, uptime/load averages were 9.18 / 25.76 / 32.23 (1/5/15m), memory was 13/31 GiB used,
  and swap was 7.0/8.0 GiB used. CPU PSI was elevated; memory PSI was 0 at the sampled instant.
- Kernel journal confirms a real global OOM at 12:37:02Z: the kernel killed `python` PID 2398365
  with anon RSS 19,698,612 KiB from `cron.service`; free swap was 220 KiB of 8 GiB. The retained
  evidence does not preserve the Python command line, so its exact job is unknown.

## Wiring and liveness

The old `resource-guard.log` mtime initially looked stale, but that file records alert output and is
not its per-run liveness artifact. The actual user crontab has
`*/2 * * * * mesh-resource-guard --alert`; cron journal entries show it ran at 13:20Z. Its
`.resource-guard-state` was freshly updated at 13:22Z with `OK`, and `mesh-reflex-health --check`
reported 36 per-run reflexes fresh. A direct read-only `mesh-resource-guard` at 13:21Z also said
node `OK`, while reporting node-omega accumulation and a criticality warning. Thus the reflex is
live; a quiet alert log was not a dead-reflex signal.

## Verdict

Temperature is currently within the tool's `HW: OK` verdict. The warning about unreliable load and
inference attribution is real: the `mesh-load` reading is explicitly unattributed, while the
12:37Z cron-owned Python OOM was a rapid, very large process event that a two-minute sample cannot
identify after the victim has exited. The current resource reflex and wiring are healthy, but this
incident leaves a known coverage blind for short-lived cron processes and per-process attribution.
Do not attribute that OOM to llama or change process policy without command-level evidence. No
substrate or resource-control setting was changed.

Verification: checked live crontab and cron journal, fresh reflex-health output and state-file mtime,
the complete kernel OOM victim line, direct resource-guard output, current hardware-health output,
and current process/memory/pressure snapshots.
