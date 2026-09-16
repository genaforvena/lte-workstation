# Ambient stale follow-up — 2026-09-16

## Observation

`mesh-dash --once senses` at `2026-09-16T01:01:04Z` rendered:

`ambient=DATA-STALE|dwell_s=170930|changes_24h=0|fixture=CYCLING (STALE)`

The apparently similar room-microphone path is healthy: `mesh-ambient-level --json` at
`2026-09-16T01:02:58Z` returned `label=MODERATE`, `src=tap`, `rms_db=-28.7`,
`coverage=0.984`, and the `.ambient-level` state mtime advanced at the same time. Therefore the
dash line is the separate BLE-derived `mesh-ambient-clock` axis, not the microphone producer.

## Cause

- `~/.mesh/.ambient-clock.state` has not advanced since `2026-09-11T14:34:52Z` and contains
  `DATA-STALE|...|fixture=CYCLING`.
- `~/.mesh/presence.log` has not advanced since `2026-08-30T07:10:12Z`; its last rows are old
  BLE snapshots, so the stale result is honest and must not be refreshed by touching the file.
- `scripts/mesh-ambient-clock` explicitly declares itself `orphan-ok: DECAYED` and says not to
  wire it until a live feeder is restored.
- The local node has `bluetoothctl` installed but `bluetoothctl show` reports `No default
  controller available`; `/sys/class/bluetooth` is empty. The mesh presence implementation
  therefore correctly exits 2 for this node: the adapter is absent, not merely unpowered.
- `mesh-arrivals` is wired, but its BLE scan cannot restore `presence.log` without a local radio;
  no safe code-only fix exists on this node.

## Recovery and wiring result

The prerequisite event did occur: `mesh-presence --log` at `2026-09-16T02:07:30Z` returned `rc=0`
with 7 live BLE devices and advanced `~/.mesh/presence.log` to `2026-09-16T02:07:33Z`.
`mesh-ambient-clock --json` at `2026-09-16T02:07:33Z` independently returned `data_stale=false`,
but the dash-facing cached state remained stale because the current crontab had the producer disabled.

The wiring defect was the commented producer line:

`# DECAYED 2026-09-10 ...`
`# 6-59/30 * * * * $HOME/.local/bin/mesh-ambient-clock --edge ...`

The line was re-enabled with an evidence-bearing `LIVE 2026-09-16` comment, then
`mesh-ambient-clock --edge` ran successfully (`rc=0`) at `2026-09-16T02:10:31Z`.
It wrote the real cached artifact:

`~/.mesh/.ambient-clock.state` mtime `2026-09-16T02:10:31Z`
`MODERATE|dwell_s=128|changes_24h=1|fixture=CYCLING`

No historical tape was touched and no ambient value was fabricated. `mesh-ambient-clock --json`
and the producer's `--edge` path now agree on the live BLE evidence. A bounded
`mesh-dash --once senses` run still timed out (`rc=124`) while probing another live dependency;
this is a separate dash/probe issue, not evidence that ambient-clock is stale.
