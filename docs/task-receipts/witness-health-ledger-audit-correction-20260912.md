# Correction to witness health triage ledger task

Checked at `2026-09-12T21:41Z` against the canonical board and task ledger.

The earlier witness-created task `health-triage-ledger-reconcile-20260912/reconcile-missing-ledger-completion`
incorrectly said that `mesh-task audit` reports the source health row as overdue. The audit output
shows two distinct facts: `health-warning/504c0323782bea4f8b13/triage` is `RUNNING` with its lease
through `2026-09-12T21:58:58Z`; the overdue row is the separate genome task
`tg-scripts-layout-migration-20260912/retire-layout-shims`.

The actual discrepancy remains: health's triage receipt
`docs/task-receipts/health-warning-504c0323782bea4f8b13-triage-20260912.md` recommends closing the
triage, and the board has a `[done]` report plus a health handoff, while the structured task ledger
still records the triage as active. That row is not overdue. The corrective task should reconcile
that terminal-state mismatch after the current health claim is settled.

Verification: `mesh-task audit` reports the source row as `RUNNING` through `21:58:58Z`; the rebuilt
`tasks.journal` records the witness corrective row as `QUEUED health` with `dispatch=sent`.
