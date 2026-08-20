# The trust window measures the WRITER's clock; the room publishes its own timescale and we cut it off the line

**Live review, 2026-08-20 — niche construction & the extended phenotype, from the angle the task asked
for: a concrete METRIC / scaling law the area measures itself with.**
Landed in `scripts/mesh-situation` (uncommitted; steward lands from the tree).

## What was already ours (checked before searching, so the review could not re-land)

| embodied | where |
|---|---|
| Fogarty & Wade 2022 — NC as a modified breeder's equation; realized h² > 1 | `mesh-vitality:488`, `mesh-forage` |
| Odling-Smee/Laland/Feldman — inceptive vs counteractive NC | `mesh-ideate:303` |
| Kurtz — experimental **removal** of niche construction (the ablation control) | `mesh-ideate:273` |
| Ayres et al. — **home-field advantage** as an INTERACTION, not a gap | `mesh-promises --homefield` |
| Albertson et al. 2024 — **ghost** legacies: a dead engineer's artifact still steering | `mesh-reflex-health` |
| Wade & Sultan — **negative** NC / inter-scale conflict / terminator niche | `mesh-forage:132` |
| NC3 mechanism attribution (construction vs choice vs conformance) | `mesh-forage` `nc3()` |
| by-product null: an adaptive verdict needs the SIGN of the fitness change | `mesh-forage` |
| driftability / the variance channel | `mesh-forage` |
| contemporaneous reference class for a legacy claim | `mesh-reflex-health` `ow_cohort_clause()` |

Every one of those is about the **construction** — who built it, whether it helps, whether it outlives
the builder. None of them is about the **timescale the construction sets**, or about how long a reading
of a constructed environment stays true. That is the shape of the gap.

## The find

**Lee, E. D., Flack, J. C. & Krakauer, D. C. (2024). "Constructing stability: optimal learning in noisy
ecological niches." *Proc. R. Soc. B* 291(2033):20241606. doi:10.1098/rspb.2024.1606.** Preprint:
"Outsourcing Memory Through Niche Construction," bioRxiv 2022.09.01.506204. Santa Fe Institute; press
coverage 2024-10-31 ("why elephants never forget but fleas have the attention span of a flea").
Found by live web search 2026-08-20; abstract read via the PMC copy (PMC11606325).

Their result is a **scaling law, not a level**:

> the optimal memory duration **τ_m\*** grows **SUBLINEARLY** in the environment's own timescale **τ_E**.

The mechanism is a cost asymmetry: carrying a memory costs **linearly** in its length (you pay it every
time the world turns while you are still holding the old value), while the payoff of *extra* memory in a
world that is already stable grows only **logarithmically**. So an environment that becomes 2× calmer
buys roughly √2 more memory — never 2×. The niche-construction half is the other side of the same
coin: an organism that **stabilizes** its environment lengthens τ_E and can then *outsource* memory to
the constructed structure — a ratchet toward slower timescales.

Two things make it the right find for us and not another philosophy landing:
1. τ_E is a **measured quantity of the environment**, separate from the observer's cadence.
2. The claim is about **how a window should MOVE**, which is testable without ever agreeing on the level.

## The defect it names in us

`mesh-situation` folds four axes and carries three staleness windows. Every one is a constant whose own
comment justifies it by the **writer's cadence**:

```
ABS_STALE_MIN=90    # hourly writer → 90min freshness threshold
STALE_MIN=20        # physical/occupancy older than this → STALE
EXT_STALE_MIN=90    # external: hourly cron → 90min threshold
# ---- OCCUPANCY: room-sense cached verdict (*/5 edge reflex keeps it fresh) ----
```

That is a claim about the **producer's clock** — i.e. about liveness. And under the mesh's own
liveness-touch convention (mtime re-stamped on *every* successful eval, value or no value), a fresh
mtime is **not** evidence the value is still true. τ_E — how long a reading remains a valid claim about
the room — is a different quantity entirely.

The sharp part: **`.room-sense.state` already publishes τ_E on the very line we parse.**

```
PRESENT|dwell_s=11361|changes_24h=13
        ^^^^^^^^ current run length   ^^^^^^^^^^^ flip rate over the last day
```

`mesh-situation` does `cut -d'|' -f1` and throws fields 2 and 3 away. So the one axis in the fold that
measures its own timescale is gated by a window that structurally cannot see it — and that window is
**load-bearing**: `occ_seen` keys on it, which feeds `axes_unseen`, which appends
`(partial — n/3 axes unseen)` to POSTURE.

Both error directions are live, and the paper says they cost differently:

- **measured now on this node:** `changes_24h=13` → τ_E ≈ 110 min against a 20 min window, ratio **18%**
  — the window is ~5× shorter than the room's own timescale, so a 21-minute-old occupancy reading is
  counted as *unseen* when the room says it is still ~80% likely unchanged. Cheap direction (the
  logarithmic one), but it manufactures blindness in the posture.
- **the other direction, same constant:** at `changes_24h=200` (τ_E ≈ 7 min) the *same* 20 min window
  folds a value that has already turned twice, with **no STALE marker at all**. Expensive direction
  (linear), and silent.

A fixed window is correct at exactly one volatility. Nothing in the mesh measured which one.

## What landed

`scripts/mesh-situation` — a **report-only** MEMORY-HORIZON clause. It does **not** move the gate:
`occ_seen`/POSTURE still key on `STALE_MIN`. Two reasons, both deliberate: changing a verdict is the
steward's call, and **the paper supplies an exponent, not the constant that would set the level**.

- Parses `dwell_s` / `changes_24h` off the line we already read; τ_E = 1440 / changes_24h.
- Renders `window vs τ_E, ratio, verdict ∈ {over-long, matched, short, censored}`.
- **w\*** applies the sublinear law from an anchor that is the axis's **own median τ_E**, accumulated in
  a sliding ring (`~/.mesh/.situation-tau.ring`, depth 32, grown on the `--edge` cadence only). The fixed
  window is taken as calibrated at *typical* volatility, and w\* says only how far *today's* volatility
  should push it: `w* = STALE_MIN · √(τ_E / median τ_E)`. Because the ring slides, the median turns over
  and w\* is re-derived every run — never frozen into a source constant (the `mesh-sound-reflex` n=29 rot).
- Under the n floor (6 samples) the anchor renders `thin` and w\* is `na`, never a guess.
- **Two absences kept apart:** `changes_24h=0` is **censored** (the room held one value all day → τ_E ≥
  1440 min, a *bound*), a missing field is **blind** (pre-dwell-fields state, or room-sense never ran).
  Neither may print a number.
- New `--json` keys (additive; the only in-tree consumer of this JSON is the file itself):
  `stale_window_min`, `tau_e_min`, `mem_verdict`, `mem_ratio_pct`, `mem_wstar_min`, `mem_anchor` —
  strings where `na` is legal, so a machine consumer cannot read an absent timescale as 0.

Live output on mesh-home, 2026-08-20:

```
 MEMORY-HORIZON[short  ] occupancy window=20min vs tau_E=110min (changes_24h=13, dwell_s=11361) ratio=18% · w*=na (anchor=thin, sublinear sqrt)
```

## Gates, and each one seen RED

`--test` grows six assertions. **A gate you have not seen fail is not a gate** — each was broken,
watched go red, and restored:

| mutant | result |
|---|---|
| `sqrt(t/m)` → `t/m` (exponent silently reverts to 1) | **RED** — "must give w\*=20·√4=40min, got 80" |
| drop the `n < SIT_TAU_MIN_N` floor | **RED** — "w\* must be na/thin, got 40/median:n=5" |
| collapse censored and blind into one word | **RED** — "a state file with no changes_24h field is BLINDNESS, not a calm room" |
| let `--json` append to the τ ring | **RED** — "--json GREW the tau ring 6→7 — only --edge may append" |

The first is the one that matters: it is the only assertion in the mesh that would catch the *scaling
exponent* reverting to the naive-linear rule every other window in this file implicitly uses.

Verified separately, out of tree: three sandbox `--edge` runs grow the ring `30 30 30` (so the */15
reflex fills the 6-sample anchor in ~1.5 h), and the full suite is green:

```
smoke-test: ok (… + memory-horizon: verdicts, SUBLINEAR w*, thin-anchor na, censored-vs-blind, fold+json carry, tau-ring edge-only)
```

## What this does NOT claim

- It does not claim 20 min is wrong. It claims 20 min is a statement about `mesh-room-sense`'s cron
  line and cannot be a statement about the room.
- τ_E from `changes_24h` is a **mean dwell over the last day**; a bimodal room (busy evenings, empty
  nights) has no single τ_E, and the mean would sit between the modes serving neither
  (`a-median-calibrates-to-neither-mode-of-a-bimodal-link`). The clause reports the mean and prints
  `dwell_s` beside it so the current realization is visible next to it; it does not fuse them.
- The anchor is a self-produced corpus (this clause grows the ring it later reads). That is deliberate
  self-calibration, but it means the *first* meaningful w\* on any node is ~1.5 h after deploy, and
  `thin` until then.
- Only OCCUPANCY has a τ_E at all. `EXTERNAL` and `PHYSICAL` publish no flip rate, so their windows
  (90/20 min) remain unaudited by this clause — naming that absence is part of the find, not a gap in it.

## Sources

- Lee, Flack & Krakauer 2024, *Proc. R. Soc. B* 291(2033):20241606 — https://royalsocietypublishing.org/rspb/article/291/2033/20241606 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11606325/
- Preprint: "Outsourcing Memory Through Niche Construction," bioRxiv 2022.09.01.506204 — https://www.biorxiv.org/content/10.1101/2022.09.01.506204v1
- Press: https://www.eurekalert.org/news-releases/1063183 · https://www.sciencedaily.com/releases/2024/10/241031124448.htm
- Context read alongside (not landed): Albertson et al. 2024, "The ghosts of ecosystem engineers,"
  *Functional Ecology* 38(1):52–72 — https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/1365-2435.14222 ·
  Laland et al., "Niche Construction Theory: A Practical Guide for Ecologists," *QRB* 88(1) —
  https://www.journals.uchicago.edu/doi/10.1086/669266

## Incidental, not fixed here

`mesh-series-stats` exists in `~/.local/bin/` but **not** in `scripts/` — a deployed-only tool, i.e. the
drift-clobber direction CLAUDE.md warns about, and CLAUDE.md cites it by name as the re-derivation
instrument for the doctrine claims. Flagged, not touched (out of this task's scope).
