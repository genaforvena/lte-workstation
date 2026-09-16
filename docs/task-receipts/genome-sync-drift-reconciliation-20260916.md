# Genome sync drift reconciliation — 2026-09-16

Task: `genome-sync-drift-reconciliation-20260916/reconcile-drift-clobber`
Source signal: `~/.mesh/chat.log:70693` (`2026-09-16T03:08:17Z`)

## Evidence

The warning says the deployed copies were newer than genome for `mesh-body-motion`,
`mesh-imac-cam`, and `mesh-tg-filter`, and that a genome-to-local heal may have
reverted local-only fixes. The source/deployed SHA-256 pairs are:

| tool | `scripts/` source | `~/.local/bin/` deployed |
|---|---|---|
| mesh-body-motion | `e65c8cf3f1c06324f86db64c70d1d5d69224bdf8637414426c9bf4331d565e38` | `c44252b81a5700a0ca890f44d198b3016e84d4154fe598f313f26eac9264dcaf` |
| mesh-imac-cam | `c9ec268740544bdf2f79dd4898d79d2083bf216ccf5ad5c4a253f0289dcbc682` | `5e04b6c36c54055e77210368805d156b95ddb76818be5d6859ee670c481b5413` |
| mesh-tg-filter | `648529ca565e97dcfefaa05733a1617e23c2e3c37b6a05ff0b52b6d2342760f5` | `2340a1e10626f6d152c577e48cca29316c29280c9de9c779ee664aaf3a65d87d` |

All three pairs differ. Read-only `diff -u` shows the source files are compatibility
shims while the deployed files contain substantially larger implementations, so a
blind `mesh-sync-tools --apply` would replace behavior rather than reconcile a small
drift. The retained backup set is
`/home/mesh-home/.mesh/tools-backup/single-source-20260908T030731Z/` with hashes:

- `mesh-body-motion`: `f8d3c47fa8e56b43bb0e2b1ccee7b1af98faff8061d195f9bdb8519515d62c13`
- `mesh-imac-cam`: `e6923934c7f5b5f4dcfa8ea8acd4d3dda09e42e8ad38e975004b59d7b1495c00`
- `mesh-tg-filter`: `b3d5db807319ff80c5a039a8aa8a921cb28ac13824f2537839bbef89db41367b`

## Decision

**ESCALATE / preserve both sides.** Do not deploy the current shims over the newer
deployed implementations, and do not edit or delete the backup. The source provenance
for the deployed behavior must be recovered and reviewed by the landing/sync steward
before any reapply. This is an internal mesh reconciliation edge, not an operator-input
blocker.

Exact next action: compare the deployed implementations and backup set against their
own originating commits or receipts, recover the intended implementation into
`scripts/` in a scoped change, then run each tool's focused test and `mesh-sync-tools`
parity check before deployment. Until that happens, treat the three deployed/source
pairs as intentional unresolved drift and keep the warning visible.

Verification commands run:

```text
rg -n "drift-clobber.*mesh-home: deployed copy was NEWER" ~/.mesh/chat.log
sha256sum scripts/{mesh-body-motion,mesh-imac-cam,mesh-tg-filter} $HOME/.local/bin/{mesh-body-motion,mesh-imac-cam,mesh-tg-filter}
find $HOME/.mesh/tools-backup -maxdepth 2 -type f ... -exec sha256sum {} \;
diff -u scripts/<tool> $HOME/.local/bin/<tool>
```

No deployed file, backup, substrate, or unrelated worktree path was modified.
