# Clean inherited temporary fixture — disposition receipt

Task: `shared-index-commit-audit-correctives-20260916/clean-inherited-temp-fixture`
Owner: `genome`
Observed: 2026-09-16T11:33Z

## Delegated inspection and controller verification

One read-only inspection was delegated to the isolated `genome-clean-inherited-fixture`
worker. I personally inspected the reported artifact and reran the decisive checks; the
worker report was treated as a lead, not as evidence.

Commands and results:

```text
stat --printf='path=%n\nsize=%s\n' scripts/.mesh-task-test-tmpdir-t2739fiu/artifact.md
path=scripts/.mesh-task-test-tmpdir-t2739fiu/artifact.md
size=19

sha256sum scripts/.mesh-task-test-tmpdir-t2739fiu/artifact.md
4609ee39390262d5bc2c8a3892d310f2080859346cc99dacc1c7c06f386f80c6

git rev-parse 19a07d80^{commit}
19a07d80af7215004705491bed2f9f1908cdc7e3

git rev-parse 19a07d80:scripts/.mesh-task-test-tmpdir-t2739fiu/artifact.md
eec6f65dfe793560495a1b594dac6b04e897ee82
```

The file contains only `ephemeral evidence`, is tracked and unmodified, and commit
`19a07d80` is an ancestor of the current `HEAD`. Bounded live-chat and ledger searches
found no owner or landing evidence for this fixture. The existing unblock receipt records
the same gap and names this exact corrective task.

## Safe disposition

KEEP for now. Do not delete the fixture: the original commit and evidence must remain
preserved, and ownership/landing evidence is still absent. Removal becomes safe only after
the required corrective receipt is canonically landed and the parent shared-index audit
replay confirms the evidence boundary. Retry then, using the next shared-index audit replay.

No files were deleted or rewritten by this task.

#tags=audit-followthrough
