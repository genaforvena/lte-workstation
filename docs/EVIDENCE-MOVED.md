# Receipts, artifacts and plan files moved out of this repository

Date: 2026-09-16.

`docs/task-receipts/`, `docs/audits/` and `docs/chat-range-reviews/` (and the earlier `task-receipts/`,
`artifacts/` corpora) are **node-local evidence**, not repository material. They now live under the
node's evidence root:

| was (in repo) | now |
|---|---|
| `docs/task-receipts/x.md` | `~/.mesh/evidence/receipts/x.md` |
| `task-receipts/x.md` | `~/.mesh/evidence/receipts/x.md` |
| `artifacts/x/y.txt` | `~/.mesh/evidence/artifacts/x/y.txt` |
| `docs/audits/x.md` | `~/.mesh/evidence/audits/x.md` |
| `docs/chat-range-reviews/x.md` | `~/.mesh/evidence/chat-range-reviews/x.md` |
| `docs/chat-range-reviews/x.md.findings.json` | `~/.mesh/evidence/chat-range-reviews/x.md.findings.json` |

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
receipt written back into the repo by habit cannot mint a genome incident either. The writers point at
the evidence root too, so a corpus is not recreated by the next run: `mesh-chat-range-review` names
`$(mesh-evidence-dir chat-range-reviews)` in the review prompt it hands to witness.

## Scratch plans

Plan files are work **inputs** (`mesh-task create <chain> <plan.tsv>`), not records of finished work, so
they have their own root rather than living under the evidence root:

| was (in repo) | now |
|---|---|
| `docs/task-plans/x.tsv` | `~/.mesh/plans/x.tsv` |
| `task-plans/x.tsv` | `~/.mesh/plans/x.tsv` |
| `docs/plans/x.tsv` | `~/.mesh/plans/x.tsv` |
| `docs/x.plan.tsv` | `~/.mesh/plans/x.plan.tsv` |
| `.mesh-tg-<slug>.plan.tsv` (repo root) | `~/.mesh/plans/.mesh-tg-<slug>.plan.tsv` |

```bash
mesh-evidence-dir plans                              # → the plans root
mesh-evidence-dir --resolve docs/task-plans/x.tsv    # → ~/.mesh/plans/x.tsv
```

The root honours `MESH_PLANS_DIR`, then `$MESH_DIR/plans`, then `~/.mesh/plans`.

### The rule

New plans are written to the plans root, never into the tree:

```bash
mesh-evidence-dir --mkdir plans                      # → ~/.mesh/plans
mesh-task create <chain> ~/.mesh/plans/<name>.tsv <ask-key>
```

Legacy tracked plan files stay put for now: `docs/plans/` (69 `.tsv` + 6 `.md`) and `docs/*.plan.tsv`
(10) are tracked repo material with tracked siblings — and a *tracked* edit is exactly what the
landing path covers. They are cited by other documents, so migrating them is a deliberate change of
its own rather than something a stray-file cleanup should decide. Both spellings resolve through
`mesh-evidence-dir`, which keeps either choice cheap.

Unlike the evidence corpora these were **not** a genome load, and it is worth being exact about why:
`mesh-land` enumerates *untracked* files only from an explicit allowlist (`scripts/`, `job/`,
`bootstrap.sh`, `setup.sh`, and the `UNTRACKED_DOC_PATHS` set), which has never listed
`docs/task-plans/`. The *tracked* arm is broader — it covers `charter/ docs/ task-receipts/ memory/
skills/ tests/` — so a plan file that is tracked and edited in place does become a landing candidate,
while a brand-new untracked one does not. Moving them out removes the clutter and that edge together.

## Ledger note

Ledger rows and earlier receipts that cite the old in-repo paths (including `docs/task-plans/x.tsv`) are
**not** rewritten. Resolve them with `mesh-evidence-dir --resolve <path>`; the content is preserved under the evidence root (the
migration was verified byte-for-byte). A row whose artifact no longer resolves in-repo is a path to
resolve, not a lost artifact.
