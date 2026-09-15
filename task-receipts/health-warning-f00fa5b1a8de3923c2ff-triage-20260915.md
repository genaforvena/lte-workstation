# Health-warning triage — `health-warning/f00fa5b1a8de3923c2ff`

Task: `health-warning/f00fa5b1a8de3923c2ff/triage`  
Owner: `health`  
Observed warning: study feed OAuth refresh failure and stale/degraded database-replication brief.

## Evidence

- `~/.mesh/study.log` ends at `2026-09-14T21:17:43Z` (`actor model`); its recent run records repeated
  `Failed to authenticate: OAuth session expired and could not be refreshed`, including
  `2026-09-14T13:37:11Z database replication`.
- The last successful same-topic entry is `2026-09-11T12:23:02Z`; it yielded only
  `Show HN: Biff 2.0`. This confirms the warning's stale/degraded-feed description.
- `mesh-study --test` exited 0 and reported `real-read ok (20 live hits)`, with all 18 registered
  fields and sources well-formed. This proves the fixture/dependency/read path, not OAuth recovery
  in the production scheduled lane.
- Cron wiring is present: `mesh-study` runs at `23 */4 * * *` behind `mesh-load-gate study 11`,
  with `mesh-study-autowake` every five minutes. No code or substrate change was justified by this
  triage; the live failure is an expired external OAuth session, not a local dependency failure.

## Disposition

Known external-auth blocker; retain the warning and retry on the next fresh study warning. Do not
claim a fresh brief, silently substitute the old Biff result, or modify routing/DNS/firewall/VPN.
OAuth renewal requires the study account's supported re-authentication path, which was not available
from this health window. No safe local repair was identified.

## Verification

- `mesh-study --test` — exit 0; 20 live hits, 18/18 registry sources valid.
- `stat ~/.mesh/study.log` — last write `2026-09-14 21:17:43Z`.
- `crontab -l` — scheduled study and autowake entries present.
