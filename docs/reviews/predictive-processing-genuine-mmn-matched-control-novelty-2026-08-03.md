# The genuine MMN — a prediction-error difference needs a MATCHED CONTROL, not a better statistic

*Live literature review, 2026-08-03. Predictive processing & the Bayesian brain, angle = a concrete
METRIC/EXPERIMENT the area uses to measure itself.*
*Landed: `scripts/mesh-novelty --control` (report-only, additive, uncommitted for steward).*

## The source (live, current)

**Widmann, A., Schröger, E., & Wetzel, N. (2026). "Measuring the Genuine Mismatch Negativity in the
Auditory Multi-Feature Paradigm." *European Journal of Neuroscience* 63(1):e70362.
[doi:10.1111/ejn.70362](https://doi.org/10.1111/ejn.70362)** (published January 2026; open at
[PMC12769272](https://pmc.ncbi.nlm.nih.gov/articles/PMC12769272/)).

Still-live surrounding debate: *"Complementary functional profiles of mismatch responses mediated by
adaptation and deviance detection point to two distinct auditory short-term memory systems"*, J
Neurophysiol, [doi:10.1152/jn.00515.2024](https://doi.org/10.1152/jn.00515.2024).

## The concept we did not embody: the matched control condition

The field's flagship *measurement instrument* for a prediction error is the **mismatch negativity** — the
deviant-minus-**standard** difference wave in an oddball sequence. The 2026 paper's point is that this
difference is **confounded by construction**: it sums genuine deviance detection *and* stimulus-specific
**adaptation** — the response to the repeated standard is suppressed by its own repetition, so the
deviant looks big without any model having been violated.

The remedy is **not a better statistic on the same contrast**. It is a second, physically identical
condition in which the adaptational state is equalised but no regularity is violated — the **cascadic
control** ("the trial directly preceding the control sound always has the same feature level (L2/F2) as
the standards … to better equalize the adaptational state"). **Genuine MMN = deviant − CONTROL.**

Verbatim verdict:

> "Negative amplitudes in the deviant-minus-standard comparison in the auditory multi-feature oddball
> paradigm do not permit conclusions on the presence or amplitude of the genuine MMN."

Measured at Fz — two of four deviance effects survive the control **reduced**, and two **do not survive
at all**:

| deviant | classic (dev−standard) | genuine (dev−control) | |
|---|---|---|---|
| frequency | −1.87 µV | −0.91 µV | ~halved |
| location  | −1.25 µV | −0.49 µV | ~60% gone |
| intensity | −1.91 µV | **+0.44 µV** | **absent** |
| duration  | −2.29 µV | −0.30 µV | absent/minimal |

## Where the mesh commits the same error

`scripts/mesh-novelty --conditional` **is** a deviant-minus-standard contrast: it scores
`bits(e | prev)` and reads the excess over the marginal `bits(e)` as "contextual prediction error"
(landed 2026-06-20). Two structural problems, both exactly the paper's:

1. **The difference cannot be negative.** `p_cond` is clamped `min(cand, p(cur))` (`:476`), so the
   conditional score can never fall below the marginal. "The conditional scored higher" is the shape of
   the arithmetic, not a finding.
2. **The excess has a mechanical source that mimics deviance** — the mesh's stimulus-specific
   adaptation. A Laplace-smoothed transition row is sparse; a predecessor row that simply never happened
   to contain `cur` yields `cand ≪ p(cur)` and several bits of "prediction error" out of finite-sample
   chance alone.

No axis on the file, and no sibling, ever scores the *same event against a matched control*: `--levels`
compares two **real** baselines, `--bayesian` asks how far the belief moves, `--progress` asks whether
the sequence is becoming compressible, `--territory`/`--valence`/`--tempering` are orthogonal. The
surrogate-null idiom is already mesh-wide (`mesh-criticality`, `mesh-leadlag`, `mesh-endogeneity`,
`mesh-correlate`) — this novelty *sense* simply never had one, which is why its contextual excess has
never once been read against chance.

## The control, transposed: frequency-matched order surrogates

Shuffle the **baseline's order** K times. The type multiset — hence every marginal `p(t)`, hence the
entire rarity/adaptational state — is preserved **exactly**; only the sequential regularity is
destroyed. Re-score the identical recent events, with the identical predecessors, against each shuffled
transition model. That is the cascadic control: what the contextual excess looks like when there is
nothing to violate.

```
classic = bits(e|prev) − bits(e)                     # the deviant−standard analogue (confounded)
genuine = classic − mean(classic over K order-surrogates)
p       = (1 + #{surrogate ≥ actual}) / (K+1)        # Bonferroni over the V types tested
```

`GENUINE` (a real sequential regularity was violated) · `ADAPTATION` (the classic excess is what a
frequency-matched control produces anyway — the absent-intensity-MMN case) · `FLAT` (no classic
difference to explain) · `UNDERPOWERED` (see below). Report-only: it does **not** touch `mean_bits`,
`scored`, or the `--threshold` wake gate. Deterministic (fixed seed) so a quoted number reproduces.

## Live result on the real board (2026-08-03, 3000-line `chat.log`, window 40)

```
K=339 order-surrogates, α_eff=0.00294 Bonferroni over 17 types
[verify]       GENUINE     classic 1.68b − control 0.50b = genuine 1.18b  p=0.0029  n=1
[witness]      GENUINE     classic 1.36b − control 0.25b = genuine 1.11b  p=0.0029  n=1
[access-state] ADAPTATION  classic 1.94b − control 1.45b = genuine 0.50b  p=0.1706  n=2
[done]         ADAPTATION  classic 1.89b − control 1.65b = genuine 0.24b  p=0.1088  n=10
[fyi]          ADAPTATION  classic 0.76b − control 0.58b = genuine 0.17b  p=0.0824  n=10
… 8 ADAPTATION, 7 FLAT, 2 GENUINE
occurrence-weighted mean: CLASSIC excess 0.92b → GENUINE 0.22b — 24% survives the control
```

**76% of `--conditional`'s contextual prediction error on the live board is adaptation**, and the
type with the *largest* classic excess — `[access-state]`, 1.94b, the axis's own top-ranked deviant —
does **not** survive (p=0.17). That is the mesh's absent intensity MMN, on real data.

## A flaw the live run caught in the fix itself

The first live run reported **zero** GENUINE and every type ADAPTATION. That verdict was manufactured by
the instrument: a K-surrogate permutation test cannot return `p < 1/(K+1)`, and Bonferroni over 17 types
pulled the bar to α_eff = 0.0029 — *below* the K=200 floor of 0.005. GENUINE was **unreachable**, and an
unreachable positive is indistinguishable from a real null. Fixed: K auto-raises to
`ceil(1/α_eff) − 1` (capped at `MESH_NOVELTY_CONTROL_KMAX`), and a pinned-low K that still cannot
resolve reports **UNDERPOWERED** rather than a null the instrument could not have refuted. The inverse of
"a gate you have not seen fail" — a gate that could never fire positive.

An i.i.d. 3-symbol probe also minted one false GENUINE at an uncorrected α=0.05 (family-wise error
~1−(1−α)^V, not α) — hence the Bonferroni, stated rather than hidden. Conservative by construction.

## Gates (all seen RED before green)

`--test` legs, same alphabet, differing only in whether a regularity exists to violate:

- **A structured** — strict `taking↔done` alternation + a `done`-after-`done` violation → `[done]`
  GENUINE (classic 0.63b − control 0.08b = 0.54b, p=0.005).
- **B surrogate** — the *same lines order-shuffled*: identical marginals, identical adaptational state,
  no regularity → the identical tip event must **not** be GENUINE (reads ADAPTATION, p=0.36).
- **C thesis** — i.i.d. 3-symbol stream: classic excess up to 0.47b anyway, **zero** GENUINE.
- **Resolution** — structured fixture's p ≤ α_eff with K auto-raised; `K=3, kmax=3` → UNDERPOWERED.
- **α knob** — α=0 → nothing GENUINE (the significance test is load-bearing, not decorative).

Seen red: no-shuffle surrogate (null==actual → A reads ADAPTATION) · classifier forced `GENUINE`
(B and C go red) · control blind to context (`cand = p(cur)` → everything FLAT).

## Not done / open

- **Report-only by design.** It does not gate the wake path. Wiring `ADAPTATION` into the `--threshold`
  spend gate is the obvious payoff (do not pay a mind-wake for a difference that does not survive its
  control) — but that is behavioral and gates SPEND; steward/operator lands it after live validation,
  per this file's standing instrument-first discipline.
- The surrogate destroys **first-order** sequence structure only; a longer-range regularity violated at
  lag > 1 is invisible to both the classic axis and this control.
- `n=1` types can reach GENUINE on a single occurrence. The p-value is honest about the surrogate null,
  not about the sampling of the event itself.
