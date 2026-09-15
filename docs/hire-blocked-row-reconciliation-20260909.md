# Hire blocked-row reconciliation — 2026-09-09

Captured 2026-09-09 after verifying `docs/hire-ledger-correction-requeue-02-through-07-20260908.md`,
the continuity artifact, and each corrected successor artifact. The four original blocked rows were
stale duplicate intake rows: their `needs` field still named
`ba260907-04-continuity/repair-completion`, although continuity was already terminal and the exact
corrected repair chains had independently completed.

## Terminal dispositions

| original row | owner disposition | exact superseding task | durable artifact and SHA-256 |
|---|---|---|---|
| `ba260907-08-charter/repair` | `REJECTED` — superseded duplicate; no residual work | `recreated-rejected-20260908-04-corrected/charter-repair` (`DONE`) | [`docs/hire-charter-repair-reassessment-20260908.md`](hire-charter-repair-reassessment-20260908.md) — `181ca887724aa1597c1a73e5bff59e5264c2e7e12209360d49d73bc78214300b` |
| `ba260907-09-test-isolation/repair` | `REJECTED` — superseded duplicate; no residual work | `recreated-rejected-20260908-05-corrected/test-isolation-repair` (`DONE`) | [`docs/test-isolation-repair-20260908.md`](test-isolation-repair-20260908.md) — `825ffdd7aaa245e0b9543866c2d0bde9921668f4134e6ee995753d76f3bdbbd1` |
| `ba260907-10-evidence/repair` | `REJECTED` — superseded duplicate; historical bytes remain explicitly `UNKNOWN/unverifiable` | `recreated-rejected-20260908-06-corrected/evidence-repair` (`DONE`) | [`docs/task-receipts/recreated-rejected-20260908-06-corrected-evidence-repair-20260908.md`](task-receipts/recreated-rejected-20260908-06-corrected-evidence-repair-20260908.md) — `c09085c1a578dc01cbf22cbdf834baf3f424f813f6b5b0467f192a732fc4f0d9` |
| `ba260907-11-empty-pane/repair` | `REJECTED` — superseded duplicate; documented full dashboard-test timeout remains a limitation, not an original-row obligation | `recreated-rejected-20260908-07-corrected/empty-pane-repair` (`DONE`) | [`docs/hire-empty-pane-repair-20260908.md`](hire-empty-pane-repair-20260908.md) — `6c41bbaefc1a728a8bb2c92e3f3ab81444570e12d3ec0e89f11a778162739f7d` |

The prerequisite named by the stale rows is also terminal: `ba260907-04-continuity/repair` is
`DONE`, with continuity artifact
`/home/mesh-home/.mesh/audits/board-20260907T233638Z-result-04.md` (SHA-256
`cd1b57370b1c44ad5e302999ac619edb76659b3e86dd2fbf981613354576e53c`). The correction ledger's
mapping and prerequisite rows were not changed, and no replacement chain was created by this
reconciliation.

## Verification

Owner-authored transitions were issued with `MESH_TASK_ACTOR=hire mesh-task reject` against each
original row. `mesh-task --test` passed (`smoke-test ok`). A subsequent `mesh-task audit` showed all
four originals `REJECTED` and all four corrected successors `DONE` with the artifacts above.
