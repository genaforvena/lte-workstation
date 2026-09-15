# Tiny-fleet expansion plan audit — 2026-09-12

## Verdict

The expansion plan is decomposable into five artifact-gated tasks. A prior three-task outline
exists in `docs/implementation-tasks-20260907.md`, but no canonical `tinyfleet-expansion` chain
was present in the task ledger. The executable decomposition is
`docs/plans/2026-09-12-tiny-fleet-expansion.tsv`, intended for chain
`tinyfleet-expansion-20260912`.

The existing study remains an honest blocked pilot. Its LoRA/QLoRA arm is still blocked and must
not inherit evidence from the separate mood-LoRA experiment in `/home/mesh-home/tiny-fleet`.

## Package-to-task map

| Plan package | Durable task | Artifact and gate |
|---|---|---|
| Freeze protocol; assemble corpus; provenance | `protocol-corpus-lock` | Versioned protocol/corpus manifests and exclusion ledger; immutable commit and license evidence required before a candidate is usable. No download is authorized by the plan. |
| Reproducible fixtures; splits and leakage boundaries | `fixtures-and-split-audit` | Fixture inputs/outputs, deterministic rebuild report, and disjoint split evidence; malformed, duplicate, generated, exact-copy, and near-duplicate cases must be exercised. |
| Structural, lexical, architecture, and uncertainty ladder | `structural-lexical-measures` | Raw rows, per-repository/per-stratum metrics, denominators, missingness, and uncertainty; absent parsers/arms remain `na` or `blocked`. |
| Behavioral/generative controls and genuine update arm | `behavior-controls-and-lora-preflight` | Control/mutation results and runtime preflight; LoRA/QLoRA may be `measured` only with a real adapter and its run evidence. Missing prerequisites leave it `blocked`, never prompt-only. |
| Report, cost package, witness rerun, and claim review | `report-and-independent-review` | Claim-to-artifact matrix, report bundle, checksums, independent controls/mutation rerun, and explicit dispositions for all blocked arms. |

The tasks are ordered in the TSV so fixture work follows the corpus lock, measurement follows the
fixtures, and review follows the measured bundle. This decomposition covers all seven work packages,
controls, package/review requirements, and acceptance gates in `docs/plans/2026-09-07-tiny-fleet-expansion.md`.

## Live evidence and arm disposition

- `docs/tiny-fleet-artifacts-20260907/study/study-status.json` says the study is `blocked`, with
  only `lte-workstation` resolved. It records lexical and structural as measured; prompt-only is
  ready, not measured. The leakage control fails with six duplicate blobs in snapshot B.
- `docs/tiny-fleet-artifacts-20260907/study/preflight/preflight_20260907T101228Z.json` records
  `torch=false`, `transformers=false`, and `peft=false`, while the LoRA/QLoRA arm is `blocked` with
  reason “fine-tuning prerequisites unavailable; no proxy permitted.”
- `docs/tiny-fleet-artifacts-20260907/study/close-drift-methodology.md` and
  `review-drift-method.md` both preserve the blocked/pilot-only interpretation and name the next
  provenance and leakage work.
- The separate `tinyfleet-specialists/mood-lora-bench` task is complete, with a real training run
  and witness verification recorded in `docs/coordination-mood-lora-runtime-rerun-20260907.md`
  and `docs/coordination-mood-lora-verify-20260907.md`. That experiment uses another corpus,
  objective, and base model in `/home/mesh-home/tiny-fleet`; it does not change the drift-study
  preflight or arm state.

## Verification performed

- `mesh-task status design-audit-task-sweep-20260907` confirmed this audit step was active and
  owner-assigned to `tg`.
- `mesh-task status tinyfleet-specialists` confirmed the separate mood-LoRA task and witness step
  are complete.
- `mesh-task status tinyfleet-drift-methodology` confirmed its closeout is 7/7 and retains the
  blocked study disposition.
- Reviewed the current protocol, study status, preflight, closeout, and independent review
  artifacts. No study state or LoRA artifact was changed.

## Unresolved obligations

No execution task is complete merely by this audit. Corpus expansion, additional immutable/license
evidence, leakage remediation, behavioral measures, and the LoRA/QLoRA preflight remain open in the
new chain. The first implementation step is `protocol-corpus-lock`; keep the fine-tuning arm blocked
until its own prerequisites pass and its adapter/run artifacts exist.
