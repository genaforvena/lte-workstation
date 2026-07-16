# mesh-model-swap — close the loop from search → number → adoption

**Date:** 2026-07-15
**Operator ask (verbatim):** *"until this round of replacing old crapy llms we used with tiny
shiny new ones you should have reflex to measure top 3 you can find that match our needs (do
some search) and then you have numbers — you should make sure the shiny new models are used.
e.g. why we use huge piper still, all other our llms"*

## The gap this closes

Three of the four tools already exist. The chain is cut in two places.

| tool | role | state 2026-07-15 |
|---|---|---|
| `mesh-model-watch` | the CLOCK — searches HF, proposes drifted organs | wired daily 07:17 ✅ |
| `mesh-model-bench` | the RULER — wall-clock + WER vs a fixture | exists; **1 fixture, 6 rows, all STT, all hand-run** |
| `mesh-model-resolve` | the EYE — executes each consumer's own selector | exists ✅ |
| `mesh-model-swap` | the HAND — adopt the winner | **does not exist** |

**Cut 1 — watch proposes, nothing benches.** `~/.mesh/model-fixtures/` holds exactly one
fixture (`stt-ru-operator-0812`). TTS, vision and the LLM have **no fixture and therefore no
number**. Piper is not losing a comparison; it has never been in one. That is the whole answer
to *"why we use huge piper still"*: nothing can score it.

**Cut 2 — bench measures, nothing adopts.** GigaAM won STT on 2026-07-15 (0.312 vs
whisper-base's 0.812) and is live in the room ear **only**. `mesh-voice-rx` still loads
`ggml-base.bin`, and watch's own scan already flags that its ladder cannot see the better model
sitting on disk (`LADDER MISSES large-v3-turbo-q5_0 — exact-name match`). A win in the ledger
does not move a consumer.

## Decisions taken (operator, this session)

1. **Adoption = auto-swap behind a gate — for STT and vision ONLY.** **TTS benches, renders
   samples, and PROPOSES; the operator listens and picks.** (Revised mid-session against
   evidence — see "The TTS correction" below. The original decision was auto-swap everywhere.)
2. **The swap edits the ladders directly. No pin file.** Rejected by the operator, and he was
   right: a pin file is a SECOND statement about which model a consumer loads, and
   `mesh-model-resolve` exists *because the first such map lied*. Two sources drift. The ladder
   stays the only answer, so resolve can never disagree with it by construction.
3. **Scope: STT + TTS + vision, in full**, including fixing watch's candidate filter. Order is
   the implementer's choice.
4. **On-demand first.** Ships `# orphan-ok:`. It earns a `# reflex-cadence:` only after its
   gate has been SEEN going red on a real break — *a gate you have not seen fail is not a gate*.
5. **TTS ties go to the incumbent** (implementer's call, see "What this cannot know").

## The swap surface

All three consumers' selection points are **one line each**. This is what makes direct ladder
editing safe: the reflex never parses arbitrary code.

| consumer | organ | line | shape |
|---|---|---|---|
| `mesh-voice-rx:55` | STT | `for name in ("ggml-large-v3-turbo.bin", …)` | ordered tuple |
| `mesh-face-recognize:55` | vision | `LOCAL_MODEL = os.environ.get(…, "moondream")` | scalar default |

TTS has **no swap surface** — see "The TTS correction". `mesh-note3-say:48`'s glob ladder was
named as the TTS target in the first draft of this spec and is **wrong**: it is dead code on
this node, outranked by an env pin.

Each gains a marker comment in the established `# reflex-cadence:` idiom:

```python
# model-ladder: stt/voice-rx — mesh-model-swap rewrites the NEXT line only
for name in ("ggml-large-v3-turbo.bin", "ggml-large-v3.bin", "ggml-medium.bin", "ggml-base.bin"):
```

`mesh-model-swap` replaces **exactly the marked line**, nothing else. A marker with zero matches,
or more than one, is UNKNOWN → no swap. (UNKNOWN, never a default — same rule as watch's gate 1.)

## The gate

Rollback is scheduled **first**, via `mesh-dms`, and cancelled last. Order matters.

1. `py_compile` / `bash -n` — the file still parses.
2. `mesh-model-resolve` reports the consumer now loads the winner. **This is the independent
   oracle**: it executes *their* selector, so it cannot agree with us by construction. A
   re-derivation here would just be the second map again.
3. The organ's own `--test` does a **real read** and passes.
4. Only then cancel the rollback.

Any failure restores the backed-up line. **The failure mode is "piper stays", never "the room
goes deaf."**

## The oracles

**STT** — WER vs `stt-ru-operator-0812`. Exists. Reuses `mesh-model-bench`'s two-axis rule
(speed alone selects the fastest wrong answer: whisper-tiny does this fixture in 0.8s and
returns a *different sentence*).

**TTS (new)** — round-trip: authored ru sentence → render → GigaAM transcribes → WER vs the
input text, plus render wall-clock at a real duration.

- **Its reference is genuinely independent** — we wrote the sentence. This is *stronger* than
  the STT fixture, whose `provenance.txt` honestly admits `truth.txt` is human-mediated model
  output (the room ear's own large-turbo transcript, hand-cleaned).
- **But its absolute value is not interpretable.** Round-trip WER charges the TTS candidate for
  GigaAM's own STT error (measured: 0.312 on real speech). That error is **common-mode** — every
  TTS candidate goes through the same transcriber — so it **cancels for ranking and does not
  cancel for absolute value**. The ledger row is comparative-only; never quote a TTS WER as a
  quality figure.
- Fixture text must avoid transliterated English. The existing STT fixture proves why: no two
  models render «текст-ту-спич» alike, so such text measures transliteration luck, not quality.

**Vision (new)** — N frames with known labels, scored through `mesh-face-recognize`'s own
`classify_safe()` path, so the number measures the organ rather than a re-implementation.
Accuracy = fraction correctly labelled onto the existing label set.

## Watch's candidate filter (the "match our needs" gap)

Watch currently ranks candidates by **downloads + age + VRAM fit**, with no task filter. Its
live vision top-3 is `baidu/Unlimited-OCR`, `google/diffusiongemma-26B-A4B-it`,
`Qwen/Qwen3.6-27B-FP8` — an OCR model and a diffusion model, as candidates to replace moondream
at face/scene labelling. Auto-benching that list burns GPU watching nonsense lose.

The operator's phrase was *"top 3 that **match our needs**"*. That filter does not exist today.
Fix: rank on HF `pipeline_tag` / task tags, not popularity. This improves STT and TTS candidates
too — it is not vision-specific.

## Privacy constraint (non-negotiable)

The vision fixture is **home frames**; the STT fixture is the **operator's own voice**. Both live
in `~/.mesh/model-fixtures/` (gitignored, node-local) and **never** enter the genome. The genome
is committed and pushed; a fixture is not.

## The TTS correction (found during implementation, 2026-07-15)

The first draft of this spec had TTS auto-swapping on round-trip WER, with `mesh-note3-say:48`'s
glob ladder as the edit target. Both halves were wrong, and `mesh-model-resolve` is what caught
it — the eye earning its keep before the hand was built.

**(a) The ladder is not the decision surface.** Resolve reports the live voice as
`ru_RU-irina-medium.onnx`, selected by an **env pin in `~/.mesh/nodes`** that outranks the glob
ladder. Rewriting that ladder changes nothing: the gate would revert every TTS swap forever, and
the "swap surface" was dead code. This is the *"a selector's answer is code AND env"* trap, live,
in the organ the reflex was about to automate.

**(b) The voice decision was already made, by the operator's ear.** The pin's own comment:

> Room voice = IRINA (operator 2026-07-14, live A/B in the room). He first said "главное не
> женщину", then reversed two minutes later after hearing ruslan: "давай попробуем Ирину, Ирина
> никогда нас не подводила".

He A/B'd it live and **reversed his own first instruction after hearing it**. An auto-swap on
round-trip WER would overrule a human aesthetic judgement with a metric that cannot hear.

**(c) Engine and voice are different questions, and the operator asked about the engine.** *"Why
we use huge piper still"* is about **piper the runtime** (2023 prebuilt; ru voices from
`rhasspy/piper-voices`, 37mo). The ladder is about *which voice*. And note for the record: **piper
is not huge** — 63MB per voice, a small ONNX runtime. Confirmed with the operator that the gripe
is **age, not size or naturalness**.

**The tie that settles it:** swapping the TTS *engine* also changes the *voice* (Kokoro/XTTS ship
their own), so every TTS swap is something the operator hears. WER can never be its whole gate.

**Resulting design:** TTS benches (round-trip WER + render wall-clock), searches for
2025/2026-era candidates, **renders candidate samples to the Note3**, and posts a proposal. The
operator listens and picks. STT and vision keep the auto-swap: correctness is their whole story
and there is nothing to hear.

## The TTS oracle mostly does not work (measured 2026-07-15)

Built the fixture (`tts-ru-authored-01`), tested the oracle by hand before tooling it, and it
largely failed. Full numbers in that fixture's `provenance.txt`.

**Through GigaAM it is a CONSTANT.** irina/ruslan/dmitri all score **0.000** — identical,
perfect. TTS output is clean, noiseless, perfectly articulated speech: the easiest possible
input for a good STT. A ranking keyed on this can never fire. Same family as `tone`, whose
median is its max, and `act > 0.55` which can never fire.

**Through whisper-tiny it discriminates — but it is a RANDOM VARIABLE.** Piper's render is
**non-deterministic** (3 identical invocations → 3 different md5s; VITS samples). whisper-tiny
is perfectly deterministic (0.207 three times on a fixed wav), so all variance is the
synthesiser's. The first pass read 0.103/0.172/0.207 and looked like a clean ranking; the
**within-voice** spread (0.207 vs 0.345, nominally identical renders) is **larger than that
whole between-voice gap**. n=1 is meaningless. At n=6: irina 0.144±0.034, ruslan 0.195±0.068,
dmitri 0.368±0.042 — only dmitri-vs-irina is robustly separated.

**And it is confounded by speaking rate.** irina renders this text in 13.6s, dmitri in 9.4s;
slower is easier to read. Control (vary only rate, n=6): dmitri 9.4s→0.368, 12.0s→**0.270**,
vs irina 13.6s→0.144. Rate is a real driver worth ~27% of the gap — but irina at 13.6s still
beats dmitri at 12.0s, so a residual voice effect survives. Durations were not matched exactly,
so neither "it's pure rate" nor "rate is controlled" is claimable.

**Consequence:** the spec's TTS design is not viable as written. Round-trip WER cannot rank
voices or engines on quality. It is honestly good for: render wall-clock, speaking rate, and a
**floor gate** (a candidate NOT scoring ~0.000 through gigaam is broken/mispronouncing/silent —
a genuine regression detector). Quality stays the ear's.

This is the answer to *"why we use huge piper still"*: **no mechanical axis can currently prove a
replacement is better.** The only defensible axes are age, speed, and the operator's ear.

## What this cannot know

**Round-trip WER cannot hear.** It measures intelligibility. A robotic voice that is perfectly
intelligible beats a warm one that is slightly less so. If a candidate ties piper on WER and wins
on speed, the numbers will propose a swap on an axis the operator would not have chosen.

**Mitigation:** TTS does not auto-swap at all. The numbers shortlist; the operator's ear decides.
This is not a hedge — it is the only correct answer once you notice the operator already ran a
live A/B and reversed himself on what he heard. A tie plus "faster" is not a reason to change a
voice he chose.

**`mesh-face-recognize` reads `MESH_FACE_LOCAL_MODEL` from env.** A swap can write the line and
still lose to an env var in `~/.mesh/nodes` — the *"a selector's answer is code AND env"* trap
that already bit note3-say's voice pin. Resolve running in the consumer's real env is what
catches it, but vision's swap is genuinely less trustworthy than STT's or TTS's, and the ledger
should say so.

## Build order

Each step is independently useful; each feeds the next. Reordered after the TTS correction: STT
leads, because it is now the first organ that actually auto-swaps.

1. **`mesh-model-swap` + the gate, driven on STT.** Fixture exists, winner already known
   (`voice-rx` loads `ggml-base` @ 0.812 WER while GigaAM scores 0.312), swap is small: stop
   `_best_model()` preferring a model that loses its own bench. Then **break it deliberately** —
   aim it at a nonexistent model, watch resolve refuse and the line get restored.
2. **TTS fixture + piper's number + a candidate search.** Round-trip oracle, 2025/2026-era
   candidates, samples rendered to the Note3, proposal posted. No swap.
3. **Task-fit filter in `mesh-model-watch`.** Makes "top 3 that match our needs" a true sentence.
4. **Vision fixture + oracle.** Last: depends on (3) for candidates worth spending GPU on.

## Testing

Per house rule, every `--test` must assert the REAL path, never a stub, and must be watched
FAILING before it counts:

- `mesh-model-bench --test`: a real render + real transcribe on the TTS fixture yields a parseable
  WER; a missing organ exits 2 (honest n/a), never a fake green.
- `mesh-model-swap --test`: drives a real rewrite against a **temp copy** of a real consumer,
  asserts the line moved AND that a bad swap is REVERTED. Must never write the real ledger or a
  real consumer (the `mesh-guardian` trap: a dry-run that writes the live log forges the evidence
  it exists to check). Its own log, its own fixture copy.
- The swap gate is verified by mutation: point it at a nonexistent model, confirm red + restore.
