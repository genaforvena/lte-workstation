# tiny-fleet operator ideas — genome enrichment

Status: proposed additions for the existing tiny-fleet work, recorded 2026-09-06.
This note does not rewrite the live `mesh-task` chain or move its cursor. It is the durable
brief to use when genome reaches the open model/corpus/evaluation steps.

## Source thread

The operator's latest relevant Telegram inputs are in `~/.mesh/textin.log`:

- 2026-09-03 03:01 — test `StarpowerTechnology/BbyWVY-360m` and its published claims.
- 2026-09-03 04:05–04:17 — try replacing one practical mind first (sound was the suggested
  candidate), then train a small model on the operator's own speech/messages because the style
  corpus may already be large enough.
- 2026-09-03 05:56–06:11 — compare tiny code models (including 1B/1.5B Linux-trained models),
  but start by continuing with SmallLM2/BbyWVY 360M; use the model as a compressed “fossil” of a
  codebase's culture and compare models trained on different project versions to observe its DNA
  changing over time.

These are hypotheses and experiments, not evidence that the 360M model can safely replace a lane.

## Enriched task sequence

### 1. Establish the 360M baseline

Reproduce the exact base model and revision currently available, record whether it is actually
`BbyWVY-360M`/SmallLM2 or a different artifact, and run a cheap inference smoke test. Keep the
existing non-reproduction result for the previously requested BbyWVY path; do not convert a missing
runtime or download failure into a model score.

Artifact: a model identity/preflight record with revision, digest, tokenizer, runtime, device,
load/cold-start/warm latency, memory, and an explicit `available`, `blocked`, or `failed` verdict.

### 2. Build two disjoint 360M specialists

Use the same pinned base and evaluation contract for:

1. **operator-style specialist** — RU/EN Telegram text and transcribed voice, learning style,
   tone, brevity, escalation and abstention; do not train it to memorize current mesh facts;
2. **code-culture specialist** — license-safe `lte-workstation` and `tiny-fleet` code/docs,
   learning idioms such as artifact-first verification, explicit failure, routing, handoff, and
   small-tool composition.

Measure the available corpus before training: source/time counts, language, speaker/file diversity,
near-duplicates, redaction, and minimum independent held-out sources. Split by source/file and time,
not random lines. Keep a factual-recall set separate from style-transfer, so “sounds like the
operator” cannot be mistaken for “knows the current mesh.”

Artifacts: frozen manifests, provenance/redaction report, leakage report, train/validation/heldout/
adversarial JSONL, and a `data-adequate` or `insufficient-data` decision.

### 3. Run the compressed-fossil / project-DNA experiment

Train or condition identical 360M controls on at least two pinned project snapshots (and, if data
allows, an older/newer pair of each). Ask frozen prompts about conventions, error handling,
architecture, and likely implementation choices. Compare:

- base model;
- prompt/retrieval-only conditioning;
- genuine LoRA/QLoRA, when the runtime is available;
- snapshot A vs snapshot B, within-repository and cross-repository.

Score structural convention recovery, held-out code behavior, lexical overlap, calibrated
confidence/abstention, and generative outputs separately. The result is a measured change vector,
not one “culture similarity” cosine. Save raw outputs and enough metadata to distinguish learned
style from copied text or stale facts.

Artifact: one reproducible run bundle per snapshot/model arm, with paired deltas and uncertainty;
missing fine-tuning dependencies remain a blocked arm.

### 4. Test the smallest practical replacement candidate

Use the existing fleet benchmark to rank lanes by task narrowness, safety surface, fallback quality,
and cost. Treat `sound` as the first candidate only if the measured task is genuinely bounded. Run
the 360M specialist in shadow mode against real-shaped fixtures before any routing change:

- compare it with the current sound output and the base/Groq control;
- measure p50/p95 latency, cold/warm cost, memory, timeout and fallback rates;
- include nonsense, ambiguous, adversarial, and operator-escalation cases;
- require abstain/escalate on low confidence and preserve the existing fallback;
- make a route/hold/reject decision from the artifact, never from a plausible demo.

No live lane replacement is implied by this task. A wiring step needs its own owner and independent
verification after the model artifact passes.

### 5. Capacity ladder only after the 360M evidence

Only after the 360M run is reproducible, compare current small code models (including the suggested
1B/1.5B Linux-trained family) under the same prompts, snapshots, controls, and cost columns. Check
the current model roster/revisions at run time; do not hard-code the older Qwen-3 assumption from the
thread. The larger model is a comparator and possible later candidate, not a reason to skip the
360M baseline.

## Acceptance gates

Genome should leave the work explicitly `blocked` rather than claiming success when any of these is
missing: pinned model identity, corpus adequacy, held-out separation, genuine fine-tuning evidence,
raw predictions, calibration/abstention, cost data, fallback exercise, or snapshot provenance.

The first useful result can therefore be a negative one: “360M is not yet suitable for sound,” with
the measured failure slice and the next experiment named.
