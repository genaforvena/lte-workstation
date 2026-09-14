# Resolver receipt: `unblock/adint/04121d2ccec59b9b/resolve`

- Checked: 2026-09-14T09:28:55Z UTC on `mesh-home`.
- Resolver resumed on the event `haunt-a08-scope-amendment-20260912-froze-operator-selected-dictionary-v1-manifest-and-corpus`.
- Original work: `haunt-install-unblock-20260907/install-and-retry-tinyfleet` (owner `haunt`).
- Parent task is already `DONE`, artifact-backed by `/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-a08-scope-amendment-20260912.md` (receipt SHA-256 `dc3258137018f05c1912dd29e165d77e44a26f0acf2b86f208d3a11e44053bcf`).

## Dependency preflight

The completed scope amendment freezes the operator-selected synthetic A08 input. A fresh read-only
preflight confirmed the exact source, language, normalization, immutable version, and corpus:

| Field | Frozen value | Current verification |
|---|---|---|
| Source | `tiny-fleet/corpus/applications/noisy-text-correction/manifest.json`; CC0-1.0, synthetic-only | SHA-256 `17879f42f885b18ed5e0638a6620ff745200ddb79d9a3004a20fa22933ea0997` |
| Language | `en`, `ru` | Present in the frozen input manifest |
| Normalization | No Unicode normalization or case folding; exact, case-sensitive `str.replace`; no tokenization | Implementation SHA-256 `69330b7803f0844198c84f07d54cc89e822d4df9abc63ddfb58b6c3c921c60db` |
| Version | Git commit `ed7fa28fb2b010f0cd1294b6df36bf53a5d21396` | `git cat-file -e '<commit>^{commit}'` succeeded in `/home/mesh-home/tiny-fleet` |
| Materialized corpus | `/home/mesh-home/tiny-fleet/runs/operator-selected-dictionary-v1/corpus.jsonl`; 152 rows | SHA-256 `81a41340c0c01555a536e9aa30b3b2b72b1dd9ae48908014fd0f58192515dcd3`; `wc -l` = 152 |
| Frozen input manifest | `/home/mesh-home/tiny-fleet/runs/operator-selected-dictionary-v1/input-manifest.json` | SHA-256 `9081dd78b28ed94b501016698cd6d5347095a5ea079730bf888123c3ec2e1e08` |

Commands used were read-only: `sha256sum` on the four files above, `wc -l` on the materialized
corpus, `git cat-file -e` on the pinned commit, and `mesh-task status haunt-install-unblock-20260907`.
The last command reported the parent chain complete and the `install-and-retry-tinyfleet` step done
with the cited A08 scope-amendment receipt.

## Disposition and boundary

The former missing-input condition is satisfied for the parent's amended A08-only closure criterion.
The parent already completed that criterion, so there is no parent step to resume or rerun. No
comparison or matrix was run in this resolver. The amendment explicitly leaves broader correction
behavior `INCONCLUSIVE` and does not establish BbyWVY dictionary behavior. Any future BbyWVY
dictionary claim still requires its own compatible dictionary arm and declared comparison gate;
that gate must pass before its comparison or matrix runs.

The resolver is therefore complete: the named dependency was frozen and hashed, and the referenced
parent is already terminal on its amended narrow criterion.
