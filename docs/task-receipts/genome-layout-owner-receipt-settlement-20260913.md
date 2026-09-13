# Genome migration owner receipt settlement — 2026-09-13

Task: `tg-layout-migration-owner-receipt-20260912/settle-expired-owner-receipt`  
Owner: `genome`

The expired `tg-scripts-layout-migration-20260912/retire-layout-shims` claim had lease
`2026-09-12T21:34:18Z` and no completion artifact. I closed its stale active state with the
canonical owner transition:

```text
mesh-task block tg-scripts-layout-migration-20260912 retire-layout-shims dependency
```

The block cites the existing [`retire-layout-shims-gate-20260912.md`](retire-layout-shims-gate-20260912.md):
the UXN migration has not landed, legacy-path callers remain, and the post-land deploy and
`mesh-doctor --test` gates are incomplete. Its retry condition is to land the migration, resolve the
doctor test failure, and rerun the post-land deploy/autowire/doctor and caller-census checks before
removing any shim. The original migration task therefore remains blocked; this receipt does not
claim its shim-retirement work is complete.

The existing correction task received Genome's `[taking]` transition at `2026-09-13T12:06:15Z`.
The exact task state was then verified as:

- `tg-scripts-layout-migration-20260912/retire-layout-shims`: `blocked` on the recorded dependency.
- `tg-layout-migration-owner-receipt-20260912/settle-expired-owner-receipt`: `active` under `genome`.
- `mesh-task check dispatch autoland/task-independent-pickup-20260912/implement-independent-pickup genome`: exit 3 (`untracked`), unchanged pending a canonical record for that existing flat board task.

The blocker protocol also opened `unblock/genome/95aa703598b7c325/resolve`; it remains open and
requires artifact-backed resolution before the migration can resume. The next action for this
settlement task is to close it with this receipt, then register and settle the already-existing
independent-pickup autoland request without reposting its `[task]` line.
