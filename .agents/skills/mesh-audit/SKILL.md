---
name: mesh-audit
description: Run an audit, review, or reconciliation that promises downstream task creation, with every finding mapped to an exact owner or a reasoned disposition. Use when a task carries the audit-followthrough tag.
---

Every actionable finding from an audit or review must result in an exact-owner
corrective task before the audit settles. First search for an existing active task
that covers the finding and cite it; otherwise create a corrective task naming the
owner, acceptance condition, retry edge, and durable artifact path. A finding
recorded only in a receipt is incomplete.

Canonical task plans use `owner<TAB>step-slug<TAB>description` (or the four-column
form with priority); verify the created ledger row and dispatch eligibility. Mark
every task that performs an audit, review, reconciliation, or other work promising
downstream task creation with the plan header `#tags=audit-followthrough`. Its
completion artifact must have an adjacent `<artifact>.findings.json` file with
`version: 1` and a nonempty `findings` array. Each unique finding is either
`actionable: true` with exact `task` (`chain/step`) and `owner`, or
`actionable: false` with a nonempty `reason`. `mesh-task done` verifies these
mappings against canonical replay; tagged work cannot use `reject` to bypass
disposition, so block it with an exact retry edge or complete it with a reasoned
non-actionable disposition. This tag is explicit metadata, never inferred from a
task name or prose.
