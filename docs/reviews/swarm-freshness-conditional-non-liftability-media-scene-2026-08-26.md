# Live literature review — swarm intelligence & stigmergy, from the CRITIQUE angle

**Date:** 2026-08-26 · **Lane:** genome · **Organs:** `scripts/mesh-media-scene` (writer),
`scripts/mesh-sensorium` (reader)

## Where the corpus already is

`docs/reviews/` carries **18** swarm/stigmergy files. The standard mechanisms and most of the
standard critiques are embodied: the ant-mill positive-feedback trap, density-adaptive evaporation,
pheromone entropy / foraging evenness, no-entry repellent, cross-inhibition, tunable quorum
speed-accuracy, response-threshold division of labour, sematectonic vs sign-based stigmergy,
inverse stigmergy, the fundamental diagram, differential-latency quality-blind aggregation,
directed-information lead/lag, trace-blind minority plasticity, structural bias in an uninformative
picker, asocial bias / zealot corroboration, tandem-run teaching vs transport, collective gradient
margin, interaction-rate closed-loop drive.

Every one of those is about **what the trace says** or **how fast it decays**. None is about
**what a coarsened trace is allowed to drop** — which is the axis this paper opens.

## The concept we did not embody

Fernando Paredes García, **"Axiomatic shared-medium coordination for stigmergic systems"**,
[arXiv:2608.02619](https://arxiv.org/abs/2608.02619) \[cs.DC], CC BY 4.0, submitted 12 Jun 2026.
Full text read at `https://arxiv.org/html/2608.02619v1` (108k chars); §§7.8–7.11, 8.4A, 8.5.

The paper builds a **medium-agnostic comparison layer** for stigmergic systems whose comparison
object is the *abstract enabled-response signature* — not the trace, not the medium, but the set of
(activation, response) pairs the medium elicits from the agents reading it. Verbatim from the
abstract:

> "For metadata refinements, we prove that a coarse quotient is response-adequate exactly when each
> quotient fiber is response-aligned. When that fails, there is a canonical coarsest response-adequate
> repair, and every response-adequate repair must retain at least the corresponding fiberwise number
> of response classes. On the dynamic side, quotient-compatible matched writes preserve one-step
> behavior, **freshness-conditional actions yield a one-step non-liftability obstruction**, and the
> matched one-step result lifts to finite serial traces."

Three results, and the third is the one with teeth for us:

**(a) Thm 7.8 — the criterion.** A coarsening of the medium is safe *exactly* when every full state
that collapses onto one summary elicits the SAME activation and the SAME response from every agent.
The test is therefore not "is information lost?" — all summaries lose information, that is what they
are for — but "is *response-splitting* information lost?" It is a property of the summary **jointly
with the set of readers**, never of the summary alone.

**(b) Thm 7.9A + §8.4A — the obstruction, and it is one step deep.** If any reader's action is
guarded on the **freshness** of a mark (`act iff the mark is newer than τ`), then two states with
identical visible content and different mark ages sit in one fiber and produce *different projected
successors*. §8.4A works the witness explicitly and concludes:

> "The quotient can still represent unconditional writes, but freshness-conditional writes already
> fail at the level of one-step matched evolution."

Not eventually, not under load, not at scale. **One step.** And it compounds: "multi-threshold or
multi-key freshness guards create multiple response-distinguishing classes over one coarse state."

**(c) Thm 7.10 / 7.10A + §8.5 — the repair, with a forced minimum size.** When the criterion fails,
the canonical coarsest repair pairs the coarse state with its response-signature class,
`C = {((s,φ), σ)}`, and **every** adequate repair must satisfy
`|p⁻¹(s,φ)| ≥ |F_π(s,φ) ∪ {Σ(s,φ)}| ≥ r` — at least as many classes per coarse state as the fiber
carries distinct freshness-sensitive responses. §8.5's distinguished agent commits to whichever of
`r` keys is *uniquely freshest*, and when no key is uniquely freshest or a timestamp is missing it
returns `⊥`, which the paper is careful to type: `(P,R) = (1,⊥)` is **"agent j is active but
abstains"** and is a *different* signature from `(0,⊥)` = "agent j is disabled".

That last distinction is our own `na`-vs-absent doctrine, arrived at axiomatically, and it is the
member most of our verdict alphabets are missing.

**Why this is a critique of the area and not a technique from it.** The stigmergy literature's
standing promise is that indirect coordination through a shared medium is robust *because* agents
need only a local, summarised view. This paper is the formal statement of the price: the summary is
only legitimate up to the response signature, and the single most common thing a summary drops —
**when the mark was made** — is exactly the thing that cannot be dropped as soon as one reader is
impatient. It is a negative result aimed at the field's own comfort.

**Do we embody it?** No — and the shape of the gap is instructive. `memory/` carries at least eight
*instances* of this obstruction, each discovered by pain, one organ at a time:
`each-reader-invents-its-own-staleness-bound`, `mtime-proves-a-touch-not-a-sign-relation`,
`a-collapsed-reason-makes-blind-and-quiet-identical`,
`a-parser-that-knows-one-label-renders-every-other-as-absence`,
`a-fallback-tier-that-renders-a-different-word-not-unknown`,
`a-live-average-and-a-boot-time-fossil-print-identically`,
`a-sidecar-cannot-narrow-a-bit-its-readers-never-open`,
`a-new-verdict-word-must-be-in-the-consumers-alphabet`. What we have never had is the **criterion**
(response-alignment, not information loss) or the **arithmetic** (`≥ r`, so "is this vocabulary too
coarse?" has a computable answer instead of an anecdote).

## The live instance, found by applying the criterion

`mesh-media-scene` fuses four axes into one household scene word. Two are **live probes** (`local`
via `wpctl`, `imac` via its organ) and two are **tape reads** (`tv` from `presence.log`, `mic` from
`ambient-db-tape.tsv`), each accepted anywhere inside a 600s freshness window. Its two attribution
scenes are **cross-axis inferences**: `TV-LIKELY` uses the tv axis to explain the mic axis, and
`LIVE-SOUND` — the "there are HUMANS in the room" claim — uses tv=ABSENT plus two silent media axes
to do the same.

Before this change, `axis_tv` and `axis_mic` each **computed the age and threw it away**
(`mesh-media-scene:121-122`, `:140` pre-fix), so the emitted word was the whole projection. The
board therefore rendered a TV beacon seen 3 seconds ago and one seen 9 minutes ago **byte-identically**
as `tv=IN-RANGE`, and the room's loudness was attributed to it either way. That is 7.9A's fiber,
with `r = 2` responses over one coarse state.

The reader half is worse, and it is the piece the criterion surfaced that no organ-local review
would have: `mesh-sensorium:1163` marks this state `media=$(mark ... 600)`, and `mark()` ages from
**file mtime** — while `mesh-media-scene` calls `mesh-state-touch` on *every* tick by the
liveness-touch convention (mtime = ran-live, by design). So sensorium's freshness guard was reading
the writer's heartbeat and reporting `(fresh)` for a reading whose evidence was up to ten minutes
old. Two different quantities under one clock: `mtime-proves-a-touch-not-a-sign-relation`, one ring
out — it binds *derived readings*, not just sign relations.

Live artifact, this node, first run after the fix (unprompted, not a fixture):

```
[media-scene] scene=TV-LIKELY src=- local=SILENT imac=NONE tv=IN-RANGE mic=LOUD degraded=- \
              attrib=skewed skew=351 ages=local:0,imac:0,tv:394,mic:43
```

Sound heard 43s ago, attributed to a TV beacon last seen **394s ago**. The deployed copy renders the
same instant as `... tv=IN-RANGE mic=LOUD degraded=-` and stops.

## What was built

**Writer — `scripts/mesh-media-scene`.** The repair is Thm 7.10's canonical coarsest one: pair the
coarse state with its response-signature class, rather than enlarge the scene alphabet.

- Every axis now emits `WORD AGE`. `AGE` is the age of the **evidence the word rests on** — 0 for a
  live probe, and for `IN-RANGE` the age of the *freshest line that actually matched the TV regex*,
  not of whatever landed in the tape afterwards.
- `fuse()` takes four optional trailing ages and returns a 4th and 5th field, `attrib` and `skew`:
  `direct` (MEDIA — the source names itself, no inference was made) · `fresh` / `skewed` (cross-axis
  attribution, corroborator within / beyond `SKEW_S` of the trigger) · `na` (**active but abstains** —
  the question arose and an age was unknown) · `-` (the question does not arise for this scene).
  `na` and `-` are deliberately distinct renderings; collapsing them rebuilds the fiber.
- `SKEW_S` defaults to `WIN_S/2`, i.e. **half the organ's own already-declared freshness window** —
  not a new invented constant.
- **`attrib=` never rewrites the scene word.** A consumer's alphabet does not grow when ours does
  (`a-new-verdict-word-must-be-in-the-consumers-alphabet`), so the class rides beside the verdict and
  every existing consumer keeps working unchanged.
- STATE gained a **line 2** (`attrib= skew= evidence-age= ages=`); **line 1 stays the bare scene word
  forever**, because `mesh-sensorium` reads it with `head -1` and there is no reader sweep here.
  Line 2 is written **unconditionally on every tick** while line 1 stays change-gated — the scene is a
  debounced verdict, the evidence age is a live quantity, and change-gating it would hand a
  freshness-guarded reader an age frozen at the last flip: the same collapse, rebuilt one layer out.

**Reader — `scripts/mesh-sensorium`.** `mark()` gained an optional 4th argument: an explicit age that
overrides the mtime-derived one, plus an `evage()` helper that reads `evidence-age=` off line 2. The
`media=` call site passes it and appends `[skewed-attrib]` when the class says so. A producer that
publishes no line 2 falls back to mtime, byte-identically to before. Proven on one file at one
instant: **mtime says `(fresh)`, the evidence says `(recent)`.** Without a reader this would be a
label with no actuator — `a-gates-verdict-with-no-reader`.

## Gates (seen red, then green)

`mesh-media-scene --test`: 13 fixtures (was 8) — the eight originals now carry ages, plus **F1–F6**
driving all four classes, the `<=` boundary, and the `na`≠`-` non-collapse — plus a new end-to-end
**STATE reader-contract** block (line 1 stays the bare word · line 2 moves `fresh→skewed` with **no
scene flip**, proving it is not change-gated · `IN-RANGE` is aged by the matching line). Green,
including the live-read leg and the sandbox-honesty gate.

`mesh-sensorium --test`: a new **ROOM media=** block — 537s evidence in a just-written file renders
`(recent) [skewed-attrib]`, 1200s renders `(STALE)` though the reflex just ran, a timely attribution
renders `(fresh)` with no clause, and a line-2-less producer falls back to mtime. Whole suite green.

**Twelve mutants driven red from a scratch copy** (`/tmp/msmut`, `/tmp/snmut`; the harness aborts
loudly when a mutation site is not found — `a-failed-fixture-mutation-looks-like-a-passing-gate`):
`na-clears` · `na-collapse` · `skew-blind` · `boundary` (`-le`→`-lt`) · `media-not-direct` ·
`awk-v-regex` · `line2-change-gated` · `payload-on-line1` · `ages-dropped` (the original defect
restored) · `wrong-evidence-aged` · `mark-ignores-evidence` · `callsite-drops-evage`.

**A real bug the new legs caught, unrelated to the concept.** Passing `TV_RE` into `awk` with `-v`
runs escape processing over the value, so `\[TV\]` arrives as the character class `[TV]` and matches
the `T` in **every ISO timestamp** — the tv axis would have read `IN-RANGE` forever and inverted the
whole attribution. Caught red by the pre-existing transient-miss leg the moment the axis was touched;
the regex now stays in `grep -E` where it started. (`awk-v-eats-the-regex-backslashes`, paid twice.)

**Bounds, stated plainly.** `attrib=` is advisory by design, so nothing downstream *acts* differently
yet beyond sensorium's render — the room wake-gate named in the organ's own header does not read this
state at all today, which is a separate gap this review did not close. `SKEW_S = WIN_S/2` is derived
from an existing constant, not calibrated against the corpus of observed tv/mic skews; a wrong bound
mislabels a class and can never move a scene, which is why it was shipped that way rather than
withheld. And the repair is applied to **one** medium: the criterion says every state file with a
freshness-guarded reader owes the same audit, and `mesh-sensorium`'s `mark()` alone applies seven
different private staleness bounds to seven producers, six of which still publish no evidence age.

## Sources

- [arXiv:2608.02619 — Axiomatic shared-medium coordination for stigmergic systems](https://arxiv.org/abs/2608.02619) (full text: [HTML v1](https://arxiv.org/html/2608.02619v1))
- [Testing the limits of pheromone stigmergy in high-density robot swarms](https://royalsocietypublishing.org/doi/10.1098/rsos.190225) — surveyed, not landed: the density-crossover critique is adjacent to `swarm-density-adaptive-evaporation` and `swarm-trace-blind-minority-plasticity-reserve`
- [Recommender systems, stigmergy, and the tyranny of popularity](https://arxiv.org/html/2506.06162v2) — surveyed, discarded: our board has no popularity-weighted selection to invert
- [Emergent Collective Memory in Decentralized Multi-Agent AI Systems](https://arxiv.org/pdf/2512.10166) — surveyed, discarded: the ρc≈0.23 density threshold is about agent density, and our mind count is fixed and small
