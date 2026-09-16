# Sense liveness evidence — physical-context

- Checked: `2026-09-16T01:34:30Z`
- Scope: scheduled sense organs probed with `--test`; live candidate read with `--json`.

## Candidate decision

`mesh-physical-context` was hollow: its cron entry was present and `--test` was green, while the
edge-only real artifact `~/.mesh/physical-context.log` remained at `2026-08-17 03:52:01 UTC`.
The live state file was touched, but that is not a fresh fused reading.

## Two bounded windows

- Last 24h: `/var/log/syslog` records 188 scheduled `mesh-physical-context --edge` attempts.
- Last 7d: `/var/log/syslog` plus `/var/log/syslog.1` records 1,751 scheduled attempts.
- Fresh-artifact coverage before repair: zero timestamped physical-context log writes in both
  windows; the log has no timestamps and its mtime predates both windows. The history of per-run
  results is absent because `--edge` suppresses unchanged output.
- Empty/unreachable inputs observed by a real read: `motion=OFFLINE`, `gravity=OFFLINE`; the
  result is honestly `DEGRADED`, not calm.

## Repair and verification

Replaced the active crontab's exact edge-only entry with:

`2-59/5 * * * * $HOME/.local/bin/mesh-physical-context --json >> $HOME/.mesh/physical-context.log 2>&1`

There is now exactly one active entry. A fresh real run at `2026-09-16T01:34:30Z` appended JSON:
`label=DEGRADED`, `reason=missing: body-motion,gravity`, `inputs.presence=ACTIVE_NEAR`,
`inputs.room=PRESENT`, `inputs.motion=OFFLINE`, `inputs.light=LIT`, `inputs.gravity=OFFLINE`.
`mesh-physical-context --test` passed its 13 assertions.

`mesh-reflex-health` was run; its report identified stale scheduled artifacts and absent organs.
The direct health run exceeded the 15-second bound during the audit, so health-history coverage
is marked UNKNOWN rather than inferred.
