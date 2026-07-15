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

1. **Adoption = auto-swap behind a gate.** Not a proposed `[task]`. (Operator choice over two
   alternatives.)
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
| `mesh-note3-say:48` | TTS | `for v in "$d"/ru_RU-ruslan-*.onnx …` | ordered glob list |
| `mesh-face-recognize:55` | vision | `LOCAL_MODEL = os.environ.get(…, "moondream")` | scalar default |

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

## What this cannot know

**Round-trip WER cannot hear.** It measures intelligibility. A robotic voice that is perfectly
intelligible beats a warm one that is slightly less so. If a candidate ties piper on WER and wins
on speed, the numbers will propose a swap on an axis the operator would not have chosen.

**Mitigation:** TTS swaps require a **decisive win on both axes; a WER tie goes to the
incumbent.** A tie plus "faster" is not a reason to change a voice the operator is used to. This
keeps the blind spot harmless rather than pretending it is closed.

**`mesh-face-recognize` reads `MESH_FACE_LOCAL_MODEL` from env.** A swap can write the line and
still lose to an env var in `~/.mesh/nodes` — the *"a selector's answer is code AND env"* trap
that already bit note3-say's voice pin. Resolve running in the consumer's real env is what
catches it, but vision's swap is genuinely less trustworthy than STT's or TTS's, and the ledger
should say so.

## Build order

Each step is independently useful; each feeds the next.

1. **TTS fixture + piper's first number.** The operator's named example. Proves the round-trip
   oracle on piper before it is trusted anywhere near the room's ear.
2. **`mesh-model-swap` + the gate, driven on STT.** Fixture exists, winner already known, swap is
   small (stop `_best_model()` preferring a model that loses its own bench). Then **break it
   deliberately** — aim it at a nonexistent model, watch resolve refuse and the line get restored.
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
