# H-Ledger reconciliation acceptance — 2026-09-09

Task: `coordination-hledger-reconciliation-extension-20260909/reconciliation-acceptance`

## Verdict

**FAIL** — the extension is not acceptable as deployed. The source implementation can read the
repository when `MESH_RECON_REPO=/home/mesh-home/lte-workstation` is supplied, but the deployed
cron copy defaults `REPO` from its own directory (`~/.local/bin/..`), so its live report cannot
find task receipts or the git repository. The live 02:27 report consequently says `UNKNOWN` for
task, artifacts, git, and all three accounting checks.

## Evidence

- Live ledger check before work: step 3 was `open`, owner `witness`, with no acceptance receipt.
- `bash tests/test-mesh-hledger-reconcile.sh`: PASS; `bash -n scripts/mesh-hledger-reconcile tests/test-mesh-hledger-reconcile.sh`: PASS.
- Source-controlled run at cutoff `2026-09-09T02:56:00Z`: board/task/artifact/git sources all
  `KNOWN`; accounting checks returned `promises PASS`, `ledger PASS`, `labor PASS`; difference
  class was `SOURCE_ONLY` (`board_tasks=1962`, `replay_tasks=330`).
- Deployed run with the same cutoff and without an override: reproduced the live failure:
  `source=task status=UNKNOWN`, `source=artifacts status=UNKNOWN path=/home/mesh-home/.local/docs/task-receipts`,
  `source=git status=UNKNOWN`, and accounting sources `UNKNOWN`.
- Cadence wiring is present in `~/.mesh/reflexes.cron` as `27 * * * * ... mesh-hledger-reconcile
  --run`; the source header declares the same cadence. `~/.mesh/hledger-reconcile.log` records
  runs at 01:27 and 02:27. The latest report mtime is 02:27:02 UTC, about 30 minutes old at
  verification, within the hourly cadence but semantically unusable because of the source-path
  failure.
- The focused fixture covers only one known, balanced happy path. It does not replay a missing
  source, delayed feed, balanced-but-incomplete identity set, or an explicit adjustment.
  Inspection of the implementation shows only count equality/inequality (`MATCH` or
  `SOURCE_ONLY`); it does not implement delayed/late, state-mismatch, duplicate, or adjustment
  replay behavior. Therefore those acceptance legs are `UNKNOWN`/unproven, and a balanced but
  incomplete feed could be falsely reported as `MATCH`.
- The read-only source run writes only its requested report. `mesh-task replay --json` and
  `mesh-task queue --dispatch` hashes were unchanged across the run (`a7f29b6d9b017f23b19d08e1229e73798c0a23fbfa583d1912f1a36b070ac341` and
  `aab2381e6f23ee39dd0b2a75c02c0be7e5c30cf5be98139ee54f0ae546808c03`). No task liability or
  routing mutation was observed.
- Current accounting checks: PROMISE parity/agreement has a HOLD agreement failure
  (`replay=60` vs blank journal value); `mesh-ledger --check` and `mesh-labor --check` pass.
  This pre-existing accounting failure remains unresolved and must not be hidden by reconciliation.

## Unresolved obligations

1. Fix deployed repository resolution (or explicitly wire the repository path) and rerun the live
   report, then verify the output is `KNOWN` for all available sources.
2. Add independent fixtures for missing source, delayed feed, balanced-but-incomplete identities,
   and authorized explicit adjustment; require `UNKNOWN`/`LATE`/`STATE_MISMATCH` as appropriate.
3. Resolve or separately account for the existing PROMISE HOLD agreement failure before claiming
   an all-source PASS. Keep the extension report-only; do not alter liabilities or routing.

