# Prediction UNCERTAINTY is a second, PROACTIVE boundary signal — and every axis we own is the other one

**Live literature review — predictive processing & the Bayesian brain, recent result (2023-2026).**
Genome mind, mesh-home, 2026-08-20. Landed: `scripts/mesh-novelty --uncertainty` (report-only).

## The source

**Nguyen TT, Etzel JA, Bezdek MA, Zacks JM — "Multiple event segmentation mechanisms in the human
brain", *eLife* 107955, reviewed preprint v3, published 2026-07-07, doi:10.7554/eLife.107955.3**
(read at <https://elifesciences.org/articles/107955>; v2 record at
<https://elifesciences.org/reviewed-preprints/107955>). Found by walking the live 2025-2026 event-
segmentation literature forward from the Zacks lab's own modelling arm (Nguyen et al. 2024, cited
there); corroborating context read the same session: Gabhart, Xiong & Bastos, "Predictive coding: a
more cognitive process than we thought?", *Trends Cogn Sci* 2025, doi:10.1016/j.tics.2025.01.012
(PMC12821738) — **already read and set aside by the 2026-08-18 review**, so nothing here rests on it.

Event Segmentation Theory has always said an internal model is torn down and rebuilt when
**prediction error** spikes. This paper separates that from a second, computationally distinct
control signal — **prediction uncertainty** — and finds both, dissociated in the brain and in
behaviour. Verbatim:

> "Both error-driven and uncertainty-driven boundaries were associated with unique pattern shifts."

> "Error-driven boundaries were associated with early pattern shifts in ventrolateral prefrontal
> areas, followed by pattern stabilization in prefrontal and temporal areas. Uncertainty-driven
> boundaries were linked to shifts in parietal regions within the dorsal attention network, with
> minimal subsequent stabilization."

> "Even though error-driven and uncertainty-driven event model updating were associated with the
> same brain regions, the two updating mechanisms were associated with distinct temporal dynamics."

And the property that makes uncertainty a different **kind** of signal rather than a weaker error
signal:

> "The advantage of relying on prediction uncertainty to detect event boundaries is that it is
> inherently proactive: the cognitive system can start looking for cues about what might come next
> **before the next event starts**."

Their earlier modelling arm, quoted in the paper: *"both error-driven and uncertainty-driven updating
signals aligned with human segmentation and categorization judgments, but that uncertainty-driven
segmentation aligned significantly better."*

## What we do not embody

**Every deviance axis in the mesh is error-driven, without exception.** In `mesh-novelty` alone:
marginal `−log P(e)` · `--conditional` `−log P(e|prev)` · `--bayesian` (how far the event MOVED the
belief) · `--levels` (deviance at two timescales) · `--territory` · `--when` (how OVERDUE an arrival
is) · `--features` (which LEVEL was violated) · `--control` (is the excess genuine) · `--progress`
(is the error FALLING). Every one of them is a function of an event that **already arrived**: they
score the residual. `--diversity` is the nearest miss and is not this — it is the Shannon evenness of
the *marginal* repertoire's shape, a global statistic about the corpus, not the spread of the model's
**next-step** distribution given where we are right now.

Nothing in this file scores the entropy of a predictive distribution. The one genuine neighbour
elsewhere in the genome is `mesh-reflex-health`'s **AMBIGUITY** axis (2026-08-17, Champion et al.,
*Neural Computation* 38(3):439–469) — expected-free-energy ambiguity *is* "the expected conditional
entropy of observations given states", and it was checked before this landed. It is a different
quantity: it prices how often an **organ answers `n/a`**, i.e. how uninformative its own outputs are,
and it holds no sequential model at all. It cannot say "given that the last line was `[access-state]`,
the next one is spread over 17.6 effective successors". So the wake gate this organ feeds is structurally **reactive**: the mesh can notice
that it has already been surprised, never that it has stopped being able to predict.

Those are not the same event, and the difference is not a threshold. **A context whose successor
distribution has gone flat emits no surprising line at all** — every successor is individually
ordinary, each one individually cheap — while the model holding that context has quietly stopped
being a model. That boundary is unreachable from the error axis at any bar.

## The instrument (`mesh-novelty --uncertainty`, report-only)

One first-order model; both signals read off the **same row**, so the comparison is not confounded by
two models:

- **ERROR** `bits = −log2 P(x_t | ctx)`, floored at the marginal exactly as `p_cond()` does. This *is*
  the number `--conditional` reports — asserted, not assumed (leg U10 compares the two element-wise).
- **UNCERT** `cons = H(P(· | ctx))` in bits, using **no part of `x_t`**, reported as a reduction
  (`gain`) against the marginal entropy `H_marg`. A context reads UNPREDICTIVE when its own entropy
  buys less than `UNC_FRAC` (default 10%) of `H_marg` — self-calibrating to the live corpus, never an
  assumed 0..1.

Two legs and the conservative min, the discipline `--when` and `--control` already earned:

| leg | what it is | which way it is biased |
|---|---|---|
| `h_smooth` | entropy of the Laplace-smoothed row over the whole alphabet — what a consumer of this model would actually use | **UP**: a thin or unseen context is maximally "uncertain" by construction. `prior_share = V/(n+V)` states how much of the row is prior rather than board |
| `h_mm` | plug-in entropy of the RAW row + Miller–Madow `(k_obs−1)/(2n ln2)` | repairs the plug-in estimator's opposite, **DOWNWARD** bias at small n |

`cons = min(h_smooth, h_mm)` — conservative against the very claim this mode exists to make. And the
resolution it actually has: **n draws cannot exhibit empirical entropy above log2(min(n, V))**. A row
under that ceiling reads UNDERPOWERED — never "predictable", never "unpredictable".

Two refusals, both load-bearing and both mutation-tested:

- **NO-MODEL** (`n = 0`, a context never seen as a predecessor). Its smoothed entropy is the alphabet
  maximum, and that means only that nothing was ever learned here. Calling it "uncertain" would be
  the *unprepared-channel* fallacy — the instrument's own blankness reported as a property of the
  board. (Removing this refusal is mutant M3; it goes red.)
- **UNDERPOWERED** (row under `UNC_MINSUP`, or ceiling under the bar) — the same refusal in the other
  direction. On the live board, one row is **96.7% prior mass**.

**Proactive, demonstrated rather than asserted.** The `next` block is computed from the last line's
type and the baseline alone, with no successor in hand. Leg U7 replaces every recent line *except the
last* with different ordinary events (the baseline is untouched) and requires the verdict not to
move; mutant M5 makes `next` read the last observed transition instead, and goes red. It is the only
verdict in this file about an event that does not exist yet.

## Live measurement (this node's board, 2026-08-20, `~/.mesh/chat.log`, 2961 baseline lines)

```
one model, two signals: alphabet 87, H_marg 4.39b → UNPREDICTIVE at ≥3.95b (90% of marginal);
                        error bar 4.0b. Both read off the SAME row.
last 40 events: BOTH 9 · ERROR-DRIVEN 11 · UNCERTAINTY-DRIVEN 6 · neither 10 ·
                UNDERPOWERED 3 · NO-MODEL 1
are they one signal? r(error, uncertainty) = +0.16 over 36 scored events — NON-redundant.
UNCERTAINTY-DRIVEN ×6 — the successor was ORDINARY, the model was not:
  [handoff]→[fyi]        err 3.77b  H 4.14b (k_eff 17.6 of 87, n=49,  20 distinct, prior 64.0%)
  [access-state]→[fyi]   err 2.75b  H 4.14b (k_eff 17.6 of 87, n=255, 41 distinct, prior 25.4%)
  [access-state]→[selfcare] err 3.89b  H 4.14b (same row)
NEXT LINE — not yet posted, no successor used: after [hw-fault] the model is UNPREDICTIVE at
  H=4.36b → k_eff 20.5 of 87 (n=147, 32 distinct; likeliest [done], [fyi], [hw-fault]).
```

**Six of forty** recent events are boundaries that no axis in this file can express: `err` 2.75–3.89b,
all **below** the 4.0b error bar, so the wake gate is silent on every one of them, while the context
holding them has ~17.6 effective successors out of an 87-symbol alphabet. `r = +0.16` says plainly
that the error axis does not carry the uncertainty axis: one gate cannot fire for both.

**A second, unasked-for finding fell out of the same run.** The median context `gain` over the 36
scored events is **0.58 bits of a 4.39-bit marginal — 13.2%**. That is the *whole* value the
first-order transition model buys, and `--conditional`, the mesh's flagship predictive-coding axis,
rests entirely on it. It is not nothing (the sharp rows are real: `[fyi]→[alert]` gains 0.87b,
`[idle]→[taking]` 0.55b) but it is much less than "contextual prediction error" implies to a reader.
Report-only, named here, not acted on.

## Gates

10 assertions (U1–U10), 7 mutants, **each seen RED from a scratch copy with the control GREEN**:

| mutant | leg it actually kills |
|---|---|
| M1 error leg drops the marginal floor | U10 error-leg-is-`--conditional` |
| M2 no conservative min (smoothed leg alone) | U6 conservative-min *(also U1 — attributed)* |
| M3 NO-MODEL refusal removed | U4 no-model-refused |
| M4 UNDERPOWERED refusal removed | U5 underpowered-refused |
| M5 `next` reads the last observed transition | U7 proactive-next |
| M6 honest-n/a guard removed | U8 honest-na |
| M7 Miller–Madow correction dropped | U2 uncertainty-driven-with-silent-error *(also U9)* |

The fixture is built so the two signals **must** disagree: `[flat]` → 8 successors uniformly (a sharp
error signal is impossible there — every successor is ordinary) against `[det]` → always `[dee]`
(zero uncertainty, so a violation is pure error), plus a never-seen context and a 3-observation
context for the two refusals. `--test` runs in 0.09s; every other mode (`--conditional`, `--levels`,
`--when`, `--features`, `--bayesian`, `--diversity`) re-ran rc=0.

## Honest boundaries

- **Report-only.** `mean_bits`, `--threshold` and `--edge` are untouched; wiring an uncertainty
  boundary into the wake/SPEND gate is the steward's, and it is the obvious payoff (an uncertainty
  boundary is available *before* the line lands, which no error signal can be).
- **First-order only**, like `--conditional` — a lag>1 flat model is still invisible. This does not
  close the "longer-range regularity violation" lead in the coverage memory.
- `chat.log` is a sliding window: every `n`, every `H_marg`, and the 13.2% median gain are **today's
  answers**, to be re-derived and never quoted.
- The bar is a fraction of the live marginal entropy, which is the right calibration for "the context
  buys nothing" but means the class counts move as the board's repertoire moves.
- The paper's *temporal-dynamics* half (error boundaries stabilize afterwards, uncertainty ones do
  not) is **not** landed: it needs the post-boundary trajectory held against the pre-boundary one,
  which is a different instrument.

## The generalizable rule

**A residual is a claim about what arrived; the spread of the model is a claim about what could
arrive — and only the second is available before the event.** An organ that scores only residuals
cannot notice that it has stopped being able to predict, because that state is *silent by
construction*: it emits no outlier. Sibling of `[[a-senses-coverage-is-window-over-cadence]]` (a
sense whose window is narrower than its cadence reports a sample, not a state) and of the matched-
control rule from 2026-08-03 (a difference whose sign is guaranteed by its arithmetic is not
evidence). New neighbour, stated for the next hand: **maximal entropy in a smoothed model is the
instrument's blankness before it is the world's unpredictability — refuse it by support, not by
threshold.**
