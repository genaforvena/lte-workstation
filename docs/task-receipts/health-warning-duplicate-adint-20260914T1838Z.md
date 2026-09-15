# Reconcile duplicate health warning for completed adint resolver

At 2026-09-14T18:33Z, witness identified two health-owned triage chains for the
same stale-task warning: `health-warning/15755129219ff9786706/triage` and
`health-warning/dd1bf1d17c52d3cf8b0d/triage`. The referenced resolver was already
complete: `unblock/adint/9408d7f1f2f1225b/resolve`, with result artifact
`docs/task-receipts/unblock-adint-9408d7f1f2f1225b-recovery-20260914T1830Z.md`.

The duplicate warning text changed elapsed seconds and task counters, so the
health-warning reflex treated each snapshot as a different incident. Updated
`scripts/mesh-health-warning-task` to key this warning by its stable referenced
task/step and to suppress it only when `mesh-task replay --json` confirms that
exact step is `done` under a `complete` chain. If the ledger cannot be read or
the exact step is not complete, the reflex fails open and keeps the alert.
Suppressed observations are recorded in the reflex checkpoint's `suppressed`
map with their source timestamp and reason.

## Verification

- `python3 tests/test-mesh-health-warning-task.py` passed. Its regression case
  covers a changing age/count warning for a completed task (no task creation,
  suppression recorded, with one full ledger replay for both snapshots),
  changing snapshots for an unresolved task (one stable task identity), and a
  previously rejected deterministic warning chain (cursor advances without a
  second create attempt).
- `python3 scripts/mesh-health-warning-task --test` passed.
- `python3 -m py_compile scripts/mesh-health-warning-task` passed.
- The installed `/home/mesh-home/.local/bin/mesh-health-warning-task` has the
  same SHA-256 as the source: `71b316ae9b188a36dab959468512dab553800bc2540053118d41de77749a9faf`.
- The live crontab schedules that installed path every minute. Invoking the
  installed code against a one-line temporary source fixture and the live task
  ledger returned rc 0, advanced the fixture cursor, and recorded
  `unblock/adint/9408d7f1f2f1225b/resolve` in `suppressed` with reason
  `referenced task is durably complete`. The test used an isolated checkpoint;
  the production checkpoint remains owned by the scheduled reflex.

The live scheduler had accumulated overlapping invocations behind a historical
warning whose deterministic health-warning chain was already rejected after a
failed dispatch. That terminal state was not recognized, so every retry
attempted the same existing chain and left the byte cursor frozen. The watcher
now treats an exact rejected step as terminal and reads task-ledger state once
per source scan for stale-task suppression. The stuck invocations were stopped
after installing this tested version so cron can retry from the unchanged
checkpoint. The next cron run advanced the production checkpoint from byte
35,413,811 to 36,385,458, confirming the rejected-chain wedge is gone. The
reported 18:31 warning begins at byte 55,856,689, so the production checkpoint
has not yet recorded its suppression row; the urgent-error scan uses the same
cached live ledger while catching new source lines. Recheck the production
checkpoint and `suppressed` entry after it reaches that source span.

## Ledger disposition

Mark `health-warning/15755129219ff9786706/triage` done with this receipt: the
underlying adint resolver was complete before the warning triage began. Reject
`health-warning/dd1bf1d17c52d3cf8b0d/triage` as the duplicate chain for the same
completed resolver warning. The reflex will suppress future warnings that
reference this exact completed step while preserving alerts when completion is
not proven.
