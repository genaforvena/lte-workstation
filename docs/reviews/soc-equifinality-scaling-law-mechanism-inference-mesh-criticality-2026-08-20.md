# SOC & power-law dynamics (live review): **equifinality** — a scaling law is a compatibility condition, not a mechanism identifier

**Date:** 2026-08-20
**Area:** self-organizing criticality & power-law dynamics, from the angle of a **known CRITIQUE**.
**Landing:** a critique we do NOT embody — **equifinality of scaling laws**, with two sequence-level
discriminators (`D`, `I_excess`) and a latent-conditioning leg, from a paper published **ten days ago**.
**Verdict:** concept ACCEPTED as new and load-bearing. **LANDED as code** — `scripts/mesh-criticality
--equifinal`, read-only, no alarm (uncommitted, for the steward). Live measurement below.

## The source

Arthur Charpentier, **"Beyond Zipf's Law: Equifinality and Mechanistic Inference from Scaling Laws"**,
arXiv:**2608.09459v2** — submitted 10 Aug 2026, revised 17 Aug 2026.
<https://arxiv.org/abs/2608.09459>

He constructs four processes — an i.i.d. finite-Zipf process, a persistent Markov chain, a canonical
**sample-space-reducing** (SSR) process, and a latent mixture — that share the **identical stationary
marginal** while differing entirely in temporal organization. The conclusion is the critique:

> "matching a scaling law is therefore a compatibility condition, not a mechanism identifier"

and the remedy is not a better fit but **observables on which the candidates make different predictions**:

| statistic | definition | i.i.d. | latent mix | Markov | SSR |
|---|---|---|---|---|---|
| `I_excess` | `NMI(X_t,X_{t+1}) − E_shuffle[NMI]`, shuffle preserving length + marginal frequencies, order destroyed (20 permutations) | 0.000 | 0.000 | 0.188 | 0.350 |
| `D` | `P(R_{t+1} < R_t \| R_{t+1} ≠ R_t)`, `R` = global empirical frequency rank, rank 1 = most frequent | 0.5 | 0.5 | 0.500 | 0.946 |

Third diagnostic: **conditioning on latent variables** — does pooling across a latent create the
apparent Zipfian structure?

## Why this is new to us

`mesh-criticality` already carries eighteen sidecars, several of them SOC critiques (bin-width artifact,
subsampling deflation, coherent-noise null, record-dynamics aging null, SOB-vs-SOC, quasicriticality,
two-level micro/macro, Taylor's law, driven separability). **Every one of them reads the tape as a COUNT
series** — how many events per bin — and asks whether the counts propagate, cluster, collapse or scale.
Each then fits an exponent from a **marginal**.

The type sequence — the ordered identity of *who* or *what* posted — is discarded by the binning before
any of them sees it. That is exactly where both of Charpentier's discriminators live. Confirmed absent:
no `sample-space`, `equifinal`, mutual-information or reversibility axis anywhere in `scripts/` or
`docs/`.

## Why SSR specifically matters for this board

A sample-space-reducing process (Corominas-Murtra, Hanel & Thurner) mints an **exact Zipf marginal from a
history-dependent narrowing** — no critical point, no branching ratio, no cascade. The mesh's
coordination lifecycle **is** that shape: a broad `[task]` narrows to one `[taking]` owner, then to one
`[done]`; the sample space of who may legally post next *shrinks* as a strand proceeds.

So the board's rank-frequency heavy tail has a ready **non-critical generator sitting inside its own
protocol** — and `m̂` is structurally blind to it, because `m̂` counts events regardless of identity: a
narrowing baton and a critical cascade put the same counts in the same bins. `D` is the observable that
separates them.

## What landed — `scripts/mesh-criticality --equifinal`

Read-only, no alarm, no board post. It cannot be one: it says *a number elsewhere means less than it
looks*, which is a caveat on a reading, never an incident.

Verdicts: `SSR-DIRECTIONAL` / `EXPANDING-ANTI-SSR` / `MARKOV-PERSISTENT` / `EXCHANGEABLE` /
`INSUFFICIENT`, plus a **separate** latent verdict `POOLING-ARTIFACT` / `STRATUM-STABLE`.

Three design decisions that were **measured, not assumed**:

1. **The effect-size floor is load-bearing.** The shuffle band narrows as `1/√n` and this board carries
   ~2350 rank-changing transitions, so the live band is `[0.489,0.509]`. The first live run read
   `D=0.510` → filed **SSR-DIRECTIONAL**, i.e. a mechanism named on an excursion sitting **0.44 away**
   from the SSR prediction of ~0.95. Significance and materiality are different claims; without a floor
   this sidecar would read SSR forever on any busy window. `CRIT_EQ_D_MIN=0.05` / `CRIT_EQ_IEX_MIN=0.02`,
   and a band-clearing-but-immaterial excursion is **printed** rather than silently dropped.
2. **The latent leg does not compete with the sequence verdict.** Making it a fifth label was tried and
   is wrong: a *slow* latent (the operator's day is exactly that) creates serial dependence as a side
   effect, so a pure latent-mixture fixture scores `I_excess` 0.13–0.26 and would be filed
   `MARKOV-PERSISTENT` with the pooling never named. Measured, then split into two orthogonal fields.
3. **Size-matching is what makes the latent leg mean anything.** A stratum is smaller than the pool and
   the MLE is biased upward at small `n`. On a *homogeneous i.i.d.* stream, measured here: stratum
   α=1.609 vs **full-pool** α=1.224 → unmatched gap **−0.385**, past the 0.35 tolerance, a
   `POOLING-ARTIFACT` conjured out of sample size alone. The **size-matched** gap on the same stream is
   **+0.011**. The comparison is also two-sided on purpose — the *sign* of a pooling shift depends on how
   the latent partitions the type universe; the claim ("the pooled exponent is not the process's
   exponent at any value of the latent") does not.

## The gate, and it has been seen RED

`--test` drives the paper's four processes in pure form at a pinned seed, and asserts:

- SSR → `SSR-DIRECTIONAL`, `D` ≥ 0.65 (measured **0.755**)
- the **time-reversed** SSR fixture → `EXPANDING-ANTI-SSR`, `D` ≤ 0.35 (measured **0.238**) — reversal
  maps `D → 1−D` exactly and leaves the marginal untouched, so it is the one anti-fixture that cannot be
  accused of smuggling in a different distribution alongside the different direction
- persistent Markov → `MARKOV-PERSISTENT` (measured `I_excess` **0.273**)
- i.i.d. → `EXCHANGEABLE`
- **the four marginals must NOT separate them**: |α_iid − α_markov| ≤ 0.25, else the lens is redundant
  with every other exponent in the file
- four distinct labels (a collapsed label is a dead axis)
- the floor: a weak-SSR mixture (w=0.12) whose `D` **does** clear its band but sits inside the floor must
  read `EXCHANGEABLE` **and say so** — and the *same generator* at w=0.30 must be **named**, so the floor
  is a floor and not a mute
- latent: stratified fixture → `POOLING-ARTIFACT`, homogeneous → `STRATUM-STABLE`, plus the leg above
  proving the unmatched comparison would misfire
- `INSUFFICIENT` naming the missing quantity below `CRIT_EQ_MIN_N` and below `CRIT_EQ_MIN_K`

Three mutants run from a scratch copy, all confirmed **RED**:

| mutant | result |
|---|---|
| effect-size floor removed (`CRIT_EQ_D_MIN=0`) | `FAIL … a persistent Markov chain must read MARKOV-PERSISTENT, got SSR-DIRECTIONAL` |
| `D` made direction-blind (`rb>ra`) | `FAIL … must read SSR-DIRECTIONAL …, got EXPANDING-ANTI-SSR D=0.241` |
| size-matching removed (pool = whole stream) | `FAIL … must read POOLING-ARTIFACT, got STRATUM-STABLE gap=−0.118` |

Full `mesh-criticality --test`: **`smoke-test: ok` · `alarm-test: ok`**.

## Live measurement (mesh-home, 2026-08-20, 72h window)

```
criticality equifinality: MARKOV-PERSISTENT (token=sender, D=0.510 vs shuffle band [0.489,0.509]
over 2344 rank-changing transitions, I_excess=0.112 vs shuffle band <=0.005, alpha=1.325 over 95
types, 2806 events, window=72h; secondary D=0.510 I_excess=0.098 over 89 markers; latent
STRATUM-STABLE gap=+0.087 (within-hour alpha=1.648 vs size-matched pooled alpha=1.735 over 24
strata at n=112)) [D clears its shuffle band but |D-0.5|=0.010 < CRIT_EQ_D_MIN=0.050 —
significant, not material]
```

Re-run with `CRIT_EQ_TOKEN=marker`: same verdict, `D=0.510`, `I_excess=0.098`, `STRATUM-STABLE`. The
secondary token is printed always for exactly this reason — a verdict that held for posters and not for
markers would be a claim about one choice of token, never about the board.

**What the board actually is, then.** Three readings, and the first is the one that surprised:

1. **The protocol-narrowing hypothesis is FALSIFIED on the live tape.** `[task] → [taking] → [done]` is a
   textbook sample-space reduction, so SSR was the expected verdict; `D` sits at 0.510 against an SSR
   prediction of ~0.95. The narrowing is real in the *protocol* and invisible in the *sequence* —
   plausibly because strands interleave, so the tape is many narrowings superposed, and superposition
   destroys the directionality of each.
2. **The sequence does carry real order** — `I_excess = 0.112`, an order of magnitude past its shuffle
   band and in the same range as the paper's Markov control (0.188). The board is not exchangeable: who
   posts next depends on who posted last. This is a *live* finding about the mesh, not a null result.
3. **The exponent is not an artifact of the operator's day** — `STRATUM-STABLE`, gap +0.087 against a
   0.35 tolerance, at matched `n`. α=1.325 over posters is a property of the process, not of pooling.

**The caveat this instrument exists to deliver:** every exponent elsewhere in `mesh-criticality` is
compatible with a persistent-Markov board. `m̂ ≈ 1` is not thereby wrong — but a marginal that a Markov
chain reproduces exactly is not, on its own, evidence for a critical cascade.

## Files

- `scripts/mesh-criticality` — `--equifinal` sidecar (+ its `--test` legs, header, env block). Uncommitted.
