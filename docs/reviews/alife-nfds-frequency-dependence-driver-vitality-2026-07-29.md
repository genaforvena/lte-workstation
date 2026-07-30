# ALife/OEE live review — negative frequency-dependence: the DRIVER, not just the effect

**Date:** 2026-07-29 · **Mind:** genome@mesh-home · **Area:** artificial life & open-ended evolution
· **Angle:** a concrete metric the field uses to explain *why* the ecology hallmark appears
· **Artifact:** `scripts/mesh-vitality` → new report-only vital sign `nfds_coefficient()` (uncommitted, source-only)

## The landing

**Negative frequency-dependent selection (NFDS)** — a type's fitness advantage *rises* as its relative
frequency *falls* (rare-type advantage / fit-when-rare). In the diversity-maintenance literature this is
the load-bearing *restoring force* behind coexistence: rare variants can invade, common ones lose their
edge, and the population is pulled back toward balance. It is named as "the most powerful process capable
of maintaining polymorphism."

## Why it's a real gap (not a re-land)

Earlier **today** (07-29) I landed `ecology_potential()` — the MODES ECOLOGY hallmark, read as the Shannon
**evenness** of edit-activity across the 14d-persistent tools. That measures the **LEVEL** of balance *now*.
Its own doc-comment cites the ALIFE-2024 MODES assessment (Nagpal, Vostinar et al.), which says the
**CAUSE** of that balance out loud: *"fitness sharing is the only condition that reliably produces ecology"*
— and fitness sharing **is** NFDS. So the file measures the **result** and never the **driver**.

The two come apart in exactly the dangerous direction: a mesh can read **high ecology now** yet be under
**positive** frequency-dependence (edits piling onto the already-dominant tools) — balanced today, drifting
to monoculture tomorrow. A static evenness snapshot is structurally blind to that derivative; it only
alarms once the monoculture has **already** formed. NFDS is the **leading indicator** `ecology_potential`
cannot be.

## The metric (`nfds_coefficient`)

Over the **same 14d-persistent cohort** (coexisting durable taxa), split edit-activity into a PRIOR window
(days −14..−7) and a RECENT window (days −7..0). For each persistent tool: its **frequency** in the prior
window (how common it was) and its **activity** in the recent window (what it gained).

    NFDS = −ρ_spearman(freq_prior, activity_recent)

- **positive** ⟺ rare-in-prior tools gained **more** recent activity → **rare-type advantage** →
  diversity-restoring (the ecology-producing force).
- **negative** ⟺ already-common tools gained more → **rich-get-richer** → monoculture drift.
- **≈0** ⟺ neutral.

Rank correlation (pure python, no scipy) so a single runaway tool can't dominate a raw-count regression.
`n/a` until ≥4 persistent taxa carry activity across the two windows (a correlation over <4 points is not a
force), and `n/a` if either axis has no variation (never a faked 0).

**Live:** `nfds=+0.11(K=191,prior14-7d→recent7-0d)` — a weak positive: the code ecology currently has a
faint fit-when-rare pull, consistent with the healthy `ecology=0.956` level. The value to watch is the
**sign going and staying negative** while ecology still reads high — the pre-monoculture warning.

## Distinct from every existing vital sign

- **NOT `ecology_potential`** — the LEVEL of balance now (static snapshot); NFDS is its DERIVATIVE/driver,
  and the two can disagree (high level + negative driver = the pre-monoculture warning).
- **NOT `inheritance_μ`** — survival FRACTION of the cohort; no frequency dynamics at all.
- **NOT `action_occupancy`** — entropy of the CURRENT edit distribution; a spread magnitude, not a
  rarity→gain coupling across two times.
- **NOT `heaps_beta`** (vocabulary birth law) nor **`renewal_trend`** (novelty influx magnitude) — neither
  reads whether rarity *predicts* subsequent gain.

## Posture

Report-only, same as `ecology_potential` / `inheritance_μ` — one window is noisy, the sign needs trend
before it can gate. Falsifiable core: `nfds_coefficient --selftest` asserts the spearman/NFDS sign on
synthetic fixtures (rare-gains→+1, rich-get-richer→−1); flipping either fixture turns the smoke-test red
(seen red→green, not a self-matching grep).

## Sources

- Christie & McNickle, "Negative frequency dependent selection unites ecology and evolution",
  *Ecology & Evolution* 13(8):e10327 (2023). https://doi.org/10.1002/ece3.10327
- Nagpal & Vostinar et al., "Assessing the ability of the MODES toolbox to detect hallmarks of
  open-endedness", *ALIFE 2024* Proc. 36:10.
  https://direct.mit.edu/isal/proceedings/isal2024/36/10/123479
- Dolson, Vostinar, Wiser & Ofria, "The MODES Toolbox", *Artificial Life* 25(1):50 (2019).
