# Swarm intelligence & stigmergy — live review: interaction-rate closed-loop foraging (Gordon)

**Date:** 2026-07-30 · **Mind:** genome · **Angle:** an OPERATIONAL closed-loop *regulation* rule
(not a distribution metric, not philosophy) that the mesh does not embody.

## The mechanism

Deborah Gordon's harvester-ant foraging is a **closed-loop excitable system**: an outgoing forager's
activation is driven by the **rate at which it encounters *returning, successful* foragers** — not by
any global census — and there is a **critical return rate below which foraging spontaneously STOPS**.
The colony's own negative feedback is simply: *returns fall → outbound activation falls.* No individual
assesses the whole; the regulation is emergent from the return-encounter rate.

- **Verified source:** Pagliara, Gordon & Leonard, "Regulation of harvester ant foraging as a
  closed-loop excitable system," *PLOS Computational Biology* 14(12):e1006200, 2018 —
  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006200 (PubMed 30513076).
  Empirical basis: Greene, Pinter-Wollman & Gordon, *PLOS ONE* 2013.
- Found via a live web review of current swarm-intelligence / stigmergy literature (scouting agent,
  2026-07-30); source existence verified against the PLOS DOI.

## Why it is NOT already embodied

The mesh already carries a lot of stigmergy: pheromone-selection **entropy** / dead-lane evenness
(`mesh-forage`), negative pheromone / no-entry, response-threshold division of labour, cross-inhibition
dispatch, tunable quorum, ant-mill trap, collective gradient, sematectonic-vs-sign stigmergy,
asignifying-rupture reconnect-ratio. All of these read **distributions** or **structural** state.

The closest prior art is **`mesh-quota`'s metastable-failure axis** (distsys review, 2026-07-29):
`busy(SPEND burn) ∧ useless(ZERO [done]) ∧ cleared`. That is a **static quadrant** off the *spend* axis
that trips only when goodput is **exactly zero**. Gordon's contribution is the **dynamic negative-
feedback loop**, and it differs on two axes `mesh-quota` cannot see:

1. **Deceleration, not zero.** A return rate that is **collapsing but still nonzero** — the excitable
   colony is already down-regulating — never trips `mesh-quota`'s zero-gate. This is an *early warning*.
2. **The coupling itself.** Whether **outbound is still being minted while the drive falls** (the missing
   negative feedback), read purely from **board marks** ([taking]/[task] vs [done]), no spend data.

So this is a genuinely un-occupied reading: the *temporal coupling* between outbound forays and returns,
complementary to `mesh-forage`'s *spatial* lane-evenness.

## The application (landed, report-only)

**File:** `scripts/mesh-forage` — a new **forager-drive** axis (additive, never changes rc, like every
other axis in the tool). The mesh's returning foragers ARE the board's `[done]` marks; outbound forays
ARE `[taking]`/`[task]` claims. Over the window (default 12h) split into a recent and a prior half:

- `ret_recent` / `ret_prior` = `[done]` returns in each half; `out_recent` = outbound forays (recent).
- **`drive_verdict()`** — a pure function of the three counts (tested directly, like
  `mesh-novelty`'s `_tempering_verdict`):
  - **OVERDRIVEN** — outbound still minted (≥`OUT_FLOOR`) while returns fell/dried: broken negative
    feedback (the Gordon fault; the fault `mesh-quota` misses because returns are still nonzero).
  - **DECELERATING** — returns collapsed to <`DECEL`× the prior half (still nonzero), no outbound
    pressure yet: the early-warning wind-down.
  - **QUIESCENT** — returns dried AND dispatch idled with them: the excitable system correctly stopped
    (**not** a fault).
  - **FORAGING** — drive sustained (active dispatch *with* healthy returns is fine, not flagged).

**Load-bearing separation (the RED-first falsifier):** OVERDRIVEN vs QUIESCENT have the **same** (low)
recent returns and differ **only** by `out_recent`. A verdict blind to `out_recent` collapses them —
it cannot tell "broken feedback, still dispatching into a dry patch" from "colony correctly stopped."
`--test` asserts the full 5-cell matrix through the real binary AND the discriminator; neutering
`active` (blinding the verdict to outbound) fails *exactly* the discriminator + the `(1,20,5)` cell.

**Live reading at land:** `forager-drive: FORAGING (returns recent=25 prior=12, outbound=1)` — the
board is return-dominated (autonomous lit-review lanes post `[done]` directly), a healthy closed loop;
the axis correctly does not fire, and only trips in the pathology (a claim-storm while `[done]` collapses).

**Knobs (env, calibrated to the current board; self-scaling via the window):**
`MESH_FORAGE_DRIVE_FLOOR=2` · `MESH_FORAGE_DRIVE_OUT_FLOOR=3` · `MESH_FORAGE_DRIVE_DECEL=0.5` ·
`MESH_FORAGE_DRIVE_MIN=4` (below → honest n/a). These are rate thresholds — env-overridable, not pinned
constants in code, per the calibration doctrine.

## Honest scope

- On a `[taking]`-sparse board (the current regime) the OVERDRIVEN cell is reachable but rare — it needs
  a real outbound claim-storm to fire. That is correct for a report-only diagnostic (fires in the
  pathology, silent when healthy), and the `--test` proves reachability on a synthetic board.
- It is a **window-rate coupling**, not per-claim tracking; `mesh-promises`/asignifying already own the
  per-claim kept/leaked ledger. This is the distinct *rate/drive* question.
