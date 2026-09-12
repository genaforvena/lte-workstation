# Paired project-DNA controls — 2026-09-12

## Verdict

The two-snapshot structural and pinned-base/retrieval controls ran, but this is a **blocked pilot**,
not a clean paired-study result. The snapshots contain substantial exact-blob overlap, the
within-snapshot leakage control fails, and the model missed the count change. Keep the
genuine-update arm **BLOCKED**: there is no leakage-clean training/evaluation split or adapter
artifact. Do not generalize the measurements beyond these two commits.

## Immutable inputs and structural result

- A: `e8f47364e5a0f224c1bd03331df592272a187df5`, committed 2026-09-07.
- B: `5686c478ee3a496a6c87e54791bb026128fa9e2b`, committed 2026-09-12.
- Both commits exist locally and are distinct. Each was extracted with `git archive`; no dirty
  working-tree file entered either snapshot. `snapshots.txt` records the IDs and mutation target.
- The dependency-light evaluator counted 1,441 included UTF-8 files / 30,204,597 bytes in A and
  1,867 / 51,647,384 in B: +426 files and +21,442,787 bytes. It found 554 changed paths and
  lexical JSD 0.019510155653440216. Its file-paired uncertainty has n=1,868 paths and does not
  estimate variation across repositories or model runs.
- Same-snapshot repeatability, sorted path-order invariance, and swapped-label arithmetic passed.
  The positive mutation hash check passed; appending a deliberate mutation made the evaluator exit
  2 with `mutation.status=fail` as expected.
- **Leakage failed:** 6 duplicate blobs in A and 19 in B. Across A/B, 1,314 common paths had the
  same content hash (1,308 unique shared hashes). These snapshots cannot support a clean
  train/held-out claim. The evaluator's `shuffled_conditioning` remains `not_run`; that path has no
  live model-conditioning hook.

Machine-readable structural output is in `evaluation.json`, `uncertainty.json`, `controls.json`,
and `mutation-negative.json`. The temporary extracted snapshots were not copied into this artifact.

## Pinned base and retrieval controls

The model was the reproduced `StarpowerTechnology/BbyWVY-360m` at revision
`154a243ffa13d3259a824c40a23d709d3ea42fa7`, weight SHA-256
`3e26b40ed65c3fcd53e2930c38e3c9b9a5912389e0a6924f047cafa8eaa68c14`, tokenizer JSON SHA-256
`bf346d64f6f0fbcefb4c1b6928a98241467dff36c6fbae5fe1785c4ff90667f`. It ran offline in
`~/.venv-ai` with PyTorch 2.13.0+cu130, Transformers 5.14.1, FP16 on the RTX 3060. `bbywvy-controls.json`
retains the frozen prompts, retrieval extracts, raw responses, hashes, and timing. Greedy decoding
used `do_sample=false`, seed 20260912, and a 48-token cap.

On the exact-count question, the base arm returned placeholders and the retrieval arm answered
`A=426; B=426; delta=0` instead of `A=1441; B=1867; delta=426`. On the changed-path prompt, the
base arm returned `Path: A -> B`; retrieval returned `.codex/hooks.json`, a changed path. In the
sampled seed sweep (temperature 0.7, top-p 0.95, seeds 11/22/33), the count answer was exact once
out of three and the retrieved changed path was valid three times out of three. Raw calls are in
`seed-sensitivity.json`. These two prompts are a small control, not a benchmark or a quality claim.

## Runtime and arm disposition

The original behavior-step preflight used system Python and incorrectly described it as the
training environment. The corrected note is
[`tinyfleet-expansion-behavior-preflight-correction-20260912.md`](../../task-receipts/tinyfleet-expansion-behavior-preflight-correction-20260912.md).
The pinned runtime preflight is in `runtime-preflight/`: Torch, Transformers, PEFT, CUDA, and the
accelerator probe are present, so the LoRA dependency probe is ready. `bitsandbytes` is absent, so
QLoRA is unavailable. Readiness alone does not satisfy this task's genuine-update arm.

The selected node was mesh-home: it had 2,939 MiB free GPU memory before the pinned model run,
17 GiB RAM available, and the model's measured peak CUDA allocation was 740,662,272 bytes. After
the run, 2,772 MiB GPU memory remained free. Phaedra had only 1.3 GiB RAM available and no visible
accelerator or fine-tuning dependencies; the iMac SSH host key was unverified and Windows SSH timed
out. `resources.json` preserves this selection evidence. No packages were installed and no model
weights were modified.

The genuine-update arm is **BLOCKED** because the measured corpus is leakage-contaminated and no
valid independent split is available in this task's inputs. No adapter was trained, so there is no
genuine weight-update output to compare. Retrieval remains a control-only input path and cannot
stand in for a weight update.

## Verification

- `bash tests/test-mesh-tiny-fleet-validation.sh` — exit 0.
- `bash tests/test-mesh-tiny-fleet-evaluator.sh` — exit 0; its deliberate mutation-negative gate
  fired.
- Paired evaluator mutation-positive run — exit 0; mutation-negative run — exit 2 with the
  expected `fail` record.
- BbyWVY pinned model loaded offline and completed four greedy controls plus six seeded retrieval
  calls. Peak CUDA allocation and post-run headroom are recorded above and in the JSON artifacts.

The next owner must resolve the leakage split before any genuine-update training or a claim that
snapshot changes are recoverable. The downstream lane-ranking task must preserve this BLOCKED state
until that evidence exists.
