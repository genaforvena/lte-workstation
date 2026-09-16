# Receipts and artifacts moved out of this repository

Date: 2026-09-16.

`docs/task-receipts/` (and the earlier `task-receipts/`, `artifacts/` corpora) are **node-local
evidence**, not repository material. They now live under the node's evidence root:

| was (in repo) | now |
|---|---|
| `docs/task-receipts/x.md` | `~/.mesh/evidence/receipts/x.md` |
| `task-receipts/x.md` | `~/.mesh/evidence/receipts/x.md` |
| `artifacts/x/y.txt` | `~/.mesh/evidence/artifacts/x/y.txt` |
| `docs/audits/x.md` | `~/.mesh/evidence/audits/x.md` |

Resolve any path, including the legacy spellings above, with:

```bash
mesh-evidence-dir --resolve docs/task-receipts/x.md   # → ~/.mesh/evidence/receipts/x.md
mesh-evidence-dir receipts                            # → the receipts root
mesh-evidence-dir --mkdir receipts                    # → create it, print it
```

The root honours `MESH_EVIDENCE_ROOT`, then `$MESH_DIR/evidence`, then `~/.mesh/evidence`.

## Why

While receipts lived in the repo, every receipt write made the genome working tree dirty. That made
each receipt a **landing candidate** and minted a priority-100 `land-dirty-<sig>` incident owned by
`genome`, so evidence volume drove genome load — 51 genome-owned receipt/land chains by 2026-09-16,
and a commit stream of `mesh-land: update docs/task-receipts/...` one file at a time. Now nothing in
the repo changes when a receipt is written, so there is nothing to land.

`scripts/mesh-land` additionally filters the evidence trees out of the dirty-surface guard, so a
receipt written back into the repo by habit cannot mint a genome incident either.

## Ledger note

Ledger rows and earlier receipts that cite the old in-repo paths are **not** rewritten. Resolve them
with `mesh-evidence-dir --resolve <path>`; the content is preserved under the evidence root (the
migration was verified byte-for-byte). A row whose artifact no longer resolves in-repo is a path to
resolve, not a lost artifact.
