# Dispatch-rejected successors: recovery receipt (2026-09-09)

Durable receipt for `dispatch-rejected-successors-20260909/repair-recovery`.
The source case found 25 successors stranded behind four rejected heads. The
two genome-owned first successors were reactivated with artifact-backed,
owner-authorized transitions; unresolved haunt/operator work remains held for
those owners.

Supported command (run as the exact successor owner):

```sh
MESH_TASK_ACTOR=<owner> scripts/mesh-task recover <chain> <first-successor> <reactivate|hold> <artifact> "<reason>"
```

Exact live commands are recorded in
`docs/task-receipts/dispatch-rejected-successors-20260909-repair-recovery.md`.
`reactivate` records the recovery artifact/hash, preserves the rejected
predecessor and IDs, then dispatches exactly one successor. `hold` records an
artifact/hash and explicit dependency hold without dispatch. Wrong owner,
missing artifact, non-first successor, different replay, or unresolved chain
state is refused; identical replay is idempotent. `scripts/mesh-task audit`
renders unrecovered rows as `HELD_REJECTED`, and `scripts/mesh-task-journal`
preserves that state in the pane.

Verification: `scripts/mesh-task --test` PASS; source and deployed hashes
match for `mesh-task` and `mesh-task-journal`; the source journal materializer
published a live-format task view containing `HELD_REJECTED` rows.

