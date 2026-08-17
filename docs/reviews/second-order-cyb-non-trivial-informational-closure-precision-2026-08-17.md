# Live literature review — second-order cybernetics

**Area:** second-order cybernetics (von Foerster, Pask, Beer) · **Angle:** a concrete METRIC the area measures itself with
**Date:** 2026-08-17 · **Organ:** `scripts/mesh-precision` · **Status:** uncommitted in tree, steward lands

---

## The concept we did not embody

**Non-Trivial Informational Closure (NTIC)** — operational closure turned into a number you can
compute from two time series.

Second-order cybernetics' central postulate is **operational closure**: an observing system's
operations reference its own states, not the environment directly (von Foerster's "cybernetics of
observing systems"). The genome already embodies the **structural** form of that postulate —
`scripts/mesh-closure` computes constraint closure over the static who-enables-whom graph (Montévil
& Mossio 2015; process-enablement graphs [arXiv:2411.17012](https://arxiv.org/pdf/2411.17012)). What
it does **not** embody is the **dynamic, information-theoretic** form, which is what this literature
now measures itself with.

Sources, all read this session:

| Paper | Where | What it establishes |
|---|---|---|
| **Information Closure Theory of Consciousness** — Acer Y. C. Chang, Martin Biehl, Yen Yu, Ryota Kanai | [Frontiers in Psychology 11:1504 (2020), PMC7374725](https://pmc.ncbi.nlm.nih.gov/articles/PMC7374725/) | The canonical definitions. **Information flow** `J_t(E→Y) := I(Y_{t+1};E_t \| Y_t)`; the system is **closed** iff `J = 0` (Eq. 2). **Trivial** closure: also `I(Y_{t+1};E_t) = 0` — closed *because decoupled* (Eq. 3). **Non-trivial** closure: `J = 0` while `I(Y_{t+1};E_t) > 0` (Eq. 4) — closed *while coupled*. And the measure itself: **`NTIC_t(E→Y) := I(Y_{t+1};Y_t) − I(Y_{t+1};Y_t \| E_t)`** (Eq. 6). |
| **Quantifying Autonomy in Ant Colonies Using Non-Trivial Information Closure** — Ilya Horiguchi, Norihiro Maruyama, Shigeto Dobata, Michael Crosscombe, Takashi Ikegami | ALIFE 2024 (MIT Press), [doi:10.1162/isal_a_00804](https://direct.mit.edu/isal/article/doi/10.1162/isal_a_00804/123546/Quantifying-Autonomy-in-Ant-Colonies-Using-Non) | The live application: how much of an individual ant's next state is fixed by its own past vs its local environment. Ants hold a **consistent NTIC across timescales** — neither pure reflex (all environment) nor isolate (no coupling). The point: NTIC is an empirically usable autonomy statistic on real behavioural traces, not a philosophical position. |

**Prior coverage checked** (21 reviews in this area; none of them this): eigenform · non-trivial
machine · Pask teachback · algedonic habituation · good-regulator misread · variety overflow ·
well-founded meta-observation · relational viability · evidentiary adequacy · self-regulation
reasoning loop · and the whole VSM set (ACP indices, S2 anti-oscillation, S3\*, S3-S4 homeostat,
residual variety, error budget, PII, power relations, critic weighting, completing deficiencies).
`grep -rn 'informational closure\|NTIC' scripts/ docs/` → the only hits are `mesh-closure`'s
**structural** sense of the word.

---

## Why it bites here

The mesh has a **documented, named confusion that this statistic resolves exactly.** A sense whose
value stops moving is one of two entirely different things:

- **dead / decoupled** — the fossil family (`mesh-mag`/`mesh-gyro` racing their driver for 5 days
  with a green `--test`; the Note3 barometer reading a fossil), or
- **honestly reporting a stable world** — `mesh-psi`'s CALM, verified twice as real constancy.

`mesh-reflex-health`'s `value-frozen` flag points at **both**, which is why doctrine demotes it in
so many words: *"it points at both real constancy and this, so it is a lead, never a verdict."*
NTIC is the statistic that turns that lead into a verdict, with no new hardware and no new tape:

| reading | meaning | for a frozen sense |
|---|---|---|
| `J ≈ 0` and `I(Y';E) ≈ 0` | **TRIVIAL** — closed because *decoupled* | the fossil. The freeze **is** the finding. |
| `J ≈ 0` and `I(Y';E) > 0` | **NTIC** — closed while *coupled* | a **model holding**, not a death: its own state already carries what the world would say. |
| `J > 0` | **OPEN** — driven beyond its own state | a relay, not a model. Not a fault — it is what a raw sense should be. |

---

## Landed: `scripts/mesh-precision --closure <sys-tape> --env <env-tape>`

Report-only, like its `--independence` sibling: it touches no verdict or weight downstream.
`mesh-reflex-health` is the natural consumer for its `value-frozen` leads and is **deliberately not
wired** — one measurement lands at a time.

Output carries `I(Y';Y)`, `I(Y';Y|E)`, `I(Y';E)`, `J`, `NTIC` in bits, both null floors, both
p-values, and which null was binding.

### The estimator problem, and why this is not the last gamble again

**This file already reverted one information-theoretic axis.** Crypticity (χ = C_μ − E) fired
`CRYPTIC 1.53 bits` on a clean deterministic period-10 stream — pure finite-L bias, *a default
indistinguishable from a real read*. So the burden here is to show the difference is **in kind**,
not in optimism:

- χ needed length-L **words** — |Σ|^L causal states, exponential in L, hopeless at our tape lengths.
- NTIC needs one fixed 3-variable joint over `(Y_t, E_t, Y_{t+1})` — **K³ cells, K=2 by default, so 8
  cells**, estimable at the 1–4k samples a 14-day 5-minute tape carries.

Even so, every mutual information is positively biased at finite n, so nothing is reported raw:

1. **Two nulls, because they fail in opposite directions.** *Permutation* of E destroys its own
   temporal structure — anti-conservative for autocorrelated tapes, which is nearly everything here.
   *Circular shift* preserves it, but is invariant under a periodic E and degenerates as the offset
   nears n, so the offset is drawn from `[n/10, 9n/10]`. The floor is the **max** of the two, and
   the readout **names which null won**.
2. **The threshold is the upper tail, not the mean.** An MI's bias puts the observed value *at* the
   null mean under the null — a mean threshold is a ~50%-false-positive gate. Floor = null **q95**,
   plus an empirical p-value, and the null **mean is published beside it** so the choice is checkable.
3. **A hard sample floor** (`MESH_PREC_CLOSURE_MINN`, default 50 transitions) → UNKNOWN below it.
4. **The identity `I(Y';Y) − I(Y';Y|E) ≡ I(Y';E) − I(Y';E|Y)`** (both are the interaction
   information) is computed **both ways and asserted equal** — a wrong estimator fails it even when
   its verdict looks plausible.
5. **Tie-rule fallback in the discretizer.** Mesh numeric tapes are heavily zero-inflated (a psi
   `some avg10` column is `0.00` for most ticks). With the quantile cut landing *on* the repeated
   value, `>=` and `>` collapse in opposite directions; both are tried and the one occupying more
   bins wins. Found by running the tool on the real `pressure.log` and getting an honest UNKNOWN.

### Gate — 15 assertions, all three regimes with known answers

| fixture | must read | why it is there |
|---|---|---|
| independent noise | TRIVIAL | **the load-bearing one** — an NTIC here is the hollow sense that killed χ |
| `Y_{t+1} = E_t` | OPEN, `J ≈ 1 b` | a driven relay |
| E mirrors Y (random walk) | NTIC, `J` exactly 0 | closure while coupled |
| **two independent random walks** | TRIVIAL, circular-shift binding | autocorrelation must not read as coupling |
| **zero-inflated relay** (20% ones) | OPEN, `env_bins_used=2` | the live psi-column shape |
| constant tape / n < floor | UNKNOWN | honest refusals, never a verdict |
| 12 independent noise pairs | ≥10 TRIVIAL | **false-positive calibration** — a mean floor lands at ~6/12 |

**Mutants seen red (6/6 attempted, control green, suite 3.5 s):** floor = null mean instead of q95 ·
permutation-only null · `J` computed without conditioning on `Y_t` · sample floor ignored ·
constant-tape guard removed · tie-rule fallback removed. The permutation-only mutant is the most
instructive: two **independent** random walks then read **`NTIC` with 0.047 bits** — a fabricated
"this sense models its environment" manufactured out of nothing but shared autocorrelation. That is
the exact failure this axis exists to not commit, and it is now a red test rather than a hope.

*(One assertion is admittedly not mutant-covered: the NTIC two-way identity check is a defensive
self-check, and disabling it changes no fixture's verdict. Stated rather than dressed up.)*

### Live artifact — real mesh tapes

Both columns come from the **same line** of `~/.mesh/therm.log`, so the alignment is exact rather
than assumed (`Y` = `k10temp/Tctl`, `E` = `load=`, n=1719):

```json
{"verdict":"OPEN","n":1719,"I_next_own":0.159478,"I_next_own_given_env":0.102467,
 "I_next_env":0.064205,"flow_J":0.007194,"ntic_bits":0.057011,
 "null_q95_flow":0.00535,"null_q95_coupling":0.004859,"p_flow":0.0249,"p_coupling":0.005,
 "null_flow_winner":"circular-shift","null_coupling_winner":"circular-shift"}
```

CPU temperature is **coupled** to load (p = 0.005) and is **not** closed: load adds 0.0072 bits about
the next temperature beyond what the current temperature already carries (p = 0.025, just clearing
the q95 floor 0.0054). A thermal mass is mostly its own state — `NTIC = 0.057 b` is the redundant
part — but not entirely: the sense is a driven relay with strong inertia, which is what a
thermometer *should* be. A genuine reading with a small effect, reported as small.

*(Discarded before it became an artifact: `gpu:` temperature against the same `load=` column — the
gpu zone is absent from 174 of the 1720 lines, so index alignment would have silently paired
different ticks. Same trap the `--independence` sibling documents; two tapes are only index-alignable
when they are written together.)*

---

## Honest limits

- **A fully constant tape reads UNKNOWN, not TRIVIAL.** This is the honest answer and it bounds the
  application: `--closure` resolves the value-frozen question **at the numeric layer beneath the
  frozen label** (psi's CALM band froze for 14.2 days while `avg10` kept moving). Where the numeric
  layer is *itself* a constant, the question is undecidable from the tape alone — no statistic can
  separate a dead sensor from a perfect model when the output never moves.
- **Index alignment, not timestamp alignment** (inherited from `--independence`): honest only for
  tapes written together. Prefer two fields of one line.
- **Order 1, K=2 by default.** Coupling that only appears at longer lags or finer resolution reads as
  absent. `--bins` raises K at the usual cost — K³ cells against the same n.
- **Not wired anywhere.** No reflex consumes this yet, by choice.
