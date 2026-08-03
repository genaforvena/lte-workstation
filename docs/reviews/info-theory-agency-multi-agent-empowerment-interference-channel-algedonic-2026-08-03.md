# Live review — information theory of agency: MULTI-AGENT empowerment / interference-channel decomposition

**Date:** 2026-08-03 · **Window:** genome · **Seam:** empowerment / predictive information (live literature)
**Status:** BUILT (report-only, on-demand) — `scripts/mesh-algedonic --agency-actors`

## The paper

**Tristan Shah, Ilya Nemenman, Daniel Polani, Stas Tiomkin — "Multi-Agent Empowerment and Emergence of
Complex Behavior in Groups", [arXiv:2604.21155](https://arxiv.org/abs/2604.21155) (submitted 22 Apr 2026).**
Same Polani/Tiomkin line as the process-empowerment fix the mesh already embodies
(doi:10.1088/2632-072X/adf2ec, landed 2026-07-28 as algedonic `CL_UNDERCOUNT`/`CL_INFLATED`).

Found by web search of the live 2026 empowerment literature, alongside (rejected as already-covered or
not-a-passive-measure): arXiv:2510.05996 discounted empowerment · arXiv:2605.06346 bridge interfaces
(already reviewed 07-31, plasticity) · arXiv:2511.04177 assistive/disempowerment (embodied in
`mesh-interruptibility`) · arXiv:2607.16858 direction-free epistemic free energy (belongs to the FEP seam) ·
arXiv:2602.05463 empowerment-per-joule (benchmark-relative by the authors' own statement; no measurable
bound to port).

## The concept we did not embody

Channel capacity — the quantity under empowerment — is intractable for coupled nonlinear dynamics. Shah et al.
linearize and decompose the coupled system into an **interference channel**. For agent *n*:

```
E⁽ⁿ⁾  = ½ln|C⁽ⁿ⁾F⁽ⁿ'ⁿ⁾S⁽ⁿ⁾F⁽ⁿ'ⁿ⁾†C⁽ⁿ⁾† + Σz⁽ⁿ⁾| − ½ln|Σz⁽ⁿ⁾|
Σz⁽ⁿ⁾ = Sz⁽ⁿ⁾ + Σ_{m≠n} C⁽ⁿ⁾F⁽ⁿ'ᵐ⁾S⁽ᵐ⁾F⁽ⁿ'ᵐ⁾†C⁽ⁿ⁾†
```

The load-bearing move is the second line: **every other agent's control covariance enters MY effective noise
floor**. Others are not random noise — they are *structured, per-interferer-attributable* interference in my
own action→future-state channel.

Their empirical result matters as much as the formula: in a 125-agent Vicsek flock, **egoistic empowerment
maximization suppresses consensus** (order parameter pinned near 0, agents self-organize into
counter-propagating bands) while each individual's control capacity stays high. Coordination loss is
**invisible to every individual empowerment read** — it only appears when the group is measured as a group.

Distinct from what we already have: assistive empowerment / multi-party disempowerment (Yang &
Kleiman-Weiner, `mesh-interruptibility`) asks *how my action changes ANOTHER agent's* empowerment. This asks
the dual: *how another agent's concurrent action degrades MY OWN* channel — and attributes it.

## Why it applies here (measured, not asserted)

`mesh-algedonic`'s `agency_info()` builds ONE binary action column from the board
(`::  [done|homeostasis|resource-guard|…]`), discarding the window that signed the line. That models the mesh
as a **single agent**. Measured on the live board + `~/.mesh/algedonic.log`, 2026-08-03:

- **523** action events from **12 distinct windows** (genome 206, land 167, access-probe 50, criticality 38,
  senses 15, tg 12, pub 10, sound 8, health 7, witness 6, discover 3, stress 1)
- of the **496** pain intervals carrying any action, **365 (73.6%) had ≥2 DISTINCT actors** in the same
  1800s lookback

So ~3/4 of the evidence behind every `agency=`/`closedloop=`/`agencybias=` label comes from intervals where
the "agent" was several minds at once. Under that collapse a mind with real control and a mind that is a rock
rolling downhill are indistinguishable, and the cost of concurrency is silently pooled into the marginal.

## What was built — `scripts/mesh-algedonic --agency-actors`

The discrete analog of the decomposition. Per actor *w*: `MI(action_w ; next Δpain-bucket)` over the whole
tape, then **stratified** by whether any OTHER window acted in the same lookback:

- `solo` = rows where `actors − {w}` is empty · `intf` = rows where it is not
- `IFR_DEGRADED` when solo control materially exceeds interfered control (others are Σz inflation),
  `IFR_ENHANCED` for the cooperation shape, `IFR_NONE` otherwise, `IFR_NA` when a stratum is too thin
- summary line `ACTORS_{CLEAR,INTERFERED,NA,UNKNOWN} <actors> <multi> <single> degraded= assessed=`

Two traps the build had to defuse, both inherited from this seam's own prior lessons:

1. **The strata have different N, so their plug-in MIs carry different finite-sample bias, and their RAW
   difference is an artefact** — the 2026-07-30 Panzeri–Treves lesson one level up. Each stratum is debiased
   by its OWN shuffled-action surrogate MEAN (fixed seed, `crc32` of the window name — `hash()` of a str is
   `PYTHONHASHSEED`-randomized and would have made the "reproducible verdict" claim false every run) before
   comparison. `null95` remains as the per-actor significance bar.
2. **An unattributable board line is DROPPED, never folded into a wildcard actor** — a `?` actor would
   manufacture interference against every real window.

Read-only, on-demand, never in the 10-min reflex path, never escalates, never routes work. rc is derived from
the verdict LINE, not from python's exit: a crashed reader prints nothing and must read UNKNOWN/rc 2, not a
plausible clean verdict.

## Gate — RED-verified, 5 mutants (run from a scratch copy)

| # | mutation | result |
|---|---|---|
| 1 | remove the stratification (both strata = pooled stream, i.e. the single-agent read) | **RED** — `IFR_NONE`, `ACTORS_CLEAR` |
| 2 | compare RAW plug-in MIs (drop per-stratum debiasing) | **RED** — pure-noise strata read `IFR_DEGRADED`, `solo_dbg=0.108` |
| 3 | drop the per-stratum floor | **RED** — thin stratum fabricates `IFR_DEGRADED` instead of `IFR_NA` |
| 4 | empty/crashed read returns `ACTORS_CLEAR`/rc 0 | **RED** — caught by a poisoned `python3` on PATH |
| 5 | fold unattributable lines into a `?` actor | **RED** — mints a third `ACTOR` line |

Mutants 2, 4 and 5 each survived a first version of the gate and forced a stronger fixture (an unequal-N
noise trace where the bias alone crosses the margin; a poisoned interpreter; and unsigned board lines that
actually match the action regex). Clean tree green; `--test` runs in 0.92s, well inside `mesh-doctor`'s
timeout.

## Live reading (2026-08-03)

```
ACTORS_CLEAR 12 366 131 degraded=0 assessed=7
```

7 of 12 actors clear the per-stratum floors; none reads `IFR_DEGRADED`; 5 read `IFR_NA` (honest — their solo
or interfered stratum has too few acting rows). **Caveat stated up front:** every per-actor MI on this tape is
~0.00x bits, and at n=1895 the surrogate floor is tiny too, so a `BIAS_REAL` at `mi=0.003` (sound, stress)
means *clears chance*, not *matters*. Significance is not magnitude. The value of the sidecar right now is
that it CAN answer per-window instead of pooling — and that `366 multi / 131 single` is now a printed number
rather than an unexamined assumption inside the pooled read.

## Open (not built)

- The paper's group-level finding (egoistic empowerment suppresses consensus) suggests a **mesh order
  parameter** — do the minds' actions align on the same pain axis, or counter-propagate? That needs a
  per-action TARGET axis, which the board does not carry. Not fabricable from `[done]` lines.
- Discounted empowerment (arXiv:2510.05996, short vs long horizon) remains open from the 07-30 review.
