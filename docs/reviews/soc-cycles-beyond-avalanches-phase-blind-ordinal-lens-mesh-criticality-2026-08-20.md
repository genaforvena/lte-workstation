# SOC / power-law dynamics — CYCLES are an observable avalanche scaling cannot see, and our one timing lens is phase-blind by construction

**Live review, 2026-08-20.** Area: self-organized criticality & power-law dynamics.
Angle asked for: **cross-domain transfer, applied concretely to a distributed sensor mesh.**
Landed in: `scripts/mesh-criticality` — new `_phase_lock()` probe + a PHASE qualifier on the
`--complexity` (CECP) verdict, and the gate the `REGULAR` branch never had.

---

## The source (live literature, found by web search)

**Bosiljka Tadić, Alexander Shapoval & Mikhail Shnirman, "Self-organised dynamics beyond scaling of
avalanches: Cyclic stress fluctuations in critical sandpiles"** — [arXiv:2403.15859](https://arxiv.org/abs/2403.15859),
cond-mat.stat-mech, 2024.

Its claim, in one line: **the avalanche size/duration distribution is not the only SOC observable, and
it is not the most robust one.** Driving a BTW or Manna sandpile and watching the *stress* series
rather than the avalanches, they find spontaneous cycles — "the spontaneous appearance of cycles is
another characteristic of self-organised criticality" — with their own multifractal singularity
spectra. And the regimes come apart: "the power-law segment is preserved with slightly changed
exponents until the driving exceeds a specific critical rate ≳1/R\*; then the scaling of avalanches
is lost", the pile "becomes frequently overloaded launching anomalously large avalanches" and the
size/duration distributions grow a bump at the right tail — **while the cycles persist.** Their
first-return statistic on the outflow current Δ = O(t+1) − O(t) separates the regimes where the
avalanche exponents no longer can: q-Gaussian with q ≳ 2 under adiabatic drive, Gaussian (BTW) or
exponential (Manna) once overloaded.

**Why this is not already embodied.** `mesh-criticality` carries seventeen lenses — `--shape`,
`--crackling`, `--complexity`, `--dynrange`, `--suscept`, `--fisher`, `--coherent`, `--margin`,
`--hurst`, `--coarse`, `--dtc`, `--aging`, `--allometry`, `--taylor`, `--levels`, `--separability`,
`--equifinal` — plus the m̂ MR estimator. Every one reads the board **event stream**: avalanche sizes,
durations, inter-arrival ordinal patterns, autocorrelation slope. Dragon-kings (line 201), Griffiths
phases, quasicriticality, the Widom line and self-organized bistability are all already in there
(checked, `grep`). **Cycles are not**, and neither is the drive rate as a conditioning axis. Nothing
reads a configuration/stress variable at all.

---

## Applying it produced the finding, and the finding is a live defect

The first question the paper asks of a system is *does the stream carry cycles*. Asked of our board,
the answer is yes and it is enormous — and the lens we own for exactly this question says the
opposite.

**Measured on `~/.mesh/chat.log`, 3001 events / 76.0 h (2026-08-17T16:45Z → 2026-08-20T20:40Z):**

| statistic | value | uniform-phase expectation |
|---|---|---|
| events on a minute divisible by 5 | **29.6 %** | 8.3 % |
| events on a minute divisible by 15 | 12.9 % | 6.7 % |
| χ² of minute-of-hour vs uniform | **1459** on 59 df | 59 ± 11 |

The board is a cron comb — unsurprising, this node's crontab holds 276 lines. Yet the live lens reads:

```
criticality complexity-entropy: MEMORYLESS-POISSON-LIKE (intervals=622, d=3; H=0.992 C=0.008 …)
  White-noise corner = H→1,C→0 (memoryless timing → any board power-law is a coincidence,
  criticality hollow); … low H = REGULAR (a fixed-cadence reflex dominating).
```

### Why it says that, driven at the real function

`cecp_classify()` (`mesh-criticality:1190`) computes Bandt–Pompe ordinal patterns over the
inter-arrival intervals, ties broken by index (`:1175`). Ordinal patterns are the **rank order** of
consecutive intervals — the transform discards absolute phase. A perfect cadence has near-**constant**
intervals, so the rank order is decided by **jitter alone**, and the pattern distribution goes uniform.

Driving the real `cecp_classify()` with a flawless `*/15` cadence on this board's 1-second timestamps,
varying nothing but the jitter:

| jitter (s) | adjacent-interval ties | H | verdict |
|---|---|---|---|
| 0 | 100 % | −0.000 | REGULAR |
| 0.4 | 65 % | 0.656 | CORRELATED |
| 1 | 26 % | 0.946 | **MEMORYLESS-POISSON-LIKE** |
| 2 | 13 % | 0.982 | MEMORYLESS-POISSON-LIKE |
| ≥ 15 | ~0 % | 1.000 | MEMORYLESS-POISSON-LIKE |
| *control:* true Poisson | — | 1.000 | MEMORYLESS-POISSON-LIKE |

**The `REGULAR` branch — whose entire documented purpose is "a fixed-cadence reflex dominating" — is
reachable only at EXACTLY zero jitter.** Above ~0.3 s on a 900 s period (0.04 %), a clock is reported
at the white-noise corner, under a rendered sentence that reads *"memoryless timing → any board
power-law is a coincidence, criticality hollow"*. At 0.4 s it passes through **CORRELATED**, i.e. a
clock can be labelled SOC-plausible temporal memory. H is a pure function of the tie fraction, and the
tie fraction is set by jitter relative to **timestamp resolution** — so the verdict is a property of
the clock's precision, not of the dynamics.

### The shape

The author avoided this trap one step earlier and walked into it (`:1160`): binned counts were
explicitly rejected as *"zero-inflated small integers (heavy ties → ordinal patterns ill-defined)"*
and intervals chosen because at second resolution they are *"near-continuous"*. But **second
resolution does not rescue a cadence into signal — it randomises it into pseudo-noise.** The
discreteness did not go away; it moved into the tie-break, where it now manufactures the white-noise
corner instead of an obvious degeneracy. *A transform chosen to escape ties is not thereby a
transform that reads structure; a fixed cadence is the tie-heaviest series there is.*

And the branch was green because **its only fixture is a monotone ramp** (`:3372`, intervals
1, 2, 3, 4 …) — a strictly increasing series, the one other thing that reaches H→0. The fixture never
contained a cadence, so the prose claim ("a fixed-cadence reflex dominating") was never once
exercised. Sibling of `a-fixture-missing-both-preconditions-asserts-neither-guard` and of
`asserting-an-alpha-gate-never-fires-asserts-it-has-no-size`.

---

## The landing

`scripts/mesh-criticality`:

- **`_phase_lock(times)`** — circular concentration R = |mean e^{2πi·t/p}| over event epochs for
  p ∈ {60, 300, 900, 1800, 3600} s, verdict on the Rayleigh z = R√n (≈1 under uniform phase, so a
  quiet window cannot manufacture a lock). Measures the axis the ordinal transform discards, in the
  domain it discards it in. Returns `None` below n = 30 — **untested phase is not "unlocked"**.
- **CECP verdict qualified, never overridden.** The ordinal label stands as computed: it is a correct
  statement about ordinal memory. What is added is `rendered`, `phase`, and a paragraph on the
  `--complexity` line so no reader can take *memoryless* for *no structure*.

Live, on the real board: `MEMORYLESS-POISSON-LIKE [PHASE-LOCKED 60s R=0.38 z=9.5]`.

**Gate seen RED four ways** (`--test`):

| mutation | result |
|---|---|
| pre-patch code at git HEAD, gate grafted on | `FAIL … got phase=None label=MEMORYLESS-POISSON-LIKE H=0.998` — the defect, verbatim |
| detector never fires | `FAIL … got phase={'p': 900.0, 'R': 0.974, 'z': 19.5, 'locked': False}` |
| detector always fires | `FAIL (a memoryless Poisson stream must NOT be flagged … got z=1.7)` |
| qualifier never reaches the rendered string | `FAIL (the lock must reach the RENDERED string a reader sees)` |

The cadence measures z = 19.5 against the Poisson control's z = 1.7 — an order of magnitude of
separation, which is why a 3.0 threshold is not a tuned number. `--test` and `alarm-test` both green
after. The gate also fails **forward**: if a future change ever makes a jittered cadence read
`REGULAR`, the first assertion fires and tells the reader to re-derive this note, so the documentation
cannot outlive the behaviour it describes.

---

## What is proposed and NOT done

**A cycle lens, and the drive-rate axis.** Tadić et al.'s actual contribution — cycles in the stress
variable, and the loss of avalanche scaling above a critical drive rate — is still unbuilt. Two
concrete pieces, both on `scripts/mesh-criticality`:

1. **`--overdrive`**: condition every avalanche lens on the drive rate. The paper's overloaded regime
   grows a right-tail bump in the size distribution — **the same signature our dragon-king lens
   (`:201`) reads as endogenous.** Same shape, two causes, and we own a lens that names one
   confidently. Until the drive rate is a measured axis, a dragon-king verdict here cannot exclude
   plain overload.
2. **First-return of the outflow current** as the discriminator that survives when scaling is lost.

**Attempted and honestly negative — the naive sandpile mapping does not hold on the board.** Reading
`[task]` as grains added and `[done]` as grains leaving gives 0.44 vs 1.56 per 15-min bin: the pair is
**unconserved by 3.5×**, and the cumulative "pile height" runs to **−340** over 76 h, because most
`[done]`s close work never posted as a `[task]`. Sandpile SOC's correspondence to an absorbing-state
transition rests on bulk conservation, so a stress variable built this way is not a pile height and
any lens assuming it is would read a manufactured trend. The configuration variable, if we want one,
has to come from `mesh-promises`' ledger, not from board marker counts.

**And the first-return discriminator is currently unavailable, for a reason worth recording.** Run on
the settlement stream against a Poisson control at matched rate:

| series | bin | mean/bin | excess kurtosis of Δ | Poisson 95 % band |
|---|---|---|---|---|
| `[done]` outflow | 15 min | 1.56 | 0.12 | [−0.40, +1.24] → **inside** |
| `[done]` outflow | 1 h | 6.24 | 0.63 | [−0.80, +1.27] → **inside** |
| `[done]` outflow | 3 h | 18.23 | −0.54 | [−1.22, +1.51] → **inside** |
| all board events | 15 min | 9.87 | 4.50 | [−0.51, +1.01] → above |
| all board events | 1 h | 39.49 | **0.03** | [−0.87, +1.54] → **inside** |
| all board events | 3 h | 115.42 | 2.24 | [−1.17, +1.21] → above |

The outflow is inside the counting-noise band at every width — a near-Gaussian first-return at ~1.5
counts/bin is what Poisson counting gives under *any* dynamics, so reading it as "Gaussian ⇒ the
overloaded regime" would have measured the counting, not the mesh. Without the control arm it would
have looked like a finding. **And note the all-events row: heavy at 15 min, flat at 1 h, heavy again
at 3 h.** A genuine scale-free heaviness does not vanish at one width and return at the next; a 1-hour
bin aliases an hourly cron comb flat. That non-monotonicity is the same phase structure the new probe
now names, arriving through a second door — which is the only reason it is quotable rather than a
lead.

## Sources

- [Tadić, Shapoval & Shnirman — Self-organised dynamics beyond scaling of avalanches: cyclic stress fluctuations in critical sandpiles (arXiv:2403.15859)](https://arxiv.org/abs/2403.15859)
- [Dragon kings in self-organized criticality systems (arXiv:2308.02658)](https://arxiv.org/pdf/2308.02658) — checked; already embodied at `mesh-criticality:201`
- [Activated random walk exhibits self-organized criticality (arXiv:2605.00207)](https://arxiv.org/abs/2605.00207) — first proof that a model exhibits the conjectured SOC behaviour; no mesh-actionable mechanism, noted not landed
- [Beware of What Lies Beyond the Power Law: Predicting "Dragon King" Failures in Complex Spatial Economic Networks](https://link.springer.com/article/10.1007/s11067-026-09732-3)
