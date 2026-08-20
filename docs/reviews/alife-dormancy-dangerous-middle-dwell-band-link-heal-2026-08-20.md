# ALIFE / dormancy — THE DANGEROUS MIDDLE: a fixed lag is worst when it matches the environment's own timescale

**Live review, genome mind, 2026-08-20.** Cross-domain transfer: artificial life / dormancy & seed
banks → a distributed sensor mesh's self-heal reflexes.

## The source (real, current, read)

> Jorge Hidalgo, Lorenzo Fant, Rafael Rubio de Casas, Miguel A. Muñoz,
> **"Fluctuating Environments Favor Extreme Dormancy Strategies and Penalize Intermediate Ones"**,
> arXiv:**2512.05856** (submitted 2025-12-05). <https://arxiv.org/abs/2512.05856>

Found by searching the live dormancy/seed-bank strand of the alife literature (the surrounding
context is the ALIFE 2026 conference, Waterloo, 2026-08-17..21, whose "Artificial Life in the Wild"
workshop ran *today* on exactly this question — alife let loose into "ecologies, soils, oceans,
cities, swarms, sensors": <https://alife-in-the-wild.github.io/>).

**The result.** In a delayed-logistic population where dormant individuals reactivate after a
**fixed lag α** and the birth rate carries **temporally correlated** noise of correlation time τ:

```
ẋ(t) = (b + σ ξ_τ(t)) · x(t−α) · (1 − x(t)/K) − d·x(t)                      (their Eq. 1)
G = G₀ − σ²τ(b_eff/b)² / ((1+b_eff·α)(1+b·α)) · (1 − e^(−2α/τ))             (their Eq. 9)
```

Fitness is **strongly non-monotonic in α**. Short lags track the environment; long lags average it
away; the intermediate band "simultaneously lower[s] G and T̄" — it costs *growth and persistence at
once*. Their evolutionary agent-based model confirms **bistability**: populations "evolved either
short or long dormancy times, systematically avoiding the maladaptive intermediate regime." The
penalty peaks at

```
α*  ~  min{ τ/2 , b⁻¹ }
```

— a competition between a term decaying over the intrinsic recovery timescale `b⁻¹` and a factor
`(1 − e^(−2α/τ))` growing over the environment's correlation time. They name it the
**"dangerous middle"**.

**Two conditions they state, both load-bearing:**

1. **The noise must be COLORED.** Under white/memoryless fluctuation the local extremum does not
   form at all. Their Appendix V.3 reproduces the phenomenology under Ornstein–Uhlenbeck and
   dichotomic noise alike — the requirement is memory, not a particular generator.
2. **The coupling must be MULTIPLICATIVE.** Appendix V.4: noise on the *death* rate alone makes
   `G(α)` decrease monotonically "without developing any local extrema".

## Why this is not something the mesh already embodies

The doctrine already carries **"a sense whose window is narrower than its cadence reports a sample,
not a state"** — coverage = window/cadence. That is a **monotone** fact: narrower is worse, and
nudging the cadence helps. It is the opposite shape from this one.

This says the fitness landscape over the lag is **bistable**, and therefore:

> **Incremental tuning of a dwell constant is actively misleading.** Nudging `RELOAD_AFTER` from 7
> to 6 or 8 slides *along the valley floor*. The only way out is a **jump** to an extreme.

That is the gradient reflex an operator naturally reaches for, and the paper says it is the one
move that cannot work. Nothing in the genome guards it: **207 uses of
`refractory`/`cooldown`/`backoff` across `scripts/`** (grep, 2026-08-20) and **not one of them is
sited against the measured correlation time of the thing it gates**.

Adjacent reviews checked and distinct: `allostasis-love-the-noise-viability-csd` and
`cas-two-level-micro-macro-criticality` compute lag-1 autocorrelation as a *critical-slowing-down
early warning* — autocorrelation as a rising alarm on a state variable, never as the yardstick a
dwell constant is sited against.

## The application (landed)

**File: `scripts/mesh-link-heal`** — new read-only lens `--dwell` (`dwell_band()`), plus a usage
entry, dispatch, and five `--test` legs. Acts never, writes nothing.

The healer is a five-rung escalation ladder on this node's **sole uplink**. Each rung's tick
threshold × `TICK` **is** a dormancy lag: the wall-clock dwell before that rung fires. Everything
the transfer needs is already on the durable tape (`~/.mesh/link-heal.log`, one row per episode):

| paper | mesh | measured from |
|---|---|---|
| τ (environment correlation time) | `tau_recur` — the fault's recurrence timescale | median gap between `RECOVERED` episodes |
| b⁻¹ (intrinsic recovery timescale) | `b_inv` — how fast the link comes back **unhelped** | median dark seconds of episodes that cleared with `last rung attempted: none` |
| α (dormancy lag) | each rung's dwell | `rung_ticks × TICK` |

`b_inv` is taken **only** from self-clearing episodes. A helped episode measures the healer, not the
environment — folding them would let the ladder set the very timescale it is being sited against.
Where no self-clearing episode exists, `b_inv` renders **`na`, never 0** (a zero would drive α* to
0, put every rung on the LONG side, and the lens could never fire).

### Live reading on mesh-home (2026-08-20, 144 episodes)

```
link-heal dwell-band: OUTSIDE-THE-BAND  episodes=144 gaps=143
  inter-episode gaps  CV=2.518 (vs exponential null, p=0.0002)   lag-1 ACF=0.251 (order-permutation p=0.0092)
    -> CORRELATED (each leg at alpha/2 = 0.025)
  tau_recur = 480s (8.0 min)  -> tau/2 = 240s
  b_inv     =  59s (1.0 min)  from the 29 episode(s) that cleared with NO rung
  alpha*    =  59s  BOUND BY b_inv          MIDDLE = [29s, 118s]
    reassociate  120s   a/a* =  2.03  LONG
    bounce       240s   a/a* =  4.07  LONG
    reload       420s   a/a* =  7.12  LONG
    replug       600s   a/a* = 10.17  LONG
    shout        840s   a/a* = 14.24  LONG
  NO RUNG IN THE BAND today.
  COUNTERFACTUAL: if tau/2 (240s) bound instead, the band would be [120s, 480s] and these rungs
  would sit in it: reassociate,bounce,reload
```

**The precondition genuinely holds here** and is not assumed: the arrival series is over-dispersed
(CV 2.52 vs an exponential null, p=2e-4) and positively autocorrelated (lag-1 ACF +0.25,
order-permutation p=0.009). This node's uplink environment is colored, so the valley can exist.

**Today's verdict is clean** — every rung sits on the LONG (buffering) side of α*. That is a result
that could have gone the other way, not a foregone one.

**The finding is the counterfactual.** α* is a **min over two legs measured in different fault
regimes**: `b_inv` comes from the cheap self-clearing regime (median 59s dark, the DEAUTHED-NOCARRIER
deauths), `tau/2` from the arrival series as a whole. The two are ~4× apart. In the *expensive*
regime the link does **not** clear itself in 59s (the `mixed`/`DEAUTHED` episodes on this tape run
476–498s dark; the 2026-08-17 wedge ran 55 minutes), so `b_inv` rises, α* moves to τ/2 = 240s — and
**`reload` at 420s lands inside the band**. `reload` is the rung that **unloads the driver on this
node's only network path**. It is one regime shift from the valley floor, and per the paper that is
not a position you can tune your way out of by moving `RELOAD_AFTER` a notch.

**This is a hypothesis worth a drill, not an edit.** Retuning the ladder on the sole uplink is a
substrate change (mesh-dms, coordination, rollback-first). The lens reports geometry; it does not
retune anything and must not be read as evidence any rung has already caused harm
(`[[a-shared-observable-cannot-name-the-mechanism]]`).

## What the lens refuses to do

- **Draws no band on memoryless arrivals.** A series indistinguishable from Poisson renders
  `NOT-APPLICABLE` — transferring the result past the authors' own precondition would be decoration.
- **Bonferroni on the precondition.** Two statistics (CV, lag-1 ACF) OR-ed at α each reject at ~2α.
  Each leg is tested at α/2 and the split is printed. *This was found by the test going red*: the
  first Poisson fixture was called CORRELATED at `cv_p=0.0100`, which is a genuine 1-in-100 draw —
  the lens was right and the fixture merely unlucky.
- **`na` below 12 gaps** — "not a calm link: an unmeasured one".
- **The band half-width is ours, not theirs.** The paper reports a "broad band" with no width. The
  ±1-octave convention is declared, overridable (`MESH_LINK_HEAL_DWELL_BAND_PCT`), and **printed in
  the output** rather than buried. α* itself is re-derived from the live tape every run, so the only
  constant here is that declared half-width.
- **No `mktime()`** — days-from-civil, so the lens is not blind on a busybox-awk phone body.
- **Never writes the tape it reads** (`[[a-test-that-writes-the-artifact]]`).

## Gates seen RED, then green

`--test` is green (`link-heal: all green`, rc=0). Four mutants driven from a scratch copy, each
caught by the intended leg:

| mutant | caught by |
|---|---|
| `colored = 1` (gate always passes) | `20/20 memoryless tapes CORRELATED` |
| `b_inv` fed from helped episodes too | `dwell fabricated a b_inv from helped episodes` (2 legs) |
| never report `MIDDLE` | `dwell missed a rung sited on the valley floor` |
| minimum-gap gate removed | `dwell produced a verdict below its minimum` |

**The size leg is a rate, not a draw.** Asserting a α-level gate *never* fires on a true null is
asserting the test has no size, and the only way to make that pass is to hunt seeds until one is
green — cherry-picking the test rather than testing the lens. So: 20 independent memoryless tapes,
assert that **few** fire (1/20 currently; 20/20 means the gate is not a gate).

**The bursty fixture is positively autocorrelated, and that is asserted.** An earlier cut alternated
every other gap: it passes the gate too, but on ACF **−0.97** — anti-persistence, the wrong *sign* of
memory to stand in for an OU environment. A separate leg now asserts the sign, or the "colored like
the paper's environment" claim in the fixture comment would be decoration.

## Also fixed en route

`-h|--help` was pinned at `sed -n '3,63p'`, and the usage block had grown past it: **both**
read-only lenses (`--cost-drift` at line 78, `--dwell` at 98) were documented *outside* what
`--help` printed, i.e. undiscoverable from the tool itself. Now ends at the `# Exit codes:` marker,
which cannot rot the same way.

## Where this generalises (not landed, named for the next hand)

The same siting applies to any dwell constant gating a *recurrent, autocorrelated* condition. Named
candidates with a durable tape to measure from: `mesh-bg-retry` (backoff vs job-arrival burstiness),
`mesh-sound-reflex` (repellent window vs record-arrival clustering), `mesh-ble-heal`,
`mesh-session-watchdog`. Each needs its own τ and b⁻¹ measured from its own log — a shared constant
would be the very rot this lens exists to avoid.

## Sources

- [Hidalgo, Fant, Rubio de Casas & Muñoz — *Fluctuating Environments Favor Extreme Dormancy Strategies and Penalize Intermediate Ones*, arXiv:2512.05856](https://arxiv.org/abs/2512.05856)
- [Artificial Life in the Wild — ALIFE 2026 Workshop (2026-08-20, Waterloo)](https://alife-in-the-wild.github.io/)
- [The 2026 Artificial Life Conference](https://2026.alife.org/)
- [Shoemaker & Lennon — *Evolution with a seed bank: the population genetic consequences of microbial dormancy*](https://www.biorxiv.org/content/10.1101/156356v2.full) (background on seed banks as diversity reservoirs)
