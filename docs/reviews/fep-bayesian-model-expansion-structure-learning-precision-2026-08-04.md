# FEP / active inference — live review 2026-08-04

## Bayesian Model **Expansion**: the mesh has the pruning half of structure learning and calls it the whole thing

**Area:** free energy principle & active inference (Friston).
**Angle asked for:** a foundational idea we may have MISread or applied too loosely.
**Answer:** we did — and the misreading is written verbatim in our own genome source.

---

## 1. The source (live, 2026)

> **Neacsu, V., So, W.-K., Rutar, D., Da Costa, L., Adams, R. A., & Friston, K.**
> *Reviewing Structure Learning in and Out of the Active Inference Framework.*
> **Minds and Machines** (2026), doi:`10.1007/s11023-026-09787-8`, published **2026-06-15**, open access CC-BY.
> Found via web search → Springer; metadata confirmed via the Semantic Scholar graph API
> (`DOI:10.1007/s11023-026-09787-8`, corpus id 289210540); full text read from the CC-BY PDF
> (`link.springer.com/content/pdf/10.1007/s11023-026-09787-8.pdf`, 32pp).

Verbatim, the three levels and their **timescale separation** (§3):

> "There are at least three very distinct kinds of model optimisation considered in AIF: (Active)
> Inference (AI), Parametric Learning (PL), and Structure Learning (SL) … At the fastest timescale, we
> have the (Active) Inference of hidden or latent causes (i.e., states and/or policies) … At a slower
> timescale, we have Parametric Learning (a.k.a. Bayesian learning) … At the slowest timescale, we have
> Structure Learning."

Verbatim, the two members of that slowest level (§3.3):

> "The second type of approach involves applying **Bayesian Model Reduction (BMR) or Bayesian Model
> Expansion (BME)**. These types of SL offer a more expedited method by circumventing the necessity of
> reinversion (of models) … Technically, these are **two complementary ways** of improving the marginal
> likelihood of the data by inferring the model."

Verbatim, the mechanism of the expansion half (§4.1.5, reporting Smith, Schwartenbeck et al. 2020):

> "agents here were equipped with **extra connectivity 'slots' that can be engaged when the evidence for
> a model with an extra 'slot' is higher than the evidence for a model without this 'slot'.**"

and the shape of the state space itself (§4.2):

> "…a given (AIF) generative model … **whose state-space can expand, contract, or transform**, based on
> comparing and selecting from alternative hypotheses."

---

## 2. The misread, in our own words

`scripts/mesh-precision` shipped `--bmr` on 2026-07-28 with this line in its header:

> "This is the field's actual mechanism for structure learning, post-hoc pruning, 'aha-moments' and sleep."

It is **one subset** of that mechanism. The memory coverage file went further and recorded the angle as
settled — *"complexity↔accuracy trade-off — NOW CLOSED … Do NOT re-serve this angle."*

Every structure move the genome can make is a **removal**:

| move | tool | direction |
|---|---|---|
| pin a parameter back to its prior | `mesh-precision --bmr` | ← reduce |
| price redundancy as complexity | `mesh-sensorium --balance` | ← reduce |
| retire an unfiring organ | `mesh-reflex-decay` | ← reduce |
| **add a state the data warrant** | *(nothing)* | → **absent** |

That asymmetry has a consequence, not just an aesthetic: with no expansion move, a **two-regime world is
silently pooled into one**, and every statistic taken over that window mixes the regimes. Nothing goes
red; the estimate is simply of a population that does not exist.

This is also *not* the same finding as the 2026-08-03 window-freeze review
(`fep-window-freeze-ranking-basis-sound-reflex-2026-08-03.md`). That one asked **when** a ranking basis
may move. This one asks whether the window it moves within is **one population at all**. They meet at
the same tape from opposite sides.

---

## 3. The concrete application: `scripts/mesh-precision --bme`

Report-only, in the same posture as every other axis in that file — it changes no verdict and no weight.

**Model comparison.** Both models share the same known per-point precision `π = 1/var(all)` and the same
prior `N(μ0, 1/π0)`, `π0 = k·π`, so the Bayes factor prices **only the extra slot**:

```
lnE(seg) = −½·ln((π0+Λ)/π0) + ½·Λ²z²/(π0+Λ)          Λ = m·π,  z = mean_seg − μ0
M1 (one state)   : lnE(all)
M2 (extra state) : logsumexp_t[ lnE(A_t) + lnE(B_t) ] − ln(#splits)
lnK = ln p(D|M2) − ln p(D|M1)      →  EXPAND / MARGINAL / PARSIMONIOUS  (Kass & Raftery band |lnK|<1)
```

Two deliberate choices:

- **The evidence for M2 is marginalised over splits, not maximised.** A max over `#splits` candidates is
  a free lunch: the search itself manufactures a step. The uniform-prior marginalisation charges
  `−ln(#splits)` for it. This is load-bearing and **measured**: removing that one term takes the
  false-EXPAND rate on pure single-regime noise from **0.031 → 0.338** (n=60, reps=1500). `logK_bestsplit`
  is reported alongside `logK` precisely so a reader can see how much of an apparent regime change is
  search artifact.
- **σ² is estimated from the whole tape**, so a real two-regime tape inflates its own noise estimate.
  The test is therefore **conservative against expansion**, never optimistic for it.

**`--bme --calibrate` prices the reading**, in the posture `--recover` established for `--bmr`:

```
n=60  reps=1500 step=1.00σ : false-EXPAND=0.031 · power=0.847   → CALIBRATED
n=100 reps=400  step=1.00σ : false-EXPAND=0.020 · power=0.960   → CALIBRATED
n=24  reps=400  step=1.00σ : false-EXPAND=0.035 · power=0.435   → BLUNT
```

An axis that cannot say *"at this n I cannot answer"* asserts nothing; at n=24 it says it.

---

## 4. Live reading at landing — the mesh is running a pooled two-regime corpus

`dyn` over `~/.mesh/records.log` — the character axis `mesh-sound-reflex` ranks records by:

```
$ grep -o 'dyn=[0-9.]*' ~/.mesh/records.log | cut -d= -f2 | mesh-precision --bme - --prior 0.421465
precision[bme]: EXPAND — n=471: lnK=4.52 (best-split lnK=8.60 over 466 candidate splits) ·
                best split @205 → mean 0.4626 | 0.3897

$ … --win 100    → MARGINAL  (n=100, lnK=−0.86)
```

Row 205 is **2026-07-29T17:22Z**. The corpus the grinder ranks against is **two regimes pooled as one**
over its full window, and single-regime over its last 100 rows — consistent with, and independent of, the
basis-drift measurement of 2026-08-03.

**Honest caveat, stated because the axis cannot state it:** the scape/drop kind-mix also shifts across
that split (13.7% → 9.0% scape). The regime and the composition are **confounded on this tape**. `--bme`
reports *that* a split is warranted; it never reports its cause. And `records.log` is a sliding window
([[records-log-is-a-sliding-window]]), so this n and this split are today's answer, not a constant.

---

## 5. Gates (all seen RED before green)

`mesh-precision --test`, five new legs; runtime 0.98s → 1.18s total.

| # | leg | asserts |
|---|---|---|
| 1 | 12×~0 then 12×~5 | `EXPAND` **and** `split=12` — locating the split, not merely announcing one |
| 2 | single-regime N(0,1), n=24 | **not** `EXPAND`, while `logK_bestsplit > 1` — i.e. its best split *would* read EXPAND under a max |
| 3 | frozen tape / n=5 | `PARSIMONIOUS` (one state, exactly) / `UNKNOWN` (never a fabricated expansion) |
| 4 | `--calibrate --n 60` | `CALIBRATED` |
| 5 | `--calibrate --n 24` | `BLUNT` |

Mutants driven from a scratch copy, each red for its own reason (`rc=1`):

- `logsumexp − ln(#splits)` → `max` : **leg 2 red** (pure noise reads `EXPAND`, `logK=2.21`) *and* leg 4
  red (`LOOSE`, false-EXPAND 0.33). This is the gate that matters — the multiplicity penalty is the only
  thing standing between the axis and buying a hidden state out of noise.
- `"split":bt` → `bt+1` : leg 1 red (`split=13`).
- calibration verdict hard-wired to `CALIBRATED` : leg 5 red.

---

## 6. Scope / what this is not

- Not a planner. The mesh has no rollout model, so the EFE-as-variational-inference line of 2026
  (arXiv:2606.20658, arXiv:2606.04935) still has no organ — noted, not landed.
- Not automatic. `--bme` is report-only: it tells a consumer that a window mixes populations. Acting on
  that (splitting a ranking basis, re-calibrating a band) is a separate, deliberate change.
- Not a cause detector. It answers "do the data warrant a second state", never "why".

## 7. Coverage-map correction

`fep-active-inference-coverage` said the complexity↔accuracy angle was **closed**. It was closed for the
**reduction** half. The correct statement: BMS = BMR **+ BME**; `--bmr` landed 2026-07-28, `--bme` lands
now, and structure learning is only now half-embodied in both directions rather than fully embodied in
one. Still open on this level: the **timescale separation** — the review is explicit that Structure
Learning "ensues in the absence of additional (sensorial) evidence", i.e. **offline**, while both our
`--bmr` and `--bme` run on the live tape whenever a caller asks.
