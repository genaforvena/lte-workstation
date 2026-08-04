# OEE live review — the NEUTRAL SHADOW MODEL / new adaptive activity (`mesh-vitality`)

**Date:** 2026-08-04 · **Mind:** genome · **Area:** artificial life & open-ended evolution ·
**Angle:** a concrete METRIC / experimental procedure the field measures *itself* by ·
**Artifact:** `scripts/mesh-vitality` → `evo_activity()` (report-only, uncommitted in tree)

---

## The concept we did not embody: the NEUTRAL SHADOW MODEL (a control run)

**Cited, live sources (WebSearch 2026-08-04):**

- **Channon, A. (2024). "A Procedure for Testing for Tokyo Type 1 Open-Ended Evolution."**
  *Artificial Life* **30(3):345–355**, MIT Press — the 2024 OEE special issue. doi:10.1162/artl_a_00430, PMID 38635908.
  Assembles *five* methods into one pass/fail procedure for Tokyo Type 1 OEE ("ongoing generation of
  adaptive novelty and ongoing growth in complexity"), deliberately "isolated from the complexities of
  any particular evolutionary system", and names five open challenges.
  <https://doi.org/10.1162/artl_a_00430>
- **de Pinho, T. & Sinapayen, L. (2026). "A speciation simulation that partly passes open-endedness
  tests." arXiv:2603.01701** (2 Mar 2026) — the procedure *applied*, live. This is the reason the
  review landed here rather than on another 2026 OEE metric: it shows the test **discriminating**.
  <https://arxiv.org/abs/2603.01701>

The mechanism: Bedau & Packard's *evolutionary activity* counts the persistent **use** of a component.
The **shadow model** is the control that says how much of that use **selection** explains. Verbatim from
the ToLSim paper: the shadow is *"a model that is executed in parallel to the real model and mimics it:
each birth in the real model causes a birth in the shadow model and each death in the real model causes
a death in the shadow model"* — but on **randomly selected** components. Identical demography,
selection deleted. Plus **shadow-resetting**: the shadow's population and activity history are reset to
the real model's at every snapshot, so the control cannot drift away from the system it controls for.
Component-**normalized** activity is then `real − shadow`; only components above the normalized
threshold are "adaptively significant"; `A_new = (1/D) Σ` over the **newly** significant ones (their
eq. 21/22, `D = |{i : a_i > 0}|`).

**Why it is a real test:** ToLSim *passes* the raw step (40% of runs show unbounded total cumulative
activity) and *fails* the normalized step — all 20 runs show *"mostly null new activity"*. Their
conclusion: **"ToLSim is not open-ended."** A metric that can say that is worth having.

## The gap it closes here

**Every** vital sign in `mesh-vitality` reads the observed activity distribution with **no null at all**:
`ecology_potential` (evenness), `nfds_coefficient` (freq→activity), `action_occupancy` (entropy),
`omega_cycle` (order), `mls_conflict` (burst→longevity), `inheritance_mu` (survival). Each is a statistic
**of** the real edit stream; none asks what that statistic would read under a mesh with the **same
demography and no selection**.

The file's own 2226 block names half of this ("TOTAL activity is not ADAPTIVE activity") and lands the
MODES persistence filter as the answer. Persistence is necessary and **is not the control** — a durable
core hammered daily persists *and* looks selected under pure incumbency drift. Without a shadow,
"adaptive" is **asserted, never measured**, and the panel can certify rich-get-richer churn as
open-endedness. This is the one axis where the field's answer is literally *a control run*.

## What was built — `evo_activity()` (report-only)

- **Components** = genome tools (`scripts/mesh-*`, `test-*`; same `is_tool` population as `mls_conflict`).
- **Windows**: `EA_NWIN`×`EA_WIN_D` (default 14 × 3d = 42d). The shadow is **reset at every window
  boundary** — Channon's shadow-resetting, transposed: the control always restarts from the real
  system's standing state.
- **Real activity** `r_i(w)` = commits in window `w` touching tool `i`, **birth commit excluded**
  (Bedau: activity is persistent *use*, not creation). Birth = absent from the tree at the window-span
  base — the same two-snapshot substrate `mls_conflict`/`inheritance_mu` use.
- **Shadow**: the same `E(w)` events redistributed by **neutral reproduction** — parent drawn with
  probability ∝ standing abundance (+α=1 immigration): a Pólya-urn / Yule process that **keeps
  rich-get-richer and deletes preference**. Evaluated **in expectation** (the analytic mean the
  replicate average converges to) — same estimand, zero RNG jitter, no seed to shop.
- **Adaptively significant** iff the neutral upper tail `Binom(E, p_i)[X ≥ r_i] < 0.05/D`
  (Bonferroni over the window's active components). `a^N_i = r_i − E·p_i`.
- **`A_new(w)`** = `(1/D)·Σ a^N` over components significant for the **first** time.
- **Verdict** over the recent half: `NEW-ACTIVITY` (majority of windows `A_new > 0` — adaptive novelty
  still arriving) / `DRIED` (none — the ToLSim failure mode: activity continues, only the established
  components carry it).

**Live read (this repo, now):** `evo-activity=NEW-ACTIVITY:0.19(6/7w,adaptive=37)` — 6 of the last 7
windows produced a component crossing the neutral null for the first time; 37 component-windows were
adaptively significant. One recent window read `A_new = 0` (its only significant component had already
crossed), so the axis is not pinned.

## Departure from the paper — measured, not assumed

ToLSim's threshold is *"activity greater than the absolute value of the most negative adaptive
activity"*. On a **diffuse** population (≈600 tools, no dominant incumbent) that bar is roughly the
largest negative deviation ≈ the largest positive one — a coin flip for the top component. It was
implemented **faithfully first**, then the fixture seed was swept:

| seed | pure-neutral-drift fixture, paper's rule | with the binomial tail |
|---|---|---|
| 1, 2, 20260804 | DRIED ✅ | DRIED ✅ |
| 3, 7, 99 | **NEW-ACTIVITY ❌ (false positive)** | DRIED ✅ |

**3 of 6 seeds** false-positive on a stream with *no selection in it at all* — the seed that passed was
the lucky one ([[a-stochastic-gates-threshold-is-a-statistic]]). Replaced with the Bonferroni-corrected
binomial tail against the **same** shadow: **0 of 6** false-positive. The paper's rule is sound for
their small gene-value component set; it does not transfer to a diffuse one.

## Red-first gate (seen fail, then restored)

`--selftest` drives four synthetic streams through **the same `evo_activity` core the real run uses**
(one code path, not a reimplementation), plus a direct `strip_births` assertion for the git-only
birth-exclusion the stream fixtures cannot reach:

| fixture | expected |
|---|---|
| a brand-new tool selected every window | `NEW-ACTIVITY` |
| the **same veteran** taking the burst every window | `DRIED` (adaptive once, never *new* again) |
| pure neutral drift | `DRIED` |
| drift + births reused at the drift rate | `DRIED` |

Mutants run from a **scratch copy** of the file (never the tree), each `bash mesh-vitality --test`:

| mutant | result |
|---|---|
| significance bar removed (`alpha_fw = 1.0`) | **RED** |
| never-NEW-twice filter removed | **RED** |
| shadow ignores abundance (uniform, not drift) | **RED** |
| birth-exclusion removed | **RED** |
| min-window `n/a` guard removed | green — **honest exception**, the guard only fires below 3 usable windows and no fixture reaches that |

Full `mesh-vitality --test`: **green, 3.0s**.

## Weakest joints (stated, not hidden)

1. The shadow controls for **demography + incumbency, not authorship** — one mind grinding one tool for
   a day is "adaptive" to this null exactly as a mesh-wide adoption is.
2. The min-window guard is unexercised (above).
3. `A_new > 0` is easy while the mesh births tools steadily; the axis earns its keep by going **DRIED**
   when production concentrates on the established core — that direction is fixture-proven, not yet
   observed live.

## Distinct from everything already embodied

NOT the MODES persistence filter / `inheritance_mu` (durability, no null) · NOT `ecology_potential`
(evenness of the observed distribution) · NOT `nfds_coefficient` (a direction *within* the observed
data, still no control) · NOT `mls_conflict` (newborn burst→longevity) · NOT `omega_cycle` (temporal
order) · NOT `assembly_sig` (motif reuse in commit subjects) · NOT `mesh-sound-reflex:1550`'s "Bedau
new-activity" (first-seen recipe cells, no shadow, different organ).

**Selection stays with the steward** — report-only, gates nothing.

---

Sources:
- [A Procedure for Testing for Tokyo Type 1 Open-Ended Evolution — Artificial Life 30(3):345–355 (2024), doi:10.1162/artl_a_00430](https://doi.org/10.1162/artl_a_00430)
- [PubMed 38635908](https://pubmed.ncbi.nlm.nih.gov/38635908/)
- [A speciation simulation that partly passes open-endedness tests — arXiv:2603.01701 (2026)](https://arxiv.org/abs/2603.01701)
- [Editorial Introduction to the 2024 Special Issue on Open-Ended Evolution](https://direct.mit.edu/artl/article/30/3/300/123431)
