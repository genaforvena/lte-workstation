# TG operator ask intake receipt — scripts audit initiative

Ask key: `20260907T145046Z`

The operator asked for a substantial LTE Workstation repository initiative: audit
`scripts/` and the surrounding codebase, produce a map of scripts and relationships,
identify duplicates and dead code, assess risks and priorities, and then create concrete
tasks for sorting and ordering the work.

This receipt admits the exact ask into a durable owner chain:

- chain: `tg-operator-scripts-audit-20260907`
- owner: `tg`
- step: `admit-and-dispatch`
- source: `docs/ledger-coverage-audit-20260907.md`, finding 1 / ask `20260907T145046Z`
- intended next artifact: the evidence-backed scripts/code audit and its task mapping

Verification at intake:

```text
ask 20260907T145046Z is present in mesh-promises --asks
owner-authored [taking] and [done] receipts are posted for this chain
mesh-task status tg-operator-scripts-audit-20260907 is complete
artifact SHA-256 is recorded in the task-chain JSON and board [done] receipt
stale promise tg-operator-intake-owner has an explicit reconciliation disposition
```

This artifact closes the intake/dispatch obligation only. The substantive repository
audit and sorting tasks remain downstream work owned by their dispatched chain steps.
