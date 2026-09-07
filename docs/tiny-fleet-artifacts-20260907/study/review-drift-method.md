# Independent drift-method review — 2026-09-07

## Verdict

**FAIL for publication as a cross-repository drift study; PASS for the evaluator's
mechanical evidence gates.** The study is an honest blocked pilot, not evidence of
general architectural or conceptual drift.

## Evidence checked

- `study-status.json`, `corpus-manifest.json`, and `raw-evaluator-results.json` are
  present in this directory and cross-reference one another.
- `raw-evaluator-results.json` has schema `tiny-fleet-evaluator/v1`, protocol hash
  `741473bb402de93196526cc80c675febc5efe39d800456005b482f048be92a7c`, and two
  immutable snapshot commits (`5475816081b26a0f9aebb92da844493b19304eef` and
  `946d2a5f6b6bd50b12d0068116c967cd1176525d`).
- Independent rerun: `rtk bash tests/test-mesh-tiny-fleet-evaluator.sh` → PASS.

## Findings

| Check | Result | Finding |
|---|---|---|
| Same-snapshot repeatability | PASS | Metric delta is 0. |
| Mutation negative control | PASS | Expected and actual SHA-256 match for `scripts/mesh-tiny-fleet`. |
| Leakage control | FAIL | Snapshot B contains 6 duplicate blobs; the result must not be treated as clean. |
| Provenance | PASS | Snapshot commits and protocol digest are recorded. |
| LoRA/QLoRA arm | BLOCKED | `torch`, `transformers`, and `peft` are unavailable; no proxy result is permitted. |
| Cross-repository coverage | BLOCKED | Only `lte-workstation` resolved; external candidates lack immutable commits and license evidence. |
| Metric interpretation | LIMITED | Only lexical and structural metrics were measured; no behavioral, generative, or calibrated conceptual estimate exists. |

## Required corrections

Resolve immutable commits and license evidence for at least one additional
repository, remove or explain duplicate blobs before collection, then rerun the
preregistered controls. Any report must label the current result as a blocked,
single-repository lexical/structural pilot.
