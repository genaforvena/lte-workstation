# CAS / edge of chaos — the UNKNOWN-NOISE CONFOUND of critical slowing down

**Live review, 2026-08-10.** Area: complex adaptive systems & the edge of chaos (Santa Fe).
Angle asked for: **an OPERATIONAL mechanism it proposes (not just philosophy) we could implement.**
Landed in: `scripts/mesh-criticality` — new `--dtc` sidecar + a CSD-verdict qualifier.
Plus a live defect the landing surfaced: **the m̂ trend tape had no writer.**

---

## The source (live literature, found by web search)

**Brendan Harris, Leonardo L. Gollo & Ben D. Fulcher, "Tracking the distance to criticality in systems
with unknown noise", Phys. Rev. X 14, 031021 (Aug 2024) / arXiv:2310.14791v3.**
Live continuation read while searching: **arXiv:2605.12308** (2026) — in-context nowcasting of a
*relative distance to criticality* from a single observed series, i.e. the same quantity, still being
worked on.

The paper is operational, not philosophical. It screens **>7000 candidate time-series features**
(hctsa) for their ability to track the true distance to criticality μ near a bifurcation, and reports
a specific, measured failure of the two indicators the whole early-warning-signal literature runs on:

| indicator | ρ_μ, noise amplitude η **fixed** | ρ_μ, η **unknown & varying** |
|---|---|---|
| standard deviation / variance | **0.98** | **0.23** |
| lag-1 autocorrelation | **0.97** | **0.48** |
| **RAD** (their new statistic) | 0.93 | **0.93** |

Both classical indicators depend strongly on how hard the system is being kicked. Hold η fixed and
they are near-perfect; let η vary between recordings and they stop measuring distance and start
measuring η.

**The mechanism that fixes it** is the transferable part, and it is model-free:

> increments of the Wiener term scale as √Δt, increments of the deterministic term scale as Δt,
> so for small Δt   **σ(Δx) ≈ η·√Δt**

The standard deviation of the **first-differenced** series is an empirical estimate of the noise
amplitude that is (near-)independent of the distance to criticality. Their headline statistic follows
from it — the **rescaled auto-density**, partitioning at the median (Eqs. 9–11):

```
U = {x_t ≥ x̃},  L = {x_t < x̃}
f_RAD = σ(Δx)·[ 1/σ(U) − 1/σ(L) ]
```

— tailedness of the invariant density, rescaled so η divides out.

## The gap in us

`scripts/mesh-criticality` carries ~20 stacked literature sidecars. Its `csd_classify()` decides
**entirely** on Δvar and Δac1 between the two halves of the m̂ tape — the exact pair the paper
demolishes. Every other sidecar guards something else (Δt granularity, subsampling, drive, modality,
observer fraction, exponent coherence, safety margin, self-affinity). **None estimates η.** The prior
CSD landing (2026-07-05, directional ambiguity / critical speeding up) fixed the *sign* blind spot; it
never touched the *noise* one.

And the confound is live here, not hypothetical: each m̂ is a **regression estimate** off however much
board activity its window happened to carry. A quiet stretch of board followed by a busy one moves
Δvar and Δac1 with the distance to criticality unchanged, and `csd_classify` has no way to know.

## What landed

`scripts/mesh-criticality`: `sigma_diff()`, `rad_stat()`, `dtc_qualify()`, `dtc_from_tape()`, a new
read-only `--dtc` mode, and — because a qualifier that only appears under a flag nobody runs is not a
qualifier — a compact tag appended to the CSD verdict **where it is printed**:

```
CSD=WATCH n=683 Δvar=-2.607 Δac1=0.276 [NOISE-CONFOUNDED: η̂ ×0.20 between halves —
  CSD reads the kicking, not the distance; see --dtc]
```

Verdict is **η̂-ratio across the same halves `csd_classify` already splits**:
`NOISE-STABLE` (ratio inside `CRIT_DTC_ETA_BAND`, default 1.25) / `NOISE-CONFOUNDED` / `INSUFFICIENT`.
Report-only; it never touches m̂, `regime`, or the SUPERCRITICAL alarm, and it never overrules
`csd_classify` — it says whether to believe it. NOISE-CONFOUNDED does **not** mean the CSD verdict is
wrong, it means it is not evidence about distance.

The free-form human note and the new flag are the only render changes; the `--watch` tape line and
`--json` are built on separate paths and are byte-unchanged.

## RAD: implemented, reported, and NOT given a verdict — an honest negative

`rad_stat()` implements Eq. 11 exactly, and `--dtc` prints it. It does **not** carry a verdict, because
the transfer was measured and does not survive at this tape's lengths. Fold normal form
`dx = (−μx − x² − x³)dt + η√dt·ξ`, 16 seeds per condition, 600 samples per half:

- **The η-invariance reproduces cleanly.** Mean RAD moves ≤0.05 between fixed-η and variable-η runs of
  the same μ, while the variance's own dispersion across recordings nearly **6×** (sd 0.020 → 0.117).
  The paper's central claim about RAD is confirmed on this transfer.
- **But it cannot rank a single tape against itself.** RAD's per-recording spread (sd ≈ 0.15) is as
  wide as the whole span it moves across the μ sweep (+0.107 at μ=0.5 → −0.086 at μ=0.05, ≈0.19), and
  the within-series ΔRAD between halves is a coin flip — positive in 6–7 of 16 seeds in **every**
  condition, *including the one where nothing changed*. RAD ranks **pooled** recordings, which is what
  the paper does with it.

So the shipped verdict is the η̂ axis, whose separation is clean — **1.96 ± 0.14** (confounded) vs
**0.97 ± 0.07** (stable) over 16 seeds, no overlap — and RAD is a printed figure with its limits
stated. *Unwired next: pool RAD across nodes' tapes, the setting the statistic was built for.*

## The defect the landing surfaced: a tape with no writer

`--dtc` could not qualify anything, because the verdict it qualifies was **permanently
`INSUFFICIENT`**. Cause:

- every reader defaulted to `~/.mesh/criticality.log`;
- `mesh-autowire` cron-wires this tool as `--watch >> $HOME/.mesh/criticality.cron.log` — its
  convention is `<tool>.cron.log`;
- so **745 m̂ lines** had been accumulating in `criticality.cron.log` since the 2026-07-14 autowiring
  while `csd_from_tape` / `drift_from_tape` read a path nothing ever created.

Both early-warning sidecars in this file — CSD **and** Drift — were dead for four weeks. And they
**said so on every single tape line**: `CSD=INSUFFICIENT n=0 Δvar=n/a Δac1=n/a`, 745 times, printed by
the very reflex whose output was the missing input. Nobody read it as a fault. The file's own header
even names the real path in prose ("~/.mesh/criticality.cron.log, the trend tape") while six code
paths used the other one — the same shape as [[a-self-describing-artifact-with-no-writer]] and
[[a-constant-outlives-its-reader]].

Fix: `csd_tape_path()` resolves to the tape that **exists**, autowire's name first; `CRIT_CSD_TAPE`
still overrides. Both sidecars came live immediately on 683 parsed samples.

## Live, first reading after the revival

```
CSD=WATCH n=683 Δvar=-2.607 Δac1=+0.276     ← dead for 4 weeks, now live
Drift=DRIFT_DOWN Δm=-0.155                   ← also dead for 4 weeks, now live
--dtc: NOISE-CONFOUNDED  η̂=σ(Δm̂) 2.2805 → 0.4672, ratio=0.20, band [0.80,1.25]
       RAD -8.8198 → -1.3717 (Δ=+7.4480, no verdict)
```

The revived CSD verdict's very first live reading is one the noise check says is **not evidence about
distance**: the kicking fell **five-fold** between halves, so a Δvar of −2.61 is the η collapse, not a
change in distance to criticality. The paper's failure mode, caught on the first real sample.

Note the scope boundary: `Drift=DRIFT_DOWN` is **not** covered by this qualifier — drift compares the
*means* of m̂ across halves, and a mean shift is not confounded by η the way a variance is. The
DRIFT_DOWN reading stands on its own and is a separate, now-visible signal worth someone's attention.

## RED-first (a gate you have not seen fail is not a gate)

Two new assertion blocks, five mutants, each run from a scratch copy, each seen `rc=1`:

| mutant | what it breaks | result |
|---|---|---|
| **G** | `CRIT_DTC_ETA_BAND=100` — never confounded | RED (fixture A, η×2.00, read NOISE-STABLE) |
| **H** | `sigma_diff` reads the raw series, not the differences | RED (fixture B's own variance rise, ×2.59, masquerades as a noise change — **the differencing is load-bearing**) |
| **I** | label pinned to `NOISE-CONFOUNDED` | RED (fixture B, a genuine approach at constant η) |
| **J** | tape preference order reverted (legacy first) | RED (with both present, autowire's name must win) |
| **K** | `CRIT_CSD_TAPE` override ignored | RED |

The two DTC fixtures are the same fold normal form from the same seed and **both make `csd_classify`
say `RESILIENCE_LOSS`** — that is asserted first, so the noise flag is provably qualifying something.
A: μ constant, η doubled → must be NOISE-CONFOUNDED. B: μ 0.9→0.05, η constant → must be
NOISE-STABLE. A constant label cannot satisfy both. The tape-path block runs against a **sandboxed
`$HOME`** so it cannot pass by accident off the live node's state. `--test` 0.17s → **0.20s**.

## Also learned, not fixed (scope)

The third prototype condition — μ constant **and** η constant, nothing changing — still made
`csd_classify` print `RESILIENCE_LOSS` on 3 of 5 seeds. That is a *separate* false-positive mode: the
half-split comparison has no significance test at all, so ordinary sampling noise in Δvar/Δac1 clears
the flat `CRIT_CSD_EPS=0.01` threshold. This landing does not fix it (a surrogate/permutation null on
the half-split is the shape of the fix — the same one already applied to `mesh-algedonic`'s MI and
`mesh-cooscillate`'s TE). Named here so it is not mistaken for covered ground.

## Cites

- Harris, Gollo & Fulcher, *Tracking the distance to criticality in systems with unknown noise*,
  Phys. Rev. X **14**, 031021 (2024); arXiv:2310.14791v3. The >7000-feature screen, the ρ_μ collapse
  (0.98→0.23, 0.97→0.48), σ(Δx)≈η√Δt, and RAD (Eqs. 9–11). Found by WebSearch 2026-08-10.
- arXiv:2605.12308 (2026) — in-context nowcast of relative distance to criticality; the live
  continuation of this seam.
- hctsa (Fulcher), github.com/benfulcher/hctsa — where RAD ships as `CR_RAD_1`.

## Files

- `scripts/mesh-criticality` — `csd_tape_path()`, `sigma_diff()`, `rad_stat()`, `dtc_qualify()`,
  `dtc_from_tape()`, `--dtc` mode, CSD-note qualifier, test blocks 8c + 8d. Uncommitted, for the
  steward.
