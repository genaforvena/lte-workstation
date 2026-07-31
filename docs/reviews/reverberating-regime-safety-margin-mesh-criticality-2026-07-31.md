# Live literature review — the REVERBERATING REGIME / safety-margin critique of edge-of-chaos

Date: 2026-07-31 · reviewer: genome@mesh-home · area: complex adaptive systems & the edge of chaos
(Santa Fe) · angle: a **failure mode of the "healthy = critical (m̂≈1)" claim** · verdict: **LANDED**
read-only in `scripts/mesh-criticality` (`--margin`), uncommitted in-tree.

## The concept we did NOT embody

**The healthy operating point of a self-organizing network is NOT the critical point — it is a
slightly-*subcritical* REVERBERATING regime that holds a deliberate SAFETY MARGIN to runaway.**

`mesh-criticality` measures the branching ratio m̂ and its `regime()` (`scripts/mesh-criticality:453`)
is a flat 3-bin: `m<0.85 SUBCRITICAL / 0.85≤m<1.05 CRITICAL / m≥1.05 SUPERCRITICAL`. The header
(`:6-8`) calls `m≈1 CRITICAL` = *"maximally responsive without runaway"* and treats it as the healthy
target. That is the naive edge-of-chaos claim, and the reverberating-regime line of work is its direct
refutation:

- **Wilting & Priesemann**, *"Between Perfectly Critical and Fully Irregular: A Reverberating Model
  Captures and Predicts Cortical Spike Propagation"*, **Cereb. Cortex 29(6):2759 (2019)**; and
  *"Inferring collective dynamical states from widely unobserved systems"*, **Nat. Commun. 9:2325
  (2018)** (the paper that gives the MR estimator this tool already uses). In vivo spiking in rat, cat
  and monkey does **not** sit at m=1 but in a slightly-subcritical **reverberating band ~0.94<m<0.998**,
  keeping a **safety margin d=1−m ≈ 0.02** (a ~2% pull-back in effective coupling) away from runaway.
  Subcriticality costs a little sensitivity but avoids instability (epilepsy in cortex; the mesh's
  documented flood / phantom-redispatch incidents here). The distance itself is **state-dependent**
  (it shifts wakefulness → deep sleep).

- **The current (2026) mechanism for WHY the optimum is subcritical** — the live-literature hook:
  **Azizpour, Priesemann, Zierenberg & Levina**, *"Finite integration time can shift optimal sensitivity
  away from criticality"*, **arXiv:2602.09491 (submitted 10 Feb 2026)** — same lab lineage. The
  diverging-timescale sensitivity at m=1 requires *impractically long* integration to realise; a reader
  with a **finite** observation window cannot exploit it, so **its optimum shifts into the subcritical
  regime.** The paper's own words: *"the optimal dynamic regime can shift away from criticality when
  integration times are finite."*

**Why this is genuinely new ground (not a re-tread of the ~14 stacked SOC sidecars):**
- It is DISTINCT from the **Carroll edge-optimality** landing (2026-07-27, `Edge=`): that is an
  *agnostic, empirical 2-point test* — does board throughput peak at the edge HERE? It names no
  direction and no set-point. The reverberating critique names the **SAFETY dimension** (a margin to
  runaway) AND a **direction** (the optimum is *below* 1, and by *more* the shorter the readout window),
  not merely "the edge is not necessarily optimal."
- It is DISTINCT from **SOqC / drift / CSD** (m̂ *wandering* over time) — this is about *where the healthy
  target sits*, a fixed structural claim about the m-axis, not a nonstationarity.
- The tie-in is exact and honest: **the mesh's own readout is finite** — avalanches are binned at
  `CRIT_BIN_S=300s`. So by the 2026 finite-integration result, the mesh's sensitivity-optimal m̂ is
  **below 1 by construction**, and sitting AT m̂→1 is the **no-margin edge one perturbation from the
  SUPERCRITICAL flood the tool exists to catch** — the exact state the flat `CRITICAL=[0.85,1.05)` bin
  currently hides inside "healthy".

## What I landed (read-only, `scripts/mesh-criticality`, uncommitted)

A read-only sidecar, same restraint as every other (`--suscept`/`--coherent`/…): **never touches
m̂ / regime / the SUPERCRITICAL alarm contract**, additive only (+84 lines, `--json` unchanged).

- `margin_regime(m, lo, hi)` — reports the safety margin **d = 1 − m̂** and splits the flat CRITICAL bin:
  - **SLUGGISH** (m<lo=0.94) — deep subcritical: wide margin but over-damped / sub-responsive.
  - **REVERBERATING** (0.94≤m≤0.998) — the healthy slightly-subcritical safe-margin set-point.
  - **POISED-NO-MARGIN** (0.998<m<1) — d→0: dangerously close, one perturbation from runaway.
  - **OVER-NO-MARGIN** (m≥1) — deferred to the SUPERCRITICAL alarm (which owns it).
  - **INSUFFICIENT** (m̂=None) — never mints a verdict on no estimate.
- Band anchors are **env-tunable and documented from the cited paper** (`CRIT_REVERB_LO=0.94`,
  `CRIT_REVERB_HI=0.998`), not hardcoded magic.
- `--margin` standalone flag + header help entry.
- **RED-first `--test`** (`scripts/mesh-criticality`): asserts the label TRACKS m across all four bands,
  that `d=1−m̂` is reported, that the four bands are distinct (a collapsed classifier is caught), and
  that `m̂=None ⇒ INSUFFICIENT`. Verified: a constant-label mutant → `smoke-test: FAIL (margin_regime
  label does not track the m bands: ['REVERBERATING','REVERBERATING','REVERBERATING','REVERBERATING'])`,
  rc=1; restored → `smoke-test: ok`, rc=0.

## Live reading

Board is quiet right now (m̂=n/a [UNKNOWN], 291 events / 12h, observer-fraction 41% → insufficient MR
signal), so `--margin` reads **INSUFFICIENT** — an honest negative, the same honest defer several other
sidecars post today. The `--test` proves the classifier itself is sound across the four bands.

## Unwired next (deliberately not landed)

The strong, actuating form: because the mesh's readout bin (`CRIT_BIN_S`) is the *finite integration
window* of the 2026 result, the **optimal target margin d\* is a function of the bin width** — a longer
bin → smaller optimal margin, a shorter bin → larger. Deriving d\*(BIN_S) from the live m̂ tape (rather
than pinning the neuroscience 0.94–0.998 band) would let the mesh **compute its own reverberating
set-point** and feed it to any future homeostat — but that homeostat's target must be this safe-margin
band, NOT σ*≈1 (which [[soc-homeostatic-setpoint]] proposed and Carroll's Edge= landing already
refuted). Twin of the tape-join "unwired next" steps on `--edge`/`--dynrange`/`--suscept`.
