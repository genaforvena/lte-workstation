# Independent review receipt — tiny-fleet report bundle

**Date:** 2026-09-07  
**Reviewer role:** separate mechanical review pass over the report inputs and claim matrix

## Verdict

**FAIL for publication as a general cross-repository or architectural-drift study; PASS for honest
blocked-pilot packaging.** This is a concrete failure, not a green review: leakage fails, the
LoRA/QLoRA arm is blocked, shuffled conditioning is not run, and the measured evaluator covers one
repository only.

## Checks performed

| check | result | evidence |
|---|---|---|
| report schema and required files | PASS | report.json, report.md, methodology, matrix, roadmap present |
| raw-to-report numeric reconciliation | PASS | C01–C03 equal evaluator/uncertainty JSON |
| control reconciliation | PASS | C04–C06 equal control-results JSON |
| arm separation | PASS | C07–C08 equal arm-separation/preflight |
| corpus/generalization boundary | FAIL/BLOCKED | C09–C10; one measured repo and missing behavioral evidence |
| leakage | FAIL | six duplicate blobs in snapshot B |
| fine-tuning | BLOCKED | torch, transformers, peft absent |

The pre-existing `study/review-drift-method.md` independently reaches the same publication
disposition. This receipt does not upgrade any failed or blocked arm.

## Required correction

Resolve corpus provenance, duplicate leakage, behavioral controls, and genuine fine-tuning evidence;
then repeat this review from regenerated raw artifacts.
