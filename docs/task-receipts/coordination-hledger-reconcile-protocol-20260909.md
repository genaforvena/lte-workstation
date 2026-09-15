# Reconciliation protocol receipt — 2026-09-09

Task: `coordination-hledger-reconciliation-extension-20260909/reconcile-protocol`

## Protocol

`mesh-hledger-reconcile` runs hourly at minute 27, after the existing hourly ledger feeds at
minutes 7 and 19. Each run freezes one UTC cutoff at invocation (`--cutoff` can supply a replayable
cutoff) and writes a report-only snapshot to `~/.mesh/reconciliation/latest.txt`.

The source matrix is:

| Source | Watermark | Independent question |
|---|---|---|
| `~/.mesh/chat.log` | lines at/before cutoff, whole-file SHA-256, mtime | what was posted to the board? |
| `mesh-task replay --json` | replay-output SHA-256 | what task state reconstructs from the task source? |
| `git log` | commit count and commit-list SHA-256 through cutoff | what repository history landed? |
| `docs/task-receipts/` | cutoff-bounded file count and aggregate SHA-256 | what durable artifacts exist? |
| `mesh-promises --check`, `mesh-ledger --check`, `mesh-labor --check` | PASS/FAIL/UNKNOWN verdict | do existing accounting views pass their own checks? |

The report uses these difference classes: `MATCH` (the compared counts agree), `SOURCE_ONLY`
(one source has rows the other does not), `LEDGER_ONLY` (a journal row lacks a source event),
`STATE_MISMATCH` (same identity, different state), `DUPLICATE` (same identity more than once),
`LATE` (event timestamp is behind the frozen watermark), `UNAVAILABLE` (source cannot be read),
and `UNKNOWN` (comparison cannot be established). The implementation emits `UNKNOWN` when a
required board or task source is unavailable; it never converts absence into zero or equality.

## Adjustments

The reader never writes an accounting journal. A human-authorized adjustment must be appended as a
new transaction, preserving history, with this format:

```hledger
2026-09-09 * reconciliation adjustment ; recon_id=<id> cutoff=<UTC> source=<source> class=<class> reason=<short-reason> evidence=<path-or-hash>
    expenses:reconciliation:<class>:<id>       1 ADJUSTMENT
    equity:reconciliation                       -1 ADJUSTMENT
```

The amount, accounts, source evidence, and reviewer authorization must be explicit. `ADJUSTMENT`
is a non-cash marker and must not be used to force balance, erase a mismatch, revise history,
arm a budget gate, or affect routing/quality scores. If an adjustment is not authorized or source
evidence is unavailable, retain `UNKNOWN` and do not book it.

## Implementation and verification

- Added [`scripts/mesh-hledger-reconcile`](../../scripts/mesh-hledger-reconcile), including frozen
  cutoff, source watermarks, read-only accounting checks, classification, and `--run`/`--test`.
- Added [`tests/test-mesh-hledger-reconcile.sh`](../../tests/test-mesh-hledger-reconcile.sh), which
  uses isolated board/task/artifact fixtures and stub accounting checks.
- Added the self-wiring cadence header; `mesh-autowire` is the wiring authority and will add the
  deployed line only after the tool's `--test` passes. The source header is the durable wiring
  declaration; no direct journal or routing change was made.
- Red phase: the new fixture failed because the production tool did not exist (`rc=1`).
- Green phase: `bash tests/test-mesh-hledger-reconcile.sh` passed.
- `bash -n scripts/mesh-hledger-reconcile tests/test-mesh-hledger-reconcile.sh` passed.
- Current task and board state were rechecked before implementation: task-chain status remains
  `open` at `~/.mesh/task-chains/coordination-hledger-reconciliation-extension-20260909.json`;
  board dispatch is `~/.mesh/chat.log:40713`.

## Unresolved coverage

This receipt does not claim that the new deployed copy or live cron callback has run. Landing and
deployment must occur before the cadence is considered live; an independent acceptance task must
exercise missing, delayed, and balanced-but-incomplete feeds. Existing accounting remains the
source of accounting truth, and this extension remains report-only.
