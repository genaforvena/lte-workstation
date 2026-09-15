# Coordination/hledger identity-routing receipt — 2026-09-08

## Verdict

REJECTED as specified against the current task implementation. The requested exact-owner
reconciliation cannot close the remaining autostash alias because the existing task records
owner `mesh-land/genome`, while `scripts/mesh-task` derives its actor with
`ACTOR.split("@")[0].split("/")[-1]`; the live actor is therefore `genome`. Both `take` and
`reject` enforce equality and refuse the slash-qualified owner. Changing the owner or creating
a replacement autostash ID would violate the instruction to preserve existing repair IDs.

## Frozen source and queue evidence

- Source cutoff: `2026-09-08T22:38Z` (this receipt's board operations).
- `chat.log` SHA-256 at verification: `eb8c8df2f3a587e20910a03ad7783a29dc71d6859e66378bdd966462e21bb5ac`.
- `mesh-task replay --json`: `rc=0`; source-coverage test passed.
- `mesh-task queue --dispatch`: `rc=0`; the remaining relevant queued row is exactly
  `mesh-land/genome witness-live-unattended-followup-20260908-owner-correction-20260908/repair-parked-autostash-strand`.
- The original `land` alias was taken as `land` and rejected through the supported transition,
  preserving its ID. The corrected slash-owner alias remains visible and untouched because the
  current owner guard cannot address it.

## Per-obligation disposition

| Source obligation / canonical ID | Current evidence | Disposition and next action |
|---|---|---|
| `witness-live-unattended-followup-20260908/repair-parked-autostash-strand` | Existing live receipt says both stale autostashes were anchored/dropped while unrelated work and manual WIP were preserved. | Original alias rejected as superseded; no rerun. |
| `witness-live-unattended-followup-20260908-owner-correction-20260908/repair-parked-autostash-strand` owner `mesh-land/genome` | Existing owner-correction2 and generic receipts document the same live disposition; queue still carries this malformed owner. | Retained unchanged. Requires a code-level owner-identity repair or an exact-owner actor before supported rejection/supersession. |
| `sound-experiments-20260908/min-beats-material-cost` owner `sound` | Sound posted receipt `docs/task-receipts/sound-experiments-20260908-min-beats-material-cost-20260908.md` for the alias `task:min-beats-material-cost`; canonical full ID remains queued/open. | No owner impersonation. Targeted `[task]` sent to `sound` to settle the existing canonical ID against that receipt, preserving the ID. |
| `ilya-back-online-push-restore-env` owner `steward` | Prior source records it as human-owned/offline-dependent. | Separate task `coordination-hledger-identity-ilya-20260908/ilya-back-online-push-restore-env`, owner `steward`, is explicitly `BLOCKED` on `operator-input`; retry is a confirmed ilya-online event. |
| `phone-authorized-keys-recheck` owner `operator` | Prior source records it as human-owned/offline-dependent. | Separate task `coordination-hledger-identity-phone-20260908/phone-authorized-keys-recheck`, owner `operator`, is explicitly `BLOCKED` on `operator-input`; retry is operator confirmation of phone SSH reachability. |

## Verification

- `rtk proxy bash tests/test-mesh-task-source-coverage.sh`: `PASS`.
- `rtk proxy bash tests/test-mesh-task-dispatch-receipt.sh`: `PASS`.
- `rtk mesh-task replay --json`: `rc=0`.
- `rtk mesh-task queue --dispatch`: `rc=0`.
- `mesh-promises --check` reached parity `PASS` but timed out before completing claims agreement;
  `mesh-promises --balance` still showed the three unresolved non-roster liabilities. This is
  retained as unavailable/incomplete evidence, not treated as closure.

The parent task is rejected because the specified exact-owner acceptance is impossible with the
current owner parser and the remaining malformed alias must not be silently substituted.
