# H-Ledger reconciliation extension — 2026-09-09

This extends `coordination-hledger-plan-20260908`; it does not replace its existing
accounting-coverage and FYI tasks.

## Why

The mesh needs a recurring reconciliation loop: compare ledger views with independent
sources of truth, classify differences, and record explicit adjustments. H-Ledger
balances are useful evidence, but balance alone cannot prove that a task happened,
was delivered, or had a good outcome.

## Acceptance boundaries

- Reconciliation has a named cadence, frozen cutoff, source matrix, difference classes,
  and an auditable adjustment format. Missing or unavailable sources remain UNKNOWN.
- Any conditional valuation is an explicitly synthetic effort commodity, separate from
  USD/cash and from outcome quality. It must answer a decision that unit counts cannot.
- Mind/load reports expose task count, effort, age, rework/reopen, completion and
  unattributed coverage as separate axes. They must not rank quality from volume alone.
- The report is read-only until separately authorized; no budget gate or routing score
  is armed by this extension.

## Chain

`coordination-hledger-reconciliation-extension-20260909`
