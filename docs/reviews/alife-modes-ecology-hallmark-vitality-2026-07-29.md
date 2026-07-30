# ALife/OEE live review — the MODES **ecology** hallmark (the one we don't read)

**Date:** 2026-07-29 · **Lane:** artificial life & open-ended evolution, angle = a known *failure mode*
of the field's own measurements · **Landed in:** `scripts/mesh-vitality`

## The critique / failure mode (real, current, citeable)

Open-endedness in ALife is standardly assessed by the **MODES toolbox** (Dolson, Vostinar, Wiser &
Ofria, *"The MODES Toolbox: Measurements of Open-Ended Dynamics in Evolving Systems"*, **Artificial Life
25(1):50, 2019**), which names **four** hallmarks — **change, novelty, complexity, and ECOLOGY**.
Ecological potential is defined as the **Shannon entropy of the abundance distribution of the PERSISTENT
taxa**: a system has ecology when *multiple* lineages simultaneously pass the persistence filter and
coexist in a **balanced** distribution — not one dominant type plus a fringe. Multiple individuals making
it through the persistence filter together is the evidence of coexistence-promoting dynamics.

The failure mode is that **ecology is the hallmark hardest to achieve and most often ABSENT even when the
other three read positive.** The 2024 assessment (*"Assessing the ability of the MODES toolbox to detect
hallmarks of open-endedness"*, **ALIFE 2024 Proc. 36:10**) found across NK-landscape conditions that
**"fitness sharing is the only condition that reliably produces ecology"** (fit-when-rare / negative
frequency-dependence) — change/novelty/complexity rise freely while ecology stays flat. So a
change+novelty+complexity reading **over-claims** open-endedness: a monoculture that churns hard scores
high on every *other* axis, and none of them can see that the durable core is a single dominant type.

## Why this lands somewhere new for us

`mesh-vitality` was already dense on this literature — it embodies **change** (commit_velocity),
**novelty** (renewal_trend / heaps births), **complexity** (path_divergence, MSPD), and even *ecological
INHERITANCE persistence* (`inheritance_μ`). But audit shows the MODES **ecology** *object* itself was
missing:

- `inheritance_μ` is a single **survival FRACTION** of a cohort (μ=1.0 = "all 14d tools survived") — **no
  diversity/balance term**. Verified live right now: **inherit-μ=1.000** while the durable core could be a
  monoculture and μ would not move.
- `action_occupancy` is Shannon entropy over **ALL** recently-edited tools with **no persistence filter** —
  it counts ephemeral/newborn churn as spread. It is the *change* axis, not *ecology*.

Neither reads the MODES ecology object: **the balance of activity across the tools that PASSED the
persistence filter.** μ can be 1.000 and action_occupancy high while every edit lands on 3 tools and 400
persistent survivors sit inert — textbook "no ecology under high change/novelty", invisible to every
existing sign.

## The concrete application (file: `scripts/mesh-vitality`)

New report-only vital sign **`ecology_potential()`**: intersect the persistence-filtered cohort (tools
that existed 14d ago **AND** are still present at HEAD — the *same* filter `inheritance_μ` uses) with the
last-N-commit edit activity, and report the **Shannon evenness** `H/ln K` of the edit-count distribution
over that durable, coexisting-and-active set. `1.000` = activity balanced across many persistent taxa
(rich ecology); `→0` = the durable core is a monoculture a few tools dominate. `n/a` until ≥2 persistent
taxa are active in the window.

Edit-count is an **activity ANALOG** of MODES abundance, not a population census — honest and cheap now,
same report-only posture as `inheritance_μ` / `path_divergence` (one cross-sectional evenness needs a few
runs of trend before it can gate).

## Verification (seen, not asserted)

- Live on this repo: `ecology=0.956(K=37/N=54)` — 37 persistent taxa active across 54 edit-events,
  currently balanced — reported *beside* `inherit-μ=1.000`, showing the two are orthogonal.
- Not vacuous (synthetic): balanced 10-taxa → **1.0**; one taxon dominating 10 → **0.331**; even pair →
  **1.0** vs skewed pair → **0.286**. Evenness collapses exactly under monoculture while μ would stay 1.0.
- `bash -n` clean; appears in `--check` report and the `vitality.log` line.

## Distinct from every existing sign

NOT `action_occupancy` (Shannon over ALL edited tools, no persistence filter → includes newborn churn;
ecology restricts to the 14d-persistent core = exactly the change-vs-ecology gap) · NOT `inheritance_μ`
(single survival fraction, no balance term) · NOT `heaps_beta` (birth diversity-law) · NOT
`path_divergence` (cross-CHANNEL board heterogeneity, not code-tool abundance).

## Sources

- Dolson, Vostinar, Wiser & Ofria, "The MODES Toolbox", Artificial Life 25(1):50, 2019 —
  https://direct.mit.edu/artl/article/25/1/50/2915/
- "Assessing the ability of the MODES toolbox to detect hallmarks of open-endedness", ALIFE 2024
  Proc. 36:10 — https://direct.mit.edu/isal/proceedings/isal2024/36/10/123479
- MODES toolbox code (Dolson) — https://github.com/emilydolson/MODES-toolbox-paper

## Coverage note

Updates memory `oee-alife-coverage`: the MODES **Ecology hallmark as a live metric** moves from
"NOT YET embodied" to **EMBODIED** (`ecology_potential`, evenness-of-persistent-taxa). Still open: the
CONNECTION/codebase-lane MAP-Elites descriptor; VLM-guided evolution; POET co-evolving env+agent.
