# Tiny-fleet validation protocol v1

This is the frozen protocol for the expansion pilot. It is an offline, reproducible
starting point; it does not authorize corpus download, live mesh/scheduler wiring, or
model routing.

## Estimands and controls

The primary unit is a repository paired across immutable snapshots. Primary estimands are
per-repository standardized structural/lexical change and held-out convention recovery
delta versus same-snapshot control. Generative divergence is reported only after estimating
repeatability noise. All pooled values are labelled as corpus mixtures and accompanied by
repository/stratum rows. Missing parsers and unavailable arms are `na` or `blocked`, never 0.

Required controls are same-snapshot repeatability, shuffled/unrelated conditioning, swapped
labels, path/file-order permutation, synthetic known change, exact-copy and near-duplicate
leakage challenges, negative abstention prompts, repeated seeds, and base/prompt-only controls.
The final holdout is repository-stratum balanced and is not used for thresholds.

## Immutable run contract

Every run records protocol, corpus, model, evaluator commit, tokenizer, seed, sampling
parameters, output cap, embedding implementation/model digest, runtime and hardware. A run ID
is `sha256(protocol_sha256 + corpus_manifest_sha256 + model_manifest_sha256 + evaluator_commit)`.
Snapshots must be immutable commit IDs; `HEAD` is invalid until resolved. Splits are disjoint by
repository, blob, near-duplicate, prompt family, and declared time boundary.

## Preflight and blocked states

`scripts/mesh-tiny-fleet preflight` writes a JSON artifact under `$TINY_FLEET_DIR/preflight/`.
Structural and lexical arms are available offline. Prompt-only is blocked unless Ollama is
available. LoRA/QLoRA is ready only when `torch`, `transformers`, `peft`, and an accelerator
tool are present; otherwise the artifact records the exact missing prerequisites. A blocked
fine-tuning arm must not be replaced by a Modelfile or prompt-conditioning result.

## Pilot stopping rules

The pilot is capped at six repositories and 1,000 inference calls. Stop on missing license
evidence, unresolved snapshot IDs, split leakage, failed mutation controls, or budget breach.
Keep an exclusion ledger and publish partial/failure artifacts with the next experiment.

## Corpus lock and fixture contract

`mesh-tiny-fleet corpus-lock` is the clean-room freeze step. It accepts only resolved local
repositories with immutable commit IDs, declared SPDX identifiers, and hashed license evidence;
deferred candidates are recorded as exclusions and mutable or missing evidence is a hard failure.
The lock, deterministic source manifest, and fixture report contain no timestamps or network data,
so rebuilding in two fresh directories must produce identical SHA-256 values.

The fixture input contains toy train/held-out rows, exact-copy and renamed-copy leakage pairs, an
adversarial abstention row, an empty file, malformed/generated exclusion cases, and their expected
hashes. Fixture provenance is explicitly test-input-only and makes no redistribution claim. A
mutation of a locked commit or protocol must fail rather than silently produce a new green lock.
