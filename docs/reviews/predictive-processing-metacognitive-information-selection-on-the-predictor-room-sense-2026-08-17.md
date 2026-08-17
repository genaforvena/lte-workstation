# Live literature review — predictive processing & the Bayesian brain

**Area:** predictive processing / Bayesian brain · **Angle:** a concrete METRIC the field measures itself with
**Date:** 2026-08-17 · **Organ:** `scripts/mesh-room-sense` · **Status:** uncommitted in tree, steward lands

---

## The concept we did not embody

**Type-2 (metacognitive) sensitivity — and its model-free form, normalised metacognitive
information `meta-I₂ᵣ`.**

The field separates two axes that we have been collapsing into one:

- **Type-1**: was the verdict right? (accuracy / d′ — how well the signal discriminates the world)
- **Type-2**: does the system's own **confidence** discriminate its right calls from its wrong ones?

Type-2 is *not* derivable from type-1. A sense can be highly accurate and have a confidence label
that carries **zero** information about when it is wrong, and vice versa.

Sources, all read this session:

| Paper | Where | What it establishes |
|---|---|---|
| **Do LLMs Know What They Know? Measuring Metacognitive Efficiency with Signal Detection Theory** — Jon-Paul Cacioli | [arXiv:2603.25112](https://arxiv.org/abs/2603.25112), 26 Mar 2026 (v3, 28 Jul 2026) | The live result. (1) The standard summary **M-ratio = meta-d′/d′ is criticised** — pinned near 1 by construction, and *undefined* wherever there is no two-alternative type-1 decision (open-ended answering). (2) Report the **model-free** quantity instead: **meta-I₂ᵣ**, normalised information the confidence signal carries about correctness, plus the **type-2 ROC** and its z-ROC slope directly. (3) Metacognitive information varies **1.98×** across models and is **uncorrelated with accuracy** (rank ρ = **−0.80** TriviaQA, **+0.00** Natural Questions); z-ROC slopes 0.78–1.18 (confidence distributions are *unequal-variance*, which is what M silently absorbs). (4) meta-I₂ᵣ **perfectly tracks the accuracy gain from confidence-based ABSTENTION (ρ = +1.00)**. |
| **HMeta-d: hierarchical Bayesian estimation of metacognitive efficiency from confidence ratings** — Stephen M. Fleming | [Neuroscience of Consciousness 2017(1): nix007](https://academic.oup.com/nc/article/2017/1/nix007/3748261) | The standard estimator being criticised; establishes meta-d′ as "the type-1 d′ an ideal observer would need to produce the observed confidence–correctness contingency". |
| **On the assumptions behind metacognitive measurements** | [PMC9520519](https://pmc.ncbi.nlm.nih.gov/articles/PMC9520519/) | The assumption audit: these measures require the confidence distribution over **both** correct and incorrect trials. Range-restrict the confidence variable and the measure is not degraded — it is undefined. |

**The one sentence that binds:** *a confidence label is worth exactly the abstention it buys, and
that worth is bounded above by H(confidence) **as recorded**.*

**Prior coverage checked** (all embodied, none of them this): Bayesian surprise vs Shannon
(2026-07-28) · Bayesian model reduction / Occam (07-28) · circular inference overcounting (07-28) ·
conformal distribution-free coverage as precision (08-04) · model recovery / identifiability (08-04) ·
genuine-MMN matched control (08-03) · local-global two-timescale (07-27) · corollary discharge
(08-14) · omission responses (08-15) · FEP epistemic value (07-30) · Bayesian model expansion (08-04) ·
predictive information rate (08-15) · and `scripts/mesh-precision`, which measures **precision =
inverse variance of a sense's signal** — a type-1 reliability. Nothing in the genome asks whether a
sense's *own emitted confidence* discriminates its hits from its misses.

---

## The measured bite on this node

Several senses publish a confidence label: `mesh-room-sense` (`confidence=high|medium|low`),
`mesh-context`, `mesh-body-motion` (`conf=0.85(high)`), `mesh-home-state` (a vote margin). No
consumer **abstains** on it — they re-print it — and nothing scores it.

I went to score the one with the longest tape. `~/.mesh/room-sense.log`, measured 2026-08-17:

```
span      2026-07-15T05:17:01Z → 2026-08-17T05:17:01Z   (33 days)
records   253
confidence=high   253
confidence=medium   0
confidence=low      0        →  H(confidence) = 0 bits
EMPTY verdicts      0
```

**That is not a degenerate sense. It is selection on the predictor.** `scripts/mesh-room-sense`
emitted its log line only inside

```bash
if [ "${MISHA_CONFIRMED_ONLY:-1}" != 1 ] || { [ "$verdict" = "PRESENT" ] && [ "$confidence" = "high" ]; }; then
```

— the sense's **only durable tape was conditioned on the very variable whose informativeness you
would want to score**. At the declared cadence (`2-59/5`, 288 evaluations/day) the reflex ran
~9,500 times in that window and retained 253 (**2.7%**); every `EMPTY`, every `UNCERTAIN`, every
medium/low confidence was written nowhere. Over such a tape meta-I₂ᵣ is **0 by construction**, and
no consumer could ever have profited from abstaining on a label that is a constant wherever it is
readable.

Note the failure is *invisible from inside*: the log is fresh, the lines are honest, each record is
individually true. Only the marginal distribution — the thing nobody looks at — is dead. This is the
same family as the doctrine's `mesh-guardian` fix (a dry-run writing the record it exists to check →
give it its **own** log) and the liveness-touch convention (decouple *ran-live* from
*value-changed*): **one `printf` was serving two duties.**

- the **WAKE SIGNAL** — an actuator trigger. Correctly gated: a room change must not wake Misha off
  ambient sound (operator 2026-06-24, tier-1).
- the **OBSERVATION RECORD** — must be unconditional, or it is not an observation.

---

## Landed: `scripts/mesh-room-sense` — observation tape split from wake edge

1. **`wake_emit_ok <verdict> <confidence>`** — the actuator gate, extracted verbatim from the inline
   condition (unchanged behaviour, `MISHA_CONFIRMED_ONLY=0` opt-out preserved).
2. **`tape_room_eval <ts> <verdict> <confidence> <status> <occupancy> [degraded] [signals]`** —
   unconditional per-evaluation record to `~/.mesh/room-sense-tape.log`, called at the **top of the
   `edge)` branch**, before any debounce or confidence gating can drop it. Self-trimming to
   `ROOM_TAPE_KEEP=4032` lines (14 days at the 5-min cadence), newest-first.
3. Header block carries the literature + the measured 253/253 finding; the Artifacts section now says
   plainly which file is the actuator trigger and which is the record.

**Live artifact** (repo copy, real `--edge` run, 2026-08-17T14:25:59Z):

```
~/.mesh/room-sense-tape.log
2026-08-17T14:25:59Z verdict=PRESENT confidence=high status=OCCUPIED occupancy=OCCUPIED \
  degraded=phone-unreachable,body-unknown,kbd-unknown,cam-blind signals=kbd=UNKNOWN screen=UNKNOWN …
```

**Gate** (`--test`, +11 assertions: 4 wake-edge, 7 tape). The load-bearing key is that the two duties
must **disagree on the same input** — a medium-confidence evaluation is exactly what the wake gate
drops, so if the tape drops it too the selection bug is back. Asserted: 3 evaluations → 3 records; the
dropped `EMPTY/medium` is present; ≥3 distinct confidence values survive (H > 0); the trim fires and
**evicts the oldest** (a "newest survives" assertion alone is vacuous — appends always land at the
end); an absent directory is a silent no-op that creates no tree.

**Mutants seen red** (scratch copy, 6/6 — control green):

| Mutant | Caught by |
|---|---|
| tape gated on `confidence=high` (the original bug) | 3 records → 1; dropped-medium assertion |
| `wake_emit_ok` always fires | PRESENT+medium / EMPTY must not wake |
| trim keeps the oldest (`head`) | the eviction-direction assertion |
| trim never fires | file grew to 303 lines |
| tape `mkdir -p`s an absent tree | must-not-create assertion |
| tape hardcodes `confidence=high` | confidence axis collapsed to 1 value |

---

## Honest limit — what this is NOT

An unconditional tape **restores H(confidence)**; it does **not** supply the correctness labels
meta-I₂ᵣ needs. This is the *precondition*, not the measurement. Scoring still needs an outcome
channel independent of this fusion's own inputs — room speech (`~/.mesh/room-transcript.txt`) is the
candidate, and it is **one-sided**: speech in the window is evidence of OCCUPIED, but silence is not
evidence of EMPTY. So a future `--meta` leg can score the positive class only, and must say so.
**Do not read a restored tape as a scored confidence.**

Second limit: the tape starts empty. Any meta-I₂ᵣ claim about this sense is ≥14 days away, and the
tape only begins filling once the steward lands this and `mesh-sync-tools` deploys it — the deployed
`~/.local/bin/mesh-room-sense` is still the single-printf version.

**Open lead, not a claim:** `~/.mesh/body-motion.log` shows the same shape (94/94 `conf=…(high)`).
I did not verify whether that log is likewise gated on its own confidence value. If it is, the fix
is the same shape; if it is not, a genuinely constant confidence there is its own finding.
