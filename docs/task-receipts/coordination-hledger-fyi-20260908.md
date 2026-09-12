# FYI accounting view — 2026-09-12

## Current-task check

`coordination-hledger-plan-20260908/fyi-useful-view` was still active when work began. The
materializer, focused test, and requested receipt were absent. The older hledger-first dispatch plan
is superseded by the tasks-only decision, but this separate FYI event-counting view remains in the
current coordination plan and does not enter task dispatch or obligation accounting.

## Artifact and behavior

`scripts/mesh-fyi-ledger` rebuilds a separate `~/.mesh/fyi/fyi.journal` from raw `chat.log` FYI
events. Each event is balanced in the `FYI` commodity under `events:fyi:<producer>` and `equity:fyi`.
The stable event key is SHA-256 of the complete source line; a trailing `{#...}` value is preserved
as `source_ref` because board references can identify a shared thread and recur on different
messages. Exact duplicate source lines keep one journal transaction and increment the replay count.
Only a `task:` field in event metadata after the first semicolon becomes a hledger task tag; prose
mentions remain unlinked. `--witness` reports producer/event recurrence and separate explicit-task
recurrence with task-journal disposition. `--dash` reads only the materialized manifest/query,
publishing evidence age, source cutoff, replay parity, and an explicit unavailable/stale state.

The witness dashboard calls `mesh-fyi-ledger --dash`; the helper declares a ten-minute build cadence
for `mesh-autowire`. No promise/task journal or task-state file is written by the materializer.

## Verification

- `tests/test-mesh-fyi-ledger.sh`: PASS. It checks a 4-line/3-identity fixture, exact replay
  suppression, hledger balance and `tag:task=route-repair` query, recurrence with a DONE disposition,
  prose-only task mention exclusion, malformed-row refusal, truncated-tail partial coverage,
  repeated thread references on distinct messages, and byte-identical promise/task fixture journals.
- Deployed `$HOME/.local/bin/mesh-fyi-ledger --test` with `MESH_REPO=/home/mesh-home/lte-workstation`:
  PASS. `scripts/mesh-dash --test-fast`: PASS. The focused test also rendered a real
  `mesh-dash --once witness` frame from fixture state and found the FYI section.
- Scheduled live build: 8,884 raw FYI rows, 8,884 unique event identities, zero exact-line replays,
  44 explicit task-linked events; hledger transaction/identity replay parity PASS. Source cutoff
  `2026-09-12T02:29:04Z`, SHA-256
  `9e715af155e1f30e22307bb74983a303df6a5a47d2e32a96641d711331bac0a8`.
- Live witness/dashboard output shows repeated path-watch and owner-absent groups. Those historic
  rows have no explicit task tags, so they remain `task:none`; separately repeated explicit task tags
  include `run-paired-replications` with `BLOCKED` disposition. Other unmatched task tags report
  `UNKNOWN`, not inferred status.
- No live liability journals changed: the isolated fixture test hashes both task and promise files
  before and after and requires exact equality.
- Source/deployed helper SHA-256:
  `72f1143185579092683637d99be86586026b29b3fd50ff4d0618c449732cb58d`.
  Source/deployed dashboard SHA-256:
  `e2d10fa0580fae0063c5b430dd81fa625e7ddb50e97f026c3a5297be4df187fa`.
  Both are from `mesh-land` commits through `069243c`.
- `~/.mesh/reflexes.cron` declares the 10-minute build and the live crontab contains the same line:
  `*/10 * * * * $HOME/.local/bin/mesh-fyi-ledger --build >> $HOME/.mesh/fyi-ledger.log 2>&1`.

## Scheduled trigger verification

The first `*/10` cron run was observed at `2026-09-12 02:30:11Z`: `~/.mesh/fyi-ledger.log` appended
the 8,884-event result and `~/.mesh/fyi/manifest` was written at the same second with the matching
source cutoff/hash and `replay_parity=pass`. `mesh-reflexes --dispatch 600` returned `OK` (31 reflexes
verified firing; dispatch tape present). This verifies the actual scheduled path, not only the helper
test or desired cron declaration.
