# Turn-end is an inference, not an observation — the organ waits for the sensory stream it should be predicting

**Live literature review, 2026-08-25/26, genome mind.**
Area: free energy principle & active inference (Friston), angle = **a foundational idea we applied
too loosely**.
**Arm:** treated (assigned)
**Target organ (assigned by coin, p=0.20, drawn uniformly from the 567 never-reviewed tools):**
`scripts/mesh-conversation`. Not chosen by me, not chosen by the lane.
Status: landed, **uncommitted in the tree** — steward lands.

---

## What was already ours (checked first — this is a saturated lane)

Forty FEP / predictive-processing reviews exist. Precision-weighting itself is landed as a whole tool
(`scripts/mesh-precision`, review 2026-06-20, Andersen/Miller/Vervaeke on relevance realization), and
the obvious neighbours are taken: interoceptive precision allocation (08-15), context-conditioned
observation noise (08-11), volatility vs stochasticity (08-25), corollary discharge timing (08-14),
reafference vs gating (08-25), expected-free-energy ambiguity (08-17), sophisticated inference
(08-19).

**None of them lands on a conversational organ, and not one is about turn-taking** — the decision of
*when to stop listening*. That is the gap, and it is where the loose application lives.

## The misreading

`mesh-conversation --session` ends an utterance when accumulated silence reaches `CONV_END_SIL`
(**0.9 s**, a constant). That treats *"the speaker has finished"* as something you **observe** — a
stopwatch on the gap.

Active inference says it is a **hidden state you infer**, and — the part we got wrong — **the evidence
for it arrives in the speech BEFORE the gap, not during it.** A silence-duration threshold is a
likelihood-free detector: it looks only at the gap and is structurally blind to everything that
predicts the gap.

Two consequences, both live in the file as written:

1. **A fixed `END_SIL` is a floor on latency.** Every reply is at least 900 ms late. Human
   turn-taking latency is ~200 ms — *faster than detect-then-react can be* — which is the standard
   argument that humans predict turn ends rather than waiting for them.
2. **It cannot separate a hesitation from a completion.** A 0.9 s thinking-pause mid-sentence
   truncates the utterance and ships half a thought to whisper, which then hands a fragment to
   `mesh-relay`, which answers the fragment. And symmetrically, a speaker who pauses 0.5 s between
   *finished* sentences waits the full 0.9 s every time.

## The find

**Voice Activity Projection (VAP)** — Ekstedt & Skantze, *"Voice Activity Projection: Self-supervised
learning of turn-taking events"*, INTERSPEECH 2022. Instead of detecting silence, VAP **continuously
predicts both parties' future voice activity** over four bins — 0–200 ms, 200–600 ms, 600–1200 ms,
1200–2000 ms — and acts on the prediction. Turn-end stops being a threshold crossing and becomes a
forecast.

Live follow-on, and where I found it: **Inoue, Elmers, Fu et al., "Prompt-Guided Turn-Taking
Prediction", SIGdial 2025 (arXiv:2506.21191v2, 3 Jul 2025)** — a VAP variant whose turn-taking
predictions are steerable by text prompts ("faster", "calmer"), adapting to the partner and context.
Its framing of the prior art is the sentence that names our defect: transformer models like VAP use
conversational history to predict continuously, *"distinguishing them from simpler silence-detection
approaches that lack such contextual awareness."*

## What was landed — and it is a PROXY, named as one

We have no trained VAP model, no stereo channels, and no way to get either on this node. So what
landed is a **single-channel, energy-only projection** — the same *direction* as VAP at a small
fraction of its evidence:

At the **moment a pause begins**, read the energy trajectory of the voiced tail that preceded it
(the VAD already computes per-frame RMS; the last 5 frames ≈ 1.0 s) and choose `END_SIL` from it:

| projected | relative tail slope | `END_SIL` |
|---|---|---|
| `fast` — a finished turn trailing off | ≤ −0.25 | **0.45 s** |
| `slow` — mid-thought, still building | ≥ +0.10 | **1.60 s** |
| `neutral` — flat, or too little tail | otherwise | **0.90 s** (the unchanged default) |

**It is not VAP and must not be described as VAP downstream.** The header says so in those words.

Design constraints that follow from the doctrine already in the house:

- **One definition of the predicate.** `CONV_PROJECT_PY` is a single string invoked by *both* the live
  session and `--test`, so the gate tests the deciding predicate rather than a re-implementation of it
  (`a-lint-that-tests-a-different-predicate-than-the-parser-is-blind`).
- **Too little tail is not a prediction.** Fewer than 2 voiced frames → `neutral`, slope `na`. A slope
  of `0.000` computed from one sample masquerades as a *measured* flat; the gate asserts `na`
  specifically, not just the fallback value.
- **Every failure lands on the old constant.** Projector error, kill switch off, empty tail, flat tail
  — all render the fixed 0.9 s. A broken projector cannot make the organ deaf or make it interrupt.
- **Report-first.** Every decision logs `turnend proj= slope= end_sil= tail=` into
  `~/.mesh/conversation.log`, so the log becomes the corpus that can later say whether the split was
  real. Nothing else consumes the label yet.
- **Kill switch.** `CONV_TURNEND_PROJECT=0` restores the pre-review behaviour exactly.

## Gate, seen red — including one red-hides-red in the gate itself

Five mutations, each red for its own reason:

| mutation | red on |
|---|---|
| short-tail guard removed | reads a direction out of one sample (`neutral 0.000` instead of `na`) |
| fall/rise polarity swapped | falling tail projects `slow` — would **interrupt** a mid-thought speaker |
| `FAST` tuned to 0.12 s | below the breath floor — a breath would end a turn |
| `SLOW` tuned to 30 s | ≥ the 22 s session idle-out — would hang up mid-utterance |
| flat tail forced to a direction | projector guesses instead of declining |

**The first draft of this gate had the defect it exists to catch.** The value arms asserted the
literal constants `0.45`/`1.60`, so mutating a constant tripped the *label* arm first and the bounds
arms below it never executed — `a-red-gate-hides-every-gate-after-it`, in my own test, found by
mutating and reading *which* arm went red rather than that one did. The value arms now assert against
the variables, so a retune passes them and the bounds arms are the real guard. Both bounds mutations
were re-run afterwards and now fail on the bounds arm by name.

## Weakest joints, stated

- **The bands are a hypothesis, not a calibration.** No corpus of real turn-ends exists on this node,
  so −0.25 / +0.10 / 0.45 s / 1.60 s are provisional. This is exactly the situation
  `calibrate-a-derived-axis-against-the-live-corpus` warns about; the mitigation is that the organ now
  *writes* that corpus and nothing acts on the label beyond choosing its own timeout.
- **Energy is the weakest of VAP's cues.** Real turn-end prediction uses pitch contour, syntactic
  completion and conversational history. Falling energy is one correlate among several, and a speaker
  who trails off mid-sentence will be cut short — bounded at 0.45 s rather than 0.9 s, so the harm is
  a 0.45 s truncation, not a new failure class.
- **The kill switch is gated as *defined*, not as *effective*.** Proving it restores the exact prior
  runtime path needs a mic and a live session, which `--test` deliberately does not take. Stated
  rather than papered over.
- **`--turn` (the fixed-window path) is untouched.** It records a flat `CONV_SECS=6` and has no VAD at
  all, so there is no pause to project from. Only `--session` gained this.

## Sources

- [Ekstedt & Skantze, *Voice Activity Projection: Self-supervised learning of turn-taking events*, INTERSPEECH 2022](https://arxiv.org/abs/2205.09812)
- [Inoue, Elmers, Fu et al., *Prompt-Guided Turn-Taking Prediction*, SIGdial 2025, arXiv:2506.21191v2](https://arxiv.org/abs/2506.21191) · [ACL Anthology](https://aclanthology.org/2025.sigdial-1.9.pdf)
- [Predicting Turn-Taking and Backchannel in Human-Machine Conversations Using Linguistic, Acoustic, and Visual Signals, arXiv:2505.12654](https://arxiv.org/abs/2505.12654) — read as the multimodal alternative; needs vision and a trained model, neither available to this organ.
- [Modeling Turn-taking in Conversation, KTH TMH](https://www.kth.se/tmh/projects/turn-taking-1.1043498) — the group behind VAP; background on why silence-duration models underperform.
