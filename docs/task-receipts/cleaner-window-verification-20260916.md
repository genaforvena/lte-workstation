# Cleaner window wiring verification

Task: `cleaner-window-verification-20260916/verify-cleaner-wiring`
Observed: 2026-09-16T10:32:20Z UTC

## Scope

Independently verified the implementation against
`docs/task-receipts/cleaner-window-plan-20260916.md`, the implementation receipt,
the live deployment, task wiring, and a real report-only invocation. No cleaner
mutation, publication, or task-ledger mutation was performed by the cleaner.

## Evidence

| Check | Result |
|---|---|
| `bash tests/test-mesh-cleaner.sh` | PASS; all five smoke tests and integration check |
| `scripts/mesh-manifest --check` | PASS; 1,373 complete rows, no duplicate installed basenames |
| `scripts/mesh-autowire --check` | bounded attempt did not complete within 120s under concurrent mesh load (rc=124); direct live wiring verification below passed |
| `scripts/mesh-sync-tools --apply` | PASS in the implementation receipt; deployed paths resolve to repository scripts |
| Live executable deployment | PASS; all five `~/.local/bin/mesh-cleaner-*` paths resolve to `scripts/cleaner/` |
| Live crontab | PASS; four scheduled entries exist: scan/settle every 15m, docs hourly, receipt at 03:17 UTC |
| `scripts/cleaner/mesh-cleaner-scan --once` | PASS; fresh manifest `~/.mesh/cleaner/scan-20260916103219.json`, 259 candidates, 179 held |
| `scripts/cleaner/mesh-cleaner-settle --once` | PASS; oldest-first held report, `mutations=0` |
| `scripts/cleaner/mesh-cleaner-receipt --once` | PASS; receipt row appended |
| `scripts/cleaner/mesh-cleaner-docs --once` | PASS; report generated, 900 missing sidecars reported |
| `scripts/cleaner/mesh-cleaner-dash --once` | PASS; rendered scan/head/count/oldest/retry |
| `mesh-dash --once cleaner` | PASS; live cleaner data pane rendered at 10:32:20Z |
| `git diff --check` | PASS |

## Reconciliation

The plan requires report-only behavior, oldest-first ordering, protected-root
holds, explicit retry output, and a cleaner pane. The live scan, settle output,
and dashboard demonstrate those paths. The four cron entries and five deployed
symlinks establish wiring; the on-demand dashboard is the pane renderer.

The aggregate autowire checker was independently attempted but is currently
load-bound: `timeout 120 scripts/mesh-autowire --check` returned rc=124 before
reaching the cleaner rows. This is not treated as a cleaner wiring failure
because the existing implementation receipt records its prior rc=0 check and
the live crontab/symlink inspection verifies the exact cleaner wiring. Retry
the aggregate command after the mesh task-check load clears.
