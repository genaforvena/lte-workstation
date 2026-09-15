# Tiny Fleet operator-ideas reconciliation — independent verification

Date: 2026-09-12 UTC  
Task: `tinyfleet-operator-ideas-20260912/verify-operator-ideas-reconciliation`

## Verdict

**Verified with the stated evidence gates still blocked.** All five predecessor artifact digests
match their task-ledger values. The paired-project-DNA raw-artifact checksum manifest passes, and the
reports consistently preserve the leakage, data-independence, and genuine-update failures. The
capacity comparison correctly remains blocked; no evidence supports promotion or a larger-model
comparison. This is an integrity and disposition pass, not a successful model-evidence result.

## Independent checks

Recomputed the ledger-recorded SHA-256 for each predecessor artifact:

| Step | Observed SHA-256 | Ledger match |
|---|---|---|
| `verify-bbywvy-baseline` | `0725dfd82293d45549af146d92a2b0f40b2992ce1e18371c9ae0c19af403fab8` | yes |
| `reconcile-persona-code-evidence` | `3ed40d3707f0c4696cb1f243778fee6d434371cf293b116062f539de11ac24b7` | yes |
| `paired-project-dna-snapshots` | `aa70bffd121669481f2f8d8af9b3e8f92f064db5fc3da55e1ae53152ed37da94` | yes |
| `rank-and-shadow-replacement-lane` | `646777b31f0e7ac75d338408f942dc3dd47c7531b9cfd21be5589bcec52004fe` | yes |
| `capacity-ladder-after-360m` | `bbd44fb812e376078cf1ee642aed85e99445b654a8eaaed6090733a9d60eaf39` | yes |

`sha256sum -c docs/tiny-fleet-artifacts-20260912/paired-project-dna/checksums.sha256` passed all
15 entries, including the evaluation, uncertainty, controls, mutation-negative, resource, runtime,
snapshot, and pinned-model raw outputs. The replacement shadow JSON is present (SHA-256
`467e7384b9a727fd1a4738fe7400d62b202b48a521a86d3d66a68781a88e9650`) and its README describes
the ambiguity, adversarial, escalation, and missing-candidate fallback fixtures and their outcomes.

The evidence supports these retained dispositions:

- Baseline: exact pinned BbyWVY-360M revision and weight/tokenizer hashes are recorded; the receipt
  reports a real offline inference smoke. This proves availability, not study validity.
- Persona/code corpus: the reconciliation says `insufficient-data` (synthetic-only rows and
  non-independent held-out text); no retraining is proposed.
- Paired snapshots: machine-readable results report leakage `fail` (6 duplicate blobs in A, 19 in
  B), count recovery failure, and no leakage-clean split or genuine-update adapter. The
  mutation-negative artifact records the expected deliberate mutation failure; repeatability,
  path-order, and swapped-label controls pass. Shuffled conditioning is explicitly `not_run`.
- Replacement shadow: the recommendation is HOLD; routing is unchanged. The README records the
  incomplete ambiguous/basic answers, policy block, out-of-domain escalation, and fallback result.
- Capacity ladder: BLOCKED before larger-model comparison; neither 1B nor 1.5B was run, and no
  comparison cost row was invented.

Verification commands run from this repository:

- `sha256sum -c docs/tiny-fleet-artifacts-20260912/paired-project-dna/checksums.sha256` — all 15
  entries OK.
- `bash tests/test-mesh-tiny-fleet-validation.sh` — PASS, including corpus-fixture and immutable
  lock checks.
- `bash tests/test-mesh-tiny-fleet-evaluator.sh` — PASS; the deliberate mutation-negative gate
  fired as expected.

The live ledger showed this exact step OPEN for owner `witness`; `mesh-task check dispatch …
witness` exited 0 before the owner-authored take. The board had one dispatch and then one
`[taking]` for this step; no duplicate corrective task was created. The pane sweep also showed
existing unrelated health/FYI warnings, including an overdue health-owned triage row and repeated
daemon/charter-watch observations; these were left with their existing owners.

## Scope and next gate

No routing, model configuration, source dataset, or training output was changed. A future study
requires a genuinely independent, leakage-clean split and a real adapter before genuine-update
claims; rerun the 360M controls on that evidence before selecting any larger comparator.
