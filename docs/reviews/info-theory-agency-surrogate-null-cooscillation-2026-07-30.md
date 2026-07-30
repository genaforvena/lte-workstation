# Info-theory of agency (live review): the block-permutation surrogate null — a *measured* test for spurious coupling, replacing an i.i.d. parametric p

**Date:** 2026-07-30
**Area:** information theory of agency — empowerment / predictive information, from the angle of a concrete *metric* the field uses to measure itself.
**Landing:** a mechanism we do NOT embody — the **block-permutation / block-bootstrap surrogate null** used to separate *genuine cross-signal synergy* from *spurious temporal coupling driven by a common signal*.

---

## What the area already gave us (so this doesn't re-tread)

Prior reviews in this series already landed the headline info-theoretic-agency metrics:

- **Empowerment** (channel capacity actions→future sensors) — `info-theory-agency-assistive-operator-empowerment` + `…-process-empowerment-closed-loop-undercount` (07-28).
- **Predictive information** (`I(past;future)`, structure vs noise) — `…-predictive-information-structure-vs-noise` (07-28); embodied as `mesh-precision`'s `pred_info`.
- **Semantic information** (Kolchinsky–Wolpert viability-relevant bits) — `…-semantic-information-scramble-viability` (07-29).
- **Statistical complexity / crypticity** `C_μ ≥ E` — `…-crypticity-stored-memory` (07-30); built then discarded (hollow on short logs).
- **Integrated information / PID emergence** (Rosas Ψ, synergy atoms) — embodied in `mesh-situation`; and the **MPR C_JS** in `mesh-criticality`.

So Partial Information Decomposition *as a quantity* is NOT un-embodied — `mesh-situation` already carries a PID-flavoured Ψ. What is un-embodied is the **falsification apparatus** the same literature pairs with it: the surrogate null that tells you an observed coupling is *real interaction* and not two signals riding a shared driver.

## The concept, and where I found it (live 2025–2026 literature)

**Riedl, C. (2025). "Emergent Coordination in Multi-Agent Language Models."** arXiv:2510.05174 (Oct 2025). https://arxiv.org/html/2510.05174v1

Riedl measures whether a group of agents is genuinely *coordinating* (vs merely co-varying) by a **Williams–Beer two-source Partial Information Decomposition of the time-delayed mutual information** the pair carries about a joint future target:

```
I({X_i,t , X_j,t} ; T_ij,t+ℓ)  =  UI_i + UI_j + Red_ij + Syn_ij
```

- `Red_ij` — **redundant** information (what either signal alone already tells you → the signature of a *shared driver / common mode*).
- `Syn_ij` — **synergistic** information (predictable only from the *joint* state → the signature of *genuine interaction*).

The load-bearing move — and the part we do not have — is the **surrogate falsification** he runs to prove the synergy is not an artifact:

1. **Row-wise shuffle** — break agent *identities* while preserving each timepoint's dynamics. Surviving synergy = identity-locked differentiation, not per-timestep coincidence.
2. **Column-wise *block* shuffle** — destroy the *cross-agent temporal coupling* while preserving each agent's *own* autocorrelated dynamics. If the coupling survives this null it was **spurious temporal coupling driven by common feedback**, not interaction.

This is the classic **surrogate-data / block-bootstrap** method (Theiler 1992; Politis–Romano circular block bootstrap 1994) applied as the *significance test* for an info-theoretic coupling. The key property: the surrogate **preserves each series' own autocorrelation** and only kills the *between-series* alignment — so the null is "two signals with exactly these marginal dynamics, but no shared timing."

## The gap it exposes in our genome: `scripts/mesh-cooscillate`

`mesh-cooscillate` is the mesh's co-movement miner: for each pair of numeric sensor signals it computes **Pearson r of first-differences** (Δ-series) and emits the strongest as an idea-hypothesis. Its significance gate is a **parametric i.i.d. test**:

- `scripts/mesh-cooscillate:397` — `fisher_p(r,n)`: `z = atanh(r)·sqrt(n−3)`, `p = erfc(|z|/√2)`.
- `scripts/mesh-cooscillate:494–495` — `pcorr = min(1, fisher_p(r,nd)·ntests); if pcorr>ALPHA: continue` (Bonferroni over `ntests` pairs).

**The defect.** The Fisher-z null assumes the `nd` Δ-steps are **independent**. They are not: they are first-differences of RSSI / lux / baro / battery series binned to a common clock — **autocorrelated and often non-stationary** (slow environmental drift, RF-path trends). Under positive autocorrelation the *effective* sample size is far below `nd`, so `sqrt(nd−3)` over-inflates `z` and **`fisher_p` is anticonservative**. Two signals that merely share a slow common trend (scanner-side RF drift, a diurnal environmental ramp) can clear the p-floor. Bonferroni corrects for *how many pairs were tried* — it does **nothing** about a mis-specified per-pair null.

**The tell that this is real, not hypothetical.** The file has accreted **three separate hand-found skip layers**, each a counterexample to that null, patched one incident at a time:

- the **part-whole confound** skip (`n` vs the `rssi:` channels it counts — :415–423),
- the **floor-noise gate** (two near-floor RSSI signals co-moving on shared SNR≈0 scan noise — :435–440),
- the **mobility-class / APPLIANCE** branches (personal×appliance and appliance×appliance = "same-zone scanner-side common-mode, not co-movement" — :514–560).

Every one of these is the same underlying failure: **a coupling that is statistically "significant" under the i.i.d. null but is a shared driver, not an interaction.** The block-permutation surrogate is the *single principled measurement* that subsumes the whole family — it asks directly "does this coupling survive a null that keeps each signal's own dynamics but destroys their shared timing?", which is exactly the question the three skips each answer for one special case.

## Concrete proposal (named file)

**File:** `scripts/mesh-cooscillate`. Replace/augment the parametric `fisher_p` gate with a **circular block-bootstrap surrogate p**:

1. For each candidate pair `(A,B)` with aligned Δ-series over the common bins, compute observed `|r|`.
2. Build `K` (≈500–1000) surrogates by **circularly block-shuffling B's Δ-series** in blocks of length `b ≈ nd^(1/3)` (Politis–Romano) — this preserves B's autocorrelation, destroys A↔B alignment. (Riedl's column-wise block shuffle.)
3. Surrogate p = fraction of surrogates with `|r_surr| ≥ |r_obs|`. Gate on this (still Bonferroni-scaled over `ntests`) **instead of** `fisher_p`.

A coupling from a shared slow driver produces high `|r_surr|` too (both series keep their trend, and a block-shuffled trend still aligns by chance) → high surrogate p → correctly rejected. A genuine tight co-movement (one carrier, e.g. two devices in one bag) collapses under the shuffle → low surrogate p → kept. This is the *measurement* the mobility-class rule currently stands in for by hand.

**Safe landing path (mirrors the tool's existing report-only modes).** Do **not** flip the live emit gate blind — `mesh-cooscillate` is a scheduled reflex (`# reflex-cadence: 13-59/30`). First add a **report-only `--surrogate`** diagnostic (idiomatic: the tool already has report-only `--dry`/`--list`) that prints, for every currently-emitting pair, both `p_fisher` and `p_surrogate`. Run it against live `presence.log` to produce the evidence — *how many pairs that clear the i.i.d. gate fail the surrogate null.* Only if that evidence is compelling does the emit gate change, and by then the three ad-hoc skips can likely retire behind the one measurement.

This is deferred-not-discarded for the same honest reason the crypticity review deferred CSSR: the gate change needs a real-data validation run I will not fake against a live reflex. The concept, the exact defect (`:397`, `:494`), and the method are landed here; the `--surrogate` diagnostic is the next bounded, zero-behaviour-change step.

## Why not just "discard"

Because the failure it names is **live and recurring** — the genome is already carrying three hand-maintained patches for exactly the false positives an i.i.d. correlation null produces on autocorrelated sensor Δ-series, and the surrogate-null literature (Riedl 2025; Theiler 1992; Politis–Romano 1994) is precisely the principled test that replaces them. It also connects cleanly to what we already embody: it is the falsification half of the PID/synergy machinery `mesh-situation` already uses on the value side.

## Sources

- Riedl, C. (2025). *Emergent Coordination in Multi-Agent Language Models.* arXiv:2510.05174. https://arxiv.org/html/2510.05174v1
- Williams, P. & Beer, R. (2010). *Nonnegative Decomposition of Multivariate Information.* arXiv:1004.2515 (the Red/UI/Syn PID atoms).
- Theiler, J. et al. (1992). *Testing for nonlinearity in time series: the method of surrogate data.* Physica D 58:77.
- Politis, D. & Romano, J. (1994). *The Stationary Bootstrap.* JASA 89:1303 (circular/block bootstrap for autocorrelated series).
