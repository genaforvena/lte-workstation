# Synthesized drift methodology — 2026-09-07

## Publication status

**Blocked for publication as a cross-repository drift study.** The validated result is a
single-repository, lexical/structural pilot with mechanical evaluator gates. It is not evidence
of general architectural or conceptual drift.

This synthesis is bounded by the independent review in
[`review-drift-method.md`](review-drift-method.md), the frozen
[`tiny-fleet-protocol.md`](../../tiny-fleet-protocol.md), and the raw run artifacts listed below.

## Validated scope

- Unit: one repository paired across two immutable snapshot commits.
- Resolved corpus: `lte-workstation` only; external candidates remain excluded because immutable
  commit and license evidence were not resolved.
- Available measured arms: deterministic structural metrics and lexical metrics.
- Prompt-only is a control-only arm; it is not a fine-tuning result.
- Provenance records snapshot commits, absolute snapshot paths, and the protocol SHA-256.
- Structural output records file counts, bytes, extensions, generated/malformed exclusions, path
  signature, and changed paths.
- Lexical output records vocabulary size, token count, and top terms.
- Same-snapshot repeatability is reported as a zero metric delta.
- The mutation control passes when the expected file digest equals the observed snapshot-B digest;
  changing the file makes the evaluator exit non-zero and report `mutation.status=fail`.

## Non-claims and explicit limits

- Leakage control is **FAIL**: snapshot B contains six duplicate blobs. No clean or publishable
  cross-repository estimate may be derived from this run.
- LoRA/QLoRA is **BLOCKED** because `torch`, `transformers`, and `peft` are unavailable. No
  prompt-only or Modelfile result may substitute for a genuine weight-update arm.
- There is no measured behavioral, generative, embedding-calibrated, or conceptual-drift estimate.
  Lexical and structural change must not be called architectural drift without the missing
  behavioral and calibration evidence.
- The result is not general across repositories, models, or time intervals; it is a blocked pilot.
- Missing data is represented as `blocked` or `na`, never as zero.

## Reproduction and acceptance gates

Run from the repository root:

```bash
bash tests/test-mesh-tiny-fleet-evaluator.sh
bash tests/test-mesh-tiny-fleet-validation.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/mesh-tiny-fleet-evaluate
```

The evaluator test must pass its clean fixture and must observe the deliberate mutation-negative
control as a failure. The study artifact must retain the leakage failure and blocked fine-tuning
state rather than converting either into a green result.

## Required next experiment

1. Resolve immutable commits and license evidence for at least one additional repository.
2. Remove or explain the six duplicate blobs before collection and rerun leakage controls.
3. Re-run all preregistered controls, including disjoint repository/blob/near-duplicate/time
   splits and the held-out reserve.
4. Install and verify the genuine `torch`/`transformers`/`peft` fine-tuning stack plus an
   accelerator, then retain configuration, resource logs, adapter hash, and before/after
   predictions. Until then, keep LoRA/QLoRA blocked.
5. Add behavioral/generative and calibrated metrics before interpreting any result as conceptual
   or architectural drift.

## Source artifacts

- `study-status.json` — blocked pilot verdict and next experiment.
- `review-drift-method.md` — independent PASS/FAIL/BLOCKED review.
- `corpus-manifest.json` — corpus and exclusion provenance.
- `raw-evaluator-results.json` — evaluator output, schema `tiny-fleet-evaluator/v1`.
- `../evaluator/drift-evaluation.json` — evaluator output retained from the pilot run.

