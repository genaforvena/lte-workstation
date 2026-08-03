# SOC live review — the SUBSAMPLING-DEFLATED avalanche exponent and the COARSE-GRAINING RECOVERY CURVE

- **Date:** 2026-08-03 · **Area:** self-organizing criticality & power-law dynamics
- **Angle:** a known FAILURE MODE of the area — a measured critical exponent that is systematically
  wrong because of *how much of the system you can see*, not because of the system.
- **Organ:** `scripts/mesh-criticality` — new read-only sidecar `--coarse` (`coarse_recovery()`,
  `_gamma_at()`, `_lin_slope()`). Never touches m̂, `regime()`, or the SUPERCRITICAL alarm.

## The literature

**Primary.** Srinivasan, K., Ribeiro, T. L., Kells, P. & Plenz, D., *"The recovery of parabolic
avalanches in spatially subsampled neuronal networks at criticality"*, **Scientific Reports 14,
19329 (2024)**, doi:10.1038/s41598-024-70014-4 (preprint bioRxiv 2024.02.26.582056).

**Live continuation (the same correction, in current use).** Ribeiro, T. L., Vakili, A., Gifford, B.,
Siddiqui, R., Sinfuego, V., Pajevic, S. & Plenz, D., *"Critical scaling of novelty in the cortex"*,
**Nature Communications 17, 1555 (10 Jan 2026)**, PMC12407764 — corrects for subsampling by temporal
coarse-graining before reporting the quadratic ⟨S⟩–T scaling.

### The failure mode

The exponent χ in ⟨S⟩ ~ T^χ — the direct estimate of 1/σνz, and **exactly this file's `gamma_fit`** —
is **not robust to subsampling**. Srinivasan et al. run a critical branching network and observe only
a fraction of its units. Because a cascade that continues in an *unobserved* unit reads as an
avalanche that **ended**, avalanches are truncated, and χ falls from its true value **2 to ≈1–1.3**.
The bias is systematic, downward, and silent.

### The correction is also a test — the part worth having

Their fix is to **temporally coarse-grain** (bin k consecutive steps together) and raise the
**coincident-activity threshold θ**. χ then climbs back to ≈2 *even at 0.1% sampling*. Crucially:
recovery of χ = 2 is **"exclusive to the critical model"** and **fails for near-sub- and supercritical
branching dynamics** (they place the tolerance at ~1.4% of the E/I parameter around criticality).

So the **shape of γ(k)** is a *positive* criticality test, not merely a correction. A climb says the
deflation was a sampling artifact of a genuinely critical process. A flat curve says coarse-graining
found nothing to recover.

## Why this is NOT already embodied

`scripts/mesh-criticality` carries ~22 stacked SOC reviews. Checked against all of them:

| existing | what it does | why it is not this |
|---|---|---|
| banner / MR estimator | claims subsampling-robustness | true **for m̂ only** — robustness is a property of the *slope* of log r_k vs k. It does **not** transfer to the avalanche exponents. |
| `bin_sanity()` | compares **one** Δt to ⟨IEI⟩ → CALIBRATED/GLUING/FRAGMENTING | a single-point granularity flag. No sweep, no γ. |
| `--crackling` | exponent **coherence** at that one Δt | reads **both** its numbers off the same truncated avalanches (γ_fit *and* γ_pred=(τt−1)/(τ−1)) — see the live finding below. |
| `--suscept` | χ = ⟨S²⟩/⟨S⟩ | **a different quantity that shares the symbol χ.** Here χ ≡ γ, the ⟨S⟩(T) slope. Do not conflate. |
| `--widom` / `--sob` / `--hurst` | silence fraction φ / size-distribution modality / frequency-domain slope | none of them varies the **observation scale** and watches an exponent respond. |

`grep -niE 'coarse|subsampl'` over the file before this change: subsampling appears only as prose
about m̂; "coarse-graining" appears nowhere.

## What was built

`coarse_recovery(evs, win_h, bin_s, …)`:

1. Sweep k over `CRIT_COARSE_KS` (default 1,2,4,8); bin = k·base.
2. A bin counts as **ACTIVE** only at ≥ θ events (`CRIT_COARSE_THETA`, default 1 — the paper's second axis).
3. Re-extract avalanches at each level, fit γ_k = slope of log⟨S⟩ vs log T.
4. **Base bin = `bin_s // max(k)`** (`CRIT_COARSE_BASE_S` to override). Coarse-graining needs
   headroom: starting at `BIN_S` leaves none — on this board the silences vanish by k=2 and the sweep
   dies with one usable level. Running from `BIN_S/kmax` **up to** `BIN_S` means the **top level
   reproduces exactly the bin `--crackling` reads its γ_fit at**, and the levels below it are the
   over-fragmented regime the recovery is meant to climb out of.
5. **The gluing wall:** stop the sweep once the silence fraction φ_k < `CRIT_COARSE_PHI_MIN` (0.10) —
   past that the cascades have merged into one super-run and any further γ is an artifact, not a
   recovery. (The same separation criterion `--widom` reports.)
6. Classify by OLS of γ_k on log k: **RECOVERING / FLAT / DECLINING / INSUFFICIENT** (≥3 usable levels
   required; fewer = honest defer).

## Gate — RED first

`--test` asserts the arithmetic, that θ is live, and **the mechanism itself**: the same generator with
true parabolic scaling (S ~ T²), heavily subsampled, must read a **deflated** γ(k=1) inside the
paper's 1–1.3 band and **well below** its fully-sampled counterpart, then **recover** toward 2.
Six mutants run from a scratch copy:

| mutant | result |
|---|---|
| A constant label | **RED** — subsampled fixture no longer RECOVERS |
| B θ inert (`act=list(cnt)`) | **RED** — θ above every bin count must leave no active bins |
| C gluing wall removed | **RED** — the wall fixture stops deferring |
| D γ hardcoded to the true exponent | **RED** — no deflation seen |
| E base = `bin_s` (no headroom) | **RED** — top level no longer lands on the `--crackling` bin |
| F trend on level index instead of log k | *not red* — a monotone reparametrization of the x-axis; sign-preserving, so the label is genuinely unchanged. Stated, not papered over. |

Restored → `smoke-test: ok`.

## Live reading (2026-08-03, this board)

```
12h : RECOVERING  γ(k=1)=1.18 → γ_max=1.64 at k=8, trend +0.213, base=37s→296s
      curve k=1:1.18(n=106,φ=0.89) k=2:1.31(n=87,φ=0.80) k=4:1.42(n=59,φ=0.66) k=8:1.64(n=41,φ=0.45)
96h : FLAT        γ pinned ≈1.32 across all four levels, trend −0.030
--crackling 96h : CONSISTENT, γ_fit=1.240 vs γ_pred=1.262 (τ=1.661, τt=1.834), 289 avalanches
```

**The caveat lands where it was aimed.** `--crackling` reports **CONSISTENT** at γ≈1.25 — sitting
squarely inside the subsampling-deflated 1–1.3 band. Under this review that agreement is not
evidence of coherent critical exponents; it is **what two equally-deflated estimates look like**, and
the 96h sweep shows **no recovery** (FLAT) to argue otherwise.

**Two honest tensions, stated rather than resolved:**

1. The 12h window RECOVERS and the 96h window is FLAT. Both are real readings of different windows;
   neither is the answer. Which one the sidecar should be read at is unsettled.
2. m̂ read **0.585 SUBCRITICAL** at 12h in the same run — and the paper says recovery is *exclusive*
   to criticality. A RECOVERING curve on a subcritical board is either a window-length artifact, a
   sign the mesh's γ(k) climb has a different cause than the paper's, or m̂ itself under-reading. Open.

## Unwired next steps

- **Sweep θ as well as k** — the paper's second axis, and it trades off linearly against sampling
  fraction (their θ=3000 fully-sampled ≡ θ=3 at 0.1%). Currently θ is a fixed knob, not a swept axis.
- **Attach the verdict to `--crackling`'s output** as a standing caveat once the window question above
  is settled (deliberately not done now: it would re-interpret a shipped verdict on an unresolved read).
- Join γ(k) to the m̂ tape — the twin of the edge-optimality / dynrange / suscept tape-joins already
  named as open in the other SOC landings.

## Sources

- [The recovery of parabolic avalanches in spatially subsampled neuronal networks at criticality — Sci Rep 14, 19329 (2024)](https://www.nature.com/articles/s41598-024-70014-4) ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11335857/), [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.02.26.582056v1.full))
- [Critical scaling of novelty in the cortex — Nat Commun 17, 1555 (10 Jan 2026)](https://www.nature.com/articles/s41467-025-68277-0) ([PMC12407764](https://pmc.ncbi.nlm.nih.gov/articles/PMC12407764/))
- [Parabolic avalanche scaling in the synchronization of cortical cell assemblies — Nat Commun (2023)](https://www.nature.com/articles/s41467-023-37976-x)
