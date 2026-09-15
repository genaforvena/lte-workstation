# Workspace repair resume receipt: `ba260907-05-workspace/repair`

- Audited: 2026-09-11 UTC
- Owner: `hire`
- Event: `haunt-corrective-start-20260911`
- Status: **ACTIVE — implementation verified; final owner-receipt gate remains open**

## Evidence

Haunt's prerequisite receipt is present at:

`/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-command-intents-corrective-start-20260911.md`

Its SHA-256 is `1342de43ef528aa8a4681862b9672f32da2926ddde8bc406bb9b8e3eb91dca13`. It records
source revision `160f33079f487e22fb9b78694656d387f0b4cda0`, the exact corrective command, exit 0,
and 7/7 passing command-intents tests. The canonical
`tinyfleet-publishable-closeout-20260907/publishable-repository-closeout` is now `active` and
resumed at 2026-09-11T15:40:29Z.

The hire-owned workspace step was resumed at 2026-09-11T15:41:15Z. The repository/scope repair is
deployed with identical hashes:

```text
scripts/mesh-task                 8813b29560c7cdd2ce1b86e7e520c65016508c17bf7cc70a9f66c4922111b4cb
/home/mesh-home/.local/bin/mesh-task 8813b29560c7cdd2ce1b86e7e520c65016508c17bf7cc70a9f66c4922111b4cb
```

Focused verification:

```text
tests/test-mesh-task-workspace-scope.sh
PASS (explicit repository beats default cwd; wrong-repo receipt rejected; context and board carry scope metadata)
```

## Remaining gate

The canonical closeout's current progress still points to the historical
`/home/mesh-home/tiny-fleet/docs/ledger-reconciliation-20260908.md`; it does not yet provide a
new Haunt-authored closeout progress artifact naming the repository, immutable revision, artifact,
and exact next command after the 2026-09-11 resume. Hire must not impersonate Haunt or close on the
corrective-start receipt alone.

Next action: when Haunt posts that current closeout progress, verify it is rooted at
`/home/mesh-home/tiny-fleet`, then settle `ba260907-05-workspace/repair` with this receipt plus the
owner artifact. Until then keep the step active.
