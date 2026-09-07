# Tiny-fleet validation expansion plan

**Date:** 2026-09-07  
**Status:** plan only; no implementation or corpus download is authorized by this document

## Outcome

Turn tiny-fleet from a single-project, two-snapshot demonstration into a reproducible study of
architectural drift across a substantially larger, license-safe corpus. The study must separate
lexical/vocabulary change, structural change, behavioral convention change, and model-induced
generative divergence. It must also retain the current prompt-only arm as a control and add a
genuine LoRA/QLoRA arm when dependencies are available; an unavailable fine-tuning arm is a
blocked result, never a green proxy result.

The existing report is the starting point, not ground truth: it compares `lte-workstation` at
54758160 and `HEAD`, uses Ollama Modelfiles rather than weight updates, reports three generative
prompts and an embedding score, and has a smoke test that does not establish corpus provenance,
leakage resistance, calibration, or live wiring. The expansion must preserve the useful structural
series while making every stronger claim traceable to raw inputs and a run manifest.

## Work packages and order

### 1. Freeze the protocol before collecting data

Create a versioned protocol and preregister the estimands, primary slices, exclusion rules, and
stopping rules. Pin tool versions, tokenizer, random seeds, temperature/top-p, prompt templates,
maximum output tokens, embedding model/digest, similarity implementation, and hardware/runtime
metadata. Define a run ID as a hash of protocol, corpus manifest, model manifest, and evaluator
commit. Do not tune thresholds on the final holdout.

The primary comparison is the paired change between two snapshots of each repository, with a
secondary cross-repository comparison of the same change vector. The report must label any pooled
number as a corpus mixture and publish per-repository and per-stratum values.

### 2. Assemble a substantially larger open-source corpus

Use 30 repositories initially, with a target of 24 usable repositories after exclusions. Select
from public Git hosting using a frozen query date and a manifest containing URL, immutable commit
IDs, default branch, license/SPDX evidence, language mix, stars/forks only as descriptive metadata,
commit dates, repository size, and collection status. Do not select solely by popularity.

Stratify before sampling:

| Stratum | Target | Examples of selection constraints |
|---|---:|---|
| Shell/operations | 4 | mature automation, tests or CI, at least 2 years of history |
| Python application/tooling | 5 | typed and untyped mix, documented public API |
| JS/TS application/tooling | 4 | package-managed, tests, one monorepo at most |
| Systems C/C++/Rust/Go | 8 | at least two languages represented, build/test metadata |
| Libraries/frameworks | 5 | reusable API and release history, not only applications |
| Small interpreters/compilers/data tools | 4 | syntax/architecture changes observable in source |

At least one third must be small projects (1k–20k tracked text/source files or an explicitly
recorded equivalent), one third medium projects, and no repository may contribute more than 20% of
the pooled rows. Exclude repositories with no license evidence, generated-only snapshots, fewer
than two suitable snapshots, primarily binary/vendor content, or a history too shallow to support
the preregistered interval. Keep an exclusion ledger rather than silently replacing candidates.

For each repository choose three immutable snapshots where possible: an early baseline, a midpoint,
and the latest snapshot before the collection cutoff, each separated by a minimum of 12 months or
500 commits. If history does not support that, retain the repository for structural-only analysis
and mark the temporal arm unavailable. Record a fourth, later snapshot only as a locked future
reserve when it exists. Never use `HEAD` without resolving and recording its commit ID.

### 3. Build reproducible, license-safe fixtures

Materialize each snapshot into a content-addressed fixture directory or archive. The fixture
manifest records repository, commit, file path, blob ID, byte size, language, license provenance,
generated/vendor classification, normalization version, and SHA-256. Keep raw source in restricted
research storage if redistribution is not permitted; publish manifests, hashes, extraction code,
and derived features. Do not put secrets, personal data, dependency caches, model weights, or
unlicensed test corpora into the fixture bundle.

Use one canonical file filter and one canonical text normalization. Exclude `.git`, vendored and
generated trees, lockfiles only in a separately reported sensitivity arm, binaries, files above a
declared size cap, and files whose encoding cannot be decoded. Preserve a complete exclusion count.
Create deterministic extraction fixtures with known expected counts for: file inventory, extension
histogram, bytes, token counts, identifiers, comments, imports/includes, declarations, tests, error
handling constructs, and repository metadata. Add malformed encodings, empty files, symlinks,
duplicate blobs, generated files, and path-renamed copies to the fixture suite so normalization and
deduplication are tested rather than assumed.

Split examples by repository, file/blob, and time. No file, exact blob, near-duplicate, or prompt
template family may cross train, validation, calibration, and final holdout. The final holdout is a
whole repository-stratum-balanced set of files and prompts never used for model selection.

### 4. Expand the measurement ladder

Run these arms independently and publish them separately:

1. **Structural drift:** file count/bytes, language and extension mix, dependency/import graph,
   public declarations, test/error-handling density, AST/parse-feature distributions where a
   parser exists, and commit-normalized growth. Report absolute and normalized changes.
2. **Lexical drift:** token and identifier frequencies, TF-IDF/Jensen–Shannon divergence, new/gone
   vocabulary, n-gram change, and concept dictionaries defined before looking at results. Include
   stemming/case-sensitive sensitivity analyses so a tokenizer choice is not a finding.
3. **Repository-architecture drift:** graph edit distance or stable graph summaries for imports,
   packages, commands, and ownership boundaries; API/declaration matching across renamed paths;
   component churn and concentration. A missing parser is `na`, not zero.
4. **Behavioral convention drift:** frozen completion, patch, test-generation, error-handling,
   API-design, and architecture-explanation prompts. Score executable or parseable outputs on held-
   out fixtures, convention rubric items, exact/structural tests, abstention, and factual leakage
   separately. A prompt-only result is conditioning, not training.
5. **Capacity and representation controls:** base model, small model, larger comparator, random or
   shuffled-corpus control, and prompt-only Modelfile control. Use at least two embedding models or
   one embedding model plus lexical/structural metrics; do not call one cosine “architectural drift.”
6. **Genuine update arm:** LoRA/QLoRA on the same pinned base, tokenizer, examples, budget, and
   snapshot pairs when `torch`, `transformers`, `peft`, and accelerator prerequisites pass a
   preflight. Save adapter hash, config, training/eval logs, resource usage, before/after outputs,
   and checkpoint selection rule. If preflight fails, record the exact dependency/resource failure
   and leave this arm blocked.
7. **Temporal and cross-repo extension:** fit per-repository trajectories across three snapshots,
   then compare slopes and change vectors across strata. Hold one repository per stratum out of
   model/threshold development for a final generalization check.

### 5. Add controls and falsification tests

Every run includes:

- same snapshot versus same snapshot (repeatability/no-drift control);
- identical prompts with shuffled or unrelated corpus conditioning (prompt/model noise control);
- snapshot labels swapped (polarity control);
- byte-preserving path/file-order permutation (invariance control);
- synthetic known-change fixture with injected vocabulary, API, and graph changes (sensitivity);
- near-duplicate leakage challenge and an exact-copy retrieval challenge;
- base/no-conditioning and prompt-only controls;
- repeated seeds and repeated inference on a fixed output budget;
- negative prompts that should require abstention or say `unknown`.

At least one mutation must make each gate fail: remove snapshot pinning, leak a file into train,
replace a real adapter with a prompt, alter the tokenizer, and delete the live model/runtime step.
The test must detect each mutation. Passing a unit or smoke test alone does not establish that the
corpus was collected or that the evaluator is wired to real inference.

### 6. Define metrics, uncertainty, and interpretation

The primary estimands are (a) paired standardized change in structural/lexical features per
repository, (b) held-out convention recovery delta versus the same-snapshot control, and (c) output
divergence delta after subtracting repeatability noise. Use bootstrap confidence intervals clustered
by repository and file/blob as appropriate; report sample counts, missingness, effective sample
size, and seed variability. For multiple concepts/prompts, preregister the family and adjust or
label exploratory results.

Report at minimum: JSD/TF-IDF distance, vocabulary precision/recall for new/gone terms, graph
summary deltas, parse/test/error-handling rates, exact and structural test pass rates, abstention
precision/recall, calibration error/Brier score where confidence exists, output edit/AST distance,
embedding cosine with confidence interval, and wall/cold/warm latency, peak RAM/VRAM, disk, and
energy proxy. Define a repeatability floor from the same-snapshot control; a drift score below that
floor is `indistinguishable`, not evidence of no drift. Interpret lexical, conceptual, and
architectural claims separately and refuse a single pooled verdict when repository strata disagree.

### 7. Package artifacts and review

Each run produces a self-contained bundle:

```text
manifest.json                 # protocol/corpus/model/tool/runtime hashes
corpus.tsv + exclusions.tsv   # provenance, license, snapshot, status
fixtures/                     # hashes or permitted immutable archives
splits.json                   # source/file/time/group membership
raw/                           # prompts, outputs, errors, adapter metadata
metrics/                      # per-row, per-repo, per-stratum, pooled summaries
controls/                     # all negative and mutation-control results
costs.json                    # duration, CPU/RAM/VRAM, disk, network, energy proxy
report.md + report.json       # claims tied to artifact paths and verdicts
```

The report must include blocked arms, missing rows, exclusions, failed controls, and an exact
reproduction command using immutable IDs. A witness review reruns extraction, checks hashes and
split disjointness, inspects raw outputs, runs at least two controls and one mutation, and verifies
that the published score can be recomputed without trusting the prose.

## Cost envelope and scheduling

Use a staged budget. Corpus inventory, hashing, structural metrics, and most lexical metrics should
fit within 2 CPU-hours and 20 GB temporary storage for 30 repositories. Fixture extraction and
parsing should be budgeted at 8 CPU-hours/100 GB. Prompt-only inference should begin with 10
prompts × 3 snapshots × 24 repositories × 3 seeds × 3 model/control arms (about 6,480 calls), with
a pilot cap of 1,000 calls before expansion. Genuine LoRA/QLoRA is a separate GPU budget: pilot 2
repositories × 2 snapshots × 2 seeds, capped at 12 GPU-hours and 40 GB checkpoints; full corpus
training proceeds only if the pilot is stable and artifacts fit the storage budget. Record actual
costs, not estimates, and stop on a declared budget breach while retaining partial artifacts.

The execution order is: protocol/preflight → 6-repository pilot → independent pilot review →
24-repository corpus lock → structural/lexical pass → controls and split audit → prompt-only ladder
→ fine-tuning pilot or explicit block → full generative run → held-out evaluation → synthesis and
witness rerun. No live mesh lane, scheduler, model routing, or substrate wiring is part of this
plan.

## Acceptance criteria

The expansion is complete only when all applicable criteria have artifacts:

- at least 24 usable repositories from the declared strata, with immutable commits, license
  evidence, exclusion ledger, and at least two snapshots each;
- deterministic fixture rebuild matches manifest hashes and expected fixture tests, including
  malformed/duplicate/generated-file cases;
- train/validation/calibration/holdout groups are disjoint by repository, blob, near-duplicate,
  prompt family, and declared time boundary;
- same-snapshot repeatability and all preregistered negative controls pass their thresholds, while
  each mutation-control change is detected and goes red;
- every reported metric is recomputable from raw rows, carries n/missingness and clustered
  uncertainty, and is decomposed by repository and stratum;
- prompt-only, base, capacity, and shuffled/noise controls are present; genuine LoRA/QLoRA is either
  reproduced with adapter/config/resource artifacts or explicitly marked blocked with the failed
  preflight evidence;
- at least one locked whole-repository-per-stratum holdout is evaluated without threshold tuning;
- cost, latency, memory, storage, and network artifacts are complete for each model arm;
- an independent witness reproduces the manifest/hash/split checks, two controls, one mutation, and
  the headline tables;
- the final report never labels vocabulary or prompt-conditioning divergence as architectural drift
  without the structural/behavioral evidence needed for that claim.

If any gate fails, publish a failure report naming the failed arm, affected claims, artifact path,
and next experiment. A small, reproducible negative result is acceptable; an unmeasured arm is not.

## Existing-repository alignment

The work should extend `docs/tiny-fleet-drift-report.md`, `scripts/mesh-tiny-fleet`, and
`scripts/mesh-tiny-fleet-snapshot` only after this plan is accepted. It should preserve the weekly
structural series while separating it from expensive inference. The existing `docs/plans/
tinyfleet-drift-methodology.tsv` already calls for snapshot/corpus provenance, leakage controls,
structural baselines, generative tests, uncertainty, manifests, and a genuine fine-tuning adapter;
this plan supplies the missing scale, controls, fixtures, costs, and acceptance gates. Existing
repository test practice—fixture-driven tests, real-path gates where applicable, explicit `n/a`,
and mutation/failure evidence—must govern the eventual implementation.
