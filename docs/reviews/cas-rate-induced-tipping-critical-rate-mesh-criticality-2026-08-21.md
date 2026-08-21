# Complex adaptive systems / edge of chaos (live review): **rate-induced tipping** — the mesh's tipping lens has no time in its denominator

**Date:** 2026-08-21
**Area:** complex adaptive systems & the edge of chaos (Santa Fe lineage), from the angle of an
**OPERATIONAL mechanism we could implement**.
**Landing:** a mechanism we do NOT embody — **rate-induced tipping (R-tipping)** and its **critical
rate**, i.e. failure that occurs *without any threshold being crossed*, from a live and still-moving
literature (a framework paper posted **nine days ago**).
**Verdict:** concept ACCEPTED as new and load-bearing. **LANDED as code** — `scripts/mesh-criticality
--rtip`, read-only, no alarm (uncommitted, for the steward). Live measurement below.

## The sources

1. Paul Ritchie, Hassan Alkhayuon, Peter Cox & Sebastian Wieczorek, **"Rate-induced tipping in
   natural and human systems"**, *Earth System Dynamics* **14**:669–683 (2023),
   doi:10.5194/esd-14-669-2023. <https://esd.copernicus.org/articles/14/669/2023/>
   > "an instability that occurs when external conditions vary faster … than some critical rate,
   > usually **without crossing any critical levels (bifurcations)**."
2. Paul Ritchie & Jan Sieber, **"Early-warning indicators for rate-induced tipping"**, *Chaos*
   **26**:093116 (2016), arXiv:**1509.01696**. <https://arxiv.org/pdf/1509.01696> — the warning
   signal is **tracking failure against the moving quasi-equilibrium**, not loss of local stability.
3. Peter Ashwin & Sebastian Wieczorek et al., **"Rate-induced tipping: thresholds, edge states and
   connecting orbits"**, *Nonlinearity* (2023), doi:10.1088/1361-6544/accb37 — the critical rate
   `r_c` is *the rate at which tracking errors cross the distance to basin boundaries*.
4. **Live continuation, read while searching:** Juan Nathaniel, Carla Roesch, Derek DeSantis,
   Parvathi Kooloth, Hang Fan, Valerio Lucarini, Anastasia Romanou & Pierre Gentine, **"Koopman
   early warning signals for bifurcation and rate-induced tipping"**, arXiv:**2608.14716**,
   submitted **12 Aug 2026**. <https://arxiv.org/abs/2608.14716>
   > "most indicators rely on the notion of critical slowing down and **do not generally extend to
   > rate-induced tipping**"

The 2026 paper is the reason this counts as *live* literature rather than a fixed reading list: the
open problem it states is exactly the hole in our organ, and its own answer (residual Koopman mode
decomposition) is heavier than we need — we take the *criterion*, not their estimator.

## Why this is not already embodied

`scripts/mesh-criticality` is ~5.5k lines carrying ~20 sidecars. Sorted by what they read:

| lens | reads |
|---|---|
| `m̂`, `regime`, `--margin`, `--suscept`, `--dynrange`, `--widom` | a **level** |
| `--drift` (Δm over the tape), `csd_classify` (Δvar, Δac1 between tape halves) | a **level difference** |
| `--shape`, `--crackling`, `--hurst`, `--complexity`, `--compress`, `--coarse`, `--aging`, `--taylor`, `--allometry` | an **arrangement / exponent** |

**Not one of them divides by elapsed time**, and the two tape readers prove it in code:
`csd_from_tape` and `drift_from_tape` both `re.search(r'm̂=([0-9.]+)')` over a **dated** tape and
throw the timestamp away — the trend tape is a time series consumed as an unordered sequence.

There are five occurrences of "tipping" in the file and all five sit in the CSD block, which is
**bifurcation-induced tipping by construction**: CSD is the signature of an equilibrium *losing
stability*. In R-tipping the quasi-equilibrium **persists mathematically** and is simply outrun. So
this is not a missing knob on an existing axis; it is a missing axis, and CSD cannot be tuned into
covering it.

## The mechanism, in quantities the tool already computes

    margin       d = 1 − m̂                    (--margin's own distance to the basin boundary)
    relaxation   τ = −BIN_S / ln m̂            (branching-process autocorrelation time, since r_k = m^k)
    drive rate   r = |Δm̂| / Δt                (from the tape's OWN timestamps — new)
    tracking lag L = r · τ
    RATE RATIO   ρ = L / d                    (ρ ≥ 1 is Ashwin–Wieczorek's criterion)

**The part `--margin` structurally cannot say.** Near `m̂→1`, `τ ≈ BIN_S/d`, so

    ρ ≈ r · BIN_S / d²

The **safe rate falls as d², not as d.** A drive that is comfortable at `d = 0.5` is **25× over
critical** at `d = 0.1` *with the rate unchanged* — so "the drive has not gone up" is not a defence,
and a lens reporting `d` alone cannot express it.

**Honesty on the exponent:** `d²` is the *linear* tracking-lag argument (first-order relaxation
toward a ramped equilibrium), which is the regime this tape is read in. Nonlinear fold analyses give
other exponents. The code publishes it as the modelling choice it is, never as a measured law.

## The confound that had to be cleared first

A rate over a **noisy estimate** is mostly the estimator. Each `m̂` is an MR regression off whatever
board activity its window carried, so consecutive tape readings jitter for reasons unrelated to
drive — the same unknown-η confound `--dtc` already names for CSD, arriving on the **numerator**
instead of the variance.

So `ρ` is not read as a verdict until the rate is shown to be a *drive*. The test is an
**exchangeability surrogate**: shuffle the tape's `m̂` **values** while keeping the observed `Δt`
sequence, recompute the mean step rate. Under pure estimator jitter the ordering is exchangeable, so
observed ≈ surrogate. Observed significantly **below** the surrogate band means consecutive readings
are more alike than chance — real temporal structure, rate readable.

## Live measurement (this node, 2026-08-21)

Tape `~/.mesh/criticality.cron.log`, **1074 rows** (961 finite), **885 usable pairs**, cadence
self-calibrated to **1800 s**; excluded and counted: 173 `n/a`, 15 gap > 3× cadence, 298 `m̂ ≥ 1`
(no relaxation time — owned by the SUPERCRITICAL alarm).

    drive  2.10e-04 /s   vs  exchangeable surrogate  3.64e-04 /s  (p05 3.37e-04)  → rate RESOLVED
    ρ = lag/margin:  median 0.28    q90 7.84    frac(ρ ≥ 1) 0.29
    verdict: RATE-TIPPING

Read it carefully:

- The rate **is** resolved here — observed is 42 % below chance, outside all 400 surrogates. This
  board's `m̂` really does drift; it is not all jitter.
- **Median ρ = 0.28** — most of the time the board tracks its own drive comfortably. The axis
  discriminates; it is not a railed constant dressed as a measurement.
- **frac(ρ ≥ 1) = 0.29** — about a third of 30-minute steps have the tracking lag **exceeding the
  safety margin**, while `--margin` and the `m̂` band read normally. That is the R-tipping-susceptible
  fraction, and until today nothing in the mesh could see it.

## What landed

`scripts/mesh-criticality --rtip` (uncommitted, in-tree):

- `_rtip_tape_rows()` — the **only** tape reader here that keeps the timestamp.
- `rtip_classify()` — cadence **self-calibrated** from the tape's own median Δt (never a hardcoded
  1800; the cron cadence has been re-paced before and a constant would rot silently).
- Three exclusions, each in its **own counter and printed**, because each is a bias term: `m̂=n/a`
  rows (an honest empty read, never coerced to 0); pairs straddling a gap > 3× cadence (**a rate
  across an outage straddles the change instant** — an hours-long gap divided into a jump of 0.7
  manufactures a comfortingly small rate for a transition nobody observed); `m̂ ≥ 1` pairs (no
  quasi-equilibrium to track — substituting a τ there would fabricate a tracking claim about a
  runaway).
- Verdicts: `TRACKING` / `RATE-STRESSED` / `RATE-TIPPING` / `NOISE-DOMINATED` / `INSUFFICIENT`.
  Read-only. **No alarm, no board post, never touches `m̂`, `regime` or the alarm gate.**

### The gate, and it was seen RED

Real-read arithmetic over **mktemp tape fixtures** — never the live trend tape (a `--test` that
writes or reads the durable liveness record forges the evidence it exists to check). Six legs, each
broken on purpose and watched fail before being restored:

| broken | went red with |
|---|---|
| `τ ← flat bin` | ρ arithmetic — median 0.0417 vs hand-computed 0.4997 |
| gap exclusion removed | the 6× cadence gap pair must be excluded and counted, got 0 |
| `n/a` coerced to 0 | the two pairs touching the `m̂=n/a` row … got 0 |
| `m̂ ≥ 1` folded in | the m̂≥1 pair has no relaxation time … got 0 |
| surrogate always passes | a tape that is all step and no drift must NOT be read as a drive |
| `frac_hi ← 1.01` | a fast drift at a narrow margin must reach RATE-TIPPING — an unreachable top band is a dead axis |

The median ρ is asserted against a value hand-derived **outside** the function, so the gate is an
assertion and not a re-run. The top band is asserted **reachable** so it cannot become a dead label.

## What was NOT claimed

- No alarm wiring. The lens is read-only pending real-mesh vetting, like every sidecar here.
- No claim that `d²` is this system's measured exponent — only that it is the linear-tracking
  estimate and that the *direction* (safe rate collapses super-linearly as the margin narrows) is
  the operational content.
- `frac(ρ ≥ 1) = 0.29` is **this tape, this window**. The tape is append-only but the verdict is a
  windowed reading and must be re-derived, never quoted.
