# Crypthauntology for Kids expansion plan — 2026-09-07

**Status:** plan only; no model campaign or child-facing deployment is authorized by this file.

## Outcome and boundaries

Expand `~/src/hyperhauntology_for_kids` from a sound three-arm probe into a small, reproducible
curriculum and evaluation suite for conversation-state persistence. Preserve the narrow question:
after a harmless induced state, does a later unrelated probe recover, relative to clean and
context-matched-noise controls? Do not frame it as a jailbreak kit, a general safety benchmark, or
an instrument to elicit harmful content. All examples must be fictional, reversible, and safe to
publish; children are never research subjects or direct testers.

## Multi-step work packages

### 1. Freeze the research contract

Record the estimands, H2 refusal persistence as primary, H3 false-fact persistence as secondary,
and H4 provenance confusion as exploratory. Pin model/provider, prompt versions, temperature,
turns, detector/schema versions, power target, arm order/randomization, and stopping rules. Keep
the current establishment, `None`/coverage, `MUTE`, `TRUNCATED`, and power gates.

**Artifact:** versioned protocol and design manifest with an explicit child-safety boundary.

### 2. Build age-banded, safe lesson modules

Create modules for ages 8–10, 11–13, and 14–17, with a teacher/guardian track rather than direct
unsupervised use. Each module explains context, controls, uncertainty, and one harmless canary in
plain language. Add lessons on “a model can be wrong,” “missing data is not zero,” provenance
(what instructions are), and how to stop/reset a conversation. Avoid real personal data,
self-harm/sexual/violent examples, evasion instructions, credential requests, or claims that a
model has feelings or secret access.

**Artifacts:** lesson YAML/Markdown, glossary, facilitator guide, answer key, and safety review
checklist. Every activity has a no-model paper/offline variant.

### 3. Add a content and safety gate

Run deterministic linting for forbidden examples, personal-data-shaped strings, unsafe external
links, manipulative framing, age-band mismatch, and unsupported scientific claims. Have two
independent adult reviewers inspect every new lesson; record disagreements and resolution. Test
that refusal and uncertainty language is understandable and that the material never rewards
successful boundary crossing.

**Artifacts:** lint report, reviewer sign-offs, redacted fixture corpus, and a mutation report
showing that unsafe fixtures make the gate fail.

### 4. Expand the probe matrix without broadening the claim

For each state, add 3–5 pre-registered harmless canaries covering arithmetic, geography, identity,
uncertainty, and provenance. Balance positive/negative wording, paraphrases, languages, and
turn-distance. Randomize arm order or justify fixed order with a carry-over check. Add same-context
repeatability, shuffled-noise, snapshot-hash, prompt-order, and abstention controls. Keep every
model/provider pair separate; never pool a child-facing lesson score into a scientific verdict.

**Artifacts:** canary registry with graders and expected labels, prompt-family split manifest,
control matrix, and deterministic offline fixtures.

### 5. Pilot the instrument offline first

Use recorded tapes and synthetic responses to exercise replay, grading, coverage, power, and
redaction. Then run a small adult-reviewed pilot on one local and one remote model, sequentially,
with no child involvement. Require the state-establishment gate before scoring later turns. Keep
partial/provider-failed runs on tape and report them as blocked or inconclusive.

**Artifacts:** pilot manifests, replay-equals-live transcript, per-family denominators/MDE,
failure-state table, and cost/latency record.

### 6. Run the powered adult-only study

Collect the declared 30 complete repetitions per model/provider pair, or publish the exact
operational failure. Use treatment, clean control, and context-matched noise in every repetition.
Reserve a whole model/provider or prompt-family holdout for the final check. Freeze graders before
opening the holdout. Report nulls only when the implemented power test supports them; otherwise say
`INCONCLUSIVE`, `BLIND`, `UNDERPOWERED`, or `NOT-ESTABLISHED`.

**Artifacts:** append-only JSONL tapes, hashes, replay reports, holdout manifest, raw counts,
coverage, MDE, verdicts, and blocked-arm ledger.

### 7. Publish the educational package and review it

Separate the scientific report from the kid-facing materials. The public bundle contains safe
fixtures, protocol, manifests, replay commands, limitations, and facilitator guidance; private
provider data, credentials, raw personal text, and unreviewed traces stay out. Ask an independent
witness to rebuild the tape summary, run two controls, and trigger one safety mutation. Retire a
lesson if review finds an unsafe or misleading interpretation.

**Artifacts:** reproducible release bundle, teacher guide, safety/version changelog, witness report,
and exact next-action handoff.

## Acceptance criteria

- Every lesson is age-banded, adult-mediated, harmless, and has an offline alternative.
- Safety lint and two-reviewer sign-off pass; a deliberately unsafe fixture turns the gate red.
- Every scientific number has treatment/clean/noise arms, coverage, denominator, power/MDE,
  provenance, and replayable raw rows.
- No blind, truncated, mute, unestablished, or provider-failed run becomes a scientific null.
- Holdout prompts/models remain untouched until the protocol and graders are frozen.
- A clean checkout can run offline replay and regenerate the public report without credentials,
  personal data, or unsafe examples.
- The final report keeps the narrow persistence claim and labels all exploratory outcomes.

## Risks and immediate next action

Main risks are pedagogy turning a narrow method into a sensational claim, unsafe examples leaking
into fixtures, child-facing use being mistaken for research participation, and low coverage being
read as model recovery. Mitigate them with the safety gate, adult-only pilots, explicit verdicts,
and the paper/offline track.

**Next action:** create the protocol/design manifest and lesson schema, then run the offline
lint/replay gate before any live model call.
