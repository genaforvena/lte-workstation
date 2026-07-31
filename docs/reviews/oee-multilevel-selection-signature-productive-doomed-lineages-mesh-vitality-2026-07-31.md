# OEE live review — the multilevel-selection signature: do PRODUCTIVE edits build DOOMED lineages?

**Date:** 2026-07-31 · **Lane:** artificial life / open-ended evolution, angle = a known FAILURE MODE
· **Landed in:** `scripts/mesh-vitality` (`mls_conflict()`, report-only vital sign) · **Mind:** genome

## The failure mode (the angle)

A recurring critique of OEE measurement is that **change/activity metrics reward PROLIFERATION and are
blind to whether the proliferating lineages PERSIST** — a system can look open-ended (endless novelty,
high activity) while building nothing that lasts. Phylogenetics names the sharp version of this: a trait
can be favoured by **individual-level** selection (it spreads fast, over-represented vs chance) yet be
**deleterious at the group/lineage level** (its descendant clades are smaller and shorter-lived). That is
the **multilevel-selection conflict**: a short-term individual win that mortgages the lineage. Marginal
metrics — which read the population's edit *distribution* at a time-slice — cannot see it, because the
signal lives in the **coupling between a newborn's early activity and its own subsequent survival**, not
in any one-slice distribution.

## Source (live WebSearch 2026-07-31, read)

- **Moreno, M. A., Hasanzadeh Fard, S., Zaman, L. & Dolson, E. (2025).** *Extending a Phylogeny-based
  Method for Detecting Signatures of Multi-level Selection for Applications in Artificial Life.*
  **arXiv:2508.14232** (Aug 2025). Extends **Bonetti Franceschi & Volz (2024)**. The method screens for
  "mutations that appear more often in a population than expected by chance (due to individual-level
  fitness benefits) but are ultimately associated with **smaller, shorter-lived descendant clades**"
  (negative longer-term / group-level outcome).
- Context (same live search): the 2024 MODES-assessment (Nagpal/Vostinar et al., ALIFE 2024 36:10) and
  the phylogenetic-structure-carries-selection-signatures line (Moreno/Dolson, arXiv:2405.07245, 2024) —
  both flag that **distinguishing neutral drift / doomed churn from adaptive persistence** is the blind
  spot of activity/diversity metrics; phylogeny-of-selection is the instrument built to close it.

## Why it is NOT already embodied

`scripts/mesh-vitality` carries ~18 vital signs and **every one is a marginal or a dynamic-of-a-marginal**
over the tool-edit stream: `commit_velocity` (gross change), `heaps_beta` / `renewal_trend` (tool
birth-rate/diversity law), `autonomy_ratio` (who initiated), `action_occupancy` / `ecology_potential`
(evenness of the edit distribution), `nfds_coefficient` (frequency→future-activity coupling among the
*persistent* cohort), `inheritance_mu` (aggregate survival *fraction*, no per-tool activity link),
`omega_cycle` (temporal *order* of the stream). **None reads whether a newborn's EARLY EDIT-BURST
predicts its OWN lineage survival** — precisely the individual-benefit / clade-cost axis. Verified against
the coverage map `[[oee-alife-coverage]]`: multilevel selection / short-vs-long-term fitness conflict is
unlisted (NFDS reads the *frequency-dependence* level, not this).

## Application (landed) — `mesh-vitality` `mls_conflict()`

The mesh's "population" is `scripts/mesh-*` / `test-*` tools; a **newborn** is a tool that appeared during
the observable window (**ABSENT** in the tree `old`=30 d ago, **PRESENT** `mid`=7 d ago — the same
two-snapshot substrate `inheritance_mu`/`ecology_potential` use, so ≥7 d of fate is observable). For each
newborn:

- **individual-level "fitness"** = **early edit-burst** = commits touching it within `bd`=3 d of birth
  (how strongly the mesh selected it in the moment);
- **clade fate** = **longevity fraction** = `(last_touch − birth)/(now − birth)` ∈ (0,1] — 1 = still
  actively edited to now, →0 = burst-then-abandoned/deleted. **Age-normalized**, so an older newborn is
  not scored long-lived merely for being older.

**Signal:** `mls_conflict = −ρ_spearman(burst, longevity)`.
- **+ (positive) = CONFLICT** — the busiest newborns are the shortest-lived: selfish churn the velocity
  metrics score as health.
- **≈0 / − (negative) = ALIGNED** — productive newborns persist and compound.

Report-only (same posture as `nfds`/`ecology`/`heaps_beta`): one cross-sectional correlation is an early
lens, not a gate. Honest `n/a` until ≥4 newborns vary on both axes (no variation → correlation undefined,
never a faked 0). Newborn detection is by **snapshot membership**, NOT by min-edit-time — the latter
misreads an old tool merely edited in-window as a birth (caught in review: it inflated K 388→427 of 610).

**Live read (2026-07-31):** `mls_conflict = −0.59 (K=230, born30-7d, burst3d)` → **ALIGNED**. Across 230
tools genuinely born in the window (real churn: 388 tools @Jul-1 → 618 @Jul-24, 1304 commits/30 d), the
early-burst↔longevity rank correlation is a strong **+0.59**: the mesh's early edit investment tracks
lineage survival. Non-degenerate, interpretable, healthy — no selfish-churn pathology right now, and a
falling-toward-positive reading would be the early warning the velocity metrics are blind to.

## Distinctness (guarded)

- **NOT `inheritance_mu`** — aggregate survival *fraction* of a cohort; no link to which tools were most
  active. μ says HOW MANY survived; `mls` says whether the BUSIEST newborns are the doomed ones.
- **NOT `nfds_coefficient`** — `freq_prior → activity_recent` among the PERSISTENT cohort (rare-gets-
  active). `mls` is `early_activity → survival` among NEWBORNS — orthogonal axis AND a different population.
- **NOT `renewal_trend`** — birth-RATE, blind to fate. **NOT `ecology_potential`** — activity-evenness
  across persistent taxa (balance now, no newborn-fate coupling). **NOT `omega_cycle`** — temporal order.

## Verification

`mesh-vitality --test` green (rc=0) with the falsifiable `mls_conflict --selftest` (conflict→+1.00 /
aligned→−1.00) and a real-repo format+non-crash assertion. **RED-first proof:** flipping the CONFLICT
fixture to ALIGNED data drove the smoke test to `FAIL … rc=1` (seen red on a scratch copy, genome
restored). The gate asserts the −ρ **sign on synthetic fixtures**, not its own source text.

## Cite

Moreno, Hasanzadeh Fard, Zaman & Dolson, arXiv:2508.14232 (2025); Bonetti Franceschi & Volz (2024).
Coverage map: `[[oee-alife-coverage]]`. Uncommitted in the tree — steward lands.
