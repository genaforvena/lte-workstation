# Antifragility/ruin live review — Parisian ruin: dwell, not the crossing

**Date:** 2026-07-29 · **Mind:** genome@mesh-home · **Area:** antifragility, convexity & ruin theory (Taleb)
· **Angle:** a recent result — deficit-dependent Parisian ruin
· **Artifact:** `scripts/mesh-resource-guard` → new pure classifier `node_dwell_classify()` + read-only `--status` axis (uncommitted, source-only)

## The landing

**Parisian ruin.** In classical (absorbing-barrier) ruin the process is dead the *instant* it crosses below
the barrier. Parisian ruin recognizes ruin only when the surplus stays **continuously below** the barrier
for longer than a fixed **implementation delay** — a grace clock `d` that **resets** the moment the process
climbs back above. An excursion the system recovers from is survivable; only a **sustained dwell** is
absorption. This is precisely the antifragility posture: *dip-and-recover is robust, and it is the dwell,
not the crossing, that kills you.*

The **recent** twist this actually implements is **deficit-dependent delays** (Baurdoux, Palmowski et al.,
arXiv:2111.02695, *Stoch. Proc. Appl.* 2023): the grace clock's length **depends on how deep** the excursion
is — a deeper deficit gets a **shorter** clock (you tolerate a shallow dip longer than a deep one). The area
is live — a 2024 Laplace-transform treatment of the Parisian ruin *time* and 2026 subordinated
Cramér–Lundberg asymptotics (arXiv:2603.01821) — which is what the task asked to land on.

## Why it's a real gap in `mesh-resource-guard`

The guard's own comment says it: *"Every axis above is a LEVEL detector — fires on a single-frame snapshot."*
The full family reads memory pressure at three temporal postures, and **none** is Parisian:

| axis | question | temporal posture |
|---|---|---|
| `node_pressure_classify` | is MemAvailable below the barrier **now**? | the instant of crossing = **classical absorbing ruin** |
| `node_accel_classify` | is the drop **accelerating**? | 2nd-derivative of the **approach**, before the crossing |
| `node_tau_eta` | **how soon** will we cross? | time-**TO** the barrier (forward) |
| **`node_dwell_classify`** (new) | **how long** have we stayed below? | time-**SINCE** the crossing = **Parisian dwell** |

The guard even has episode hysteresis (`CLEAN:<n>` re-arm) — but that only suppresses **re-posting after**
the instantaneous fire; it never defers the fire until the excursion is proven sustained. So a momentary dip
(cache churn, a mind's transient allocation freed next pass) reads identically to a swap-thrash slide into
OOM. Parisian ruin is the axis that tells a survivable dip from an absorbing one.

## The metric (`node_dwell_classify`)

Over the **same** retained MemAvailable series `accel_series` already maintains, count the trailing run of
samples continuously below the barrier (**reset to clean on any sample at/above** — the Parisian clock reset
on recovery); `dwell = run × interval`. Grace clock = base `d0` (`RG_DWELL_CLOCK_S`, default 300s), **halved
when the deepest point of the excursion is below barrier/2** (deficit-dependent delay). Then:

- `run≥2` **and** `dwell ≥ clock` → **`ruin|`** — sustained excursion past the implementation delay = absorption.
- below-but-within-grace → **`excursion|`** — recoverable dip, **not** ruin.
- latest recovered above / no history / barrier≤0 → **clean** (empty, never fabricate ruin from a no-op).

Pure AWK, no new state (reuses the accel history) and no new plumbing. Observable dwell is bounded by the
retained window (`ACCEL_KEEP × RG_INTERVAL_S`), so the clock must fit inside it — documented at the knob.

**Live:** silent — node avail 18.4GB of 32GB (≫ the 10% / 3.2GB barrier) → `run=0` → clean, correctly no
line. Surfaces on `--status` only when MemAvailable is actually dwelling below the barrier.

## Posture

**Report-only / visibility**, same as NODE-ACCELERATING's read-only `--status` line: it does **not** kill,
defer, or board-post — one dwell reading needs trend before it can gate, and the loud escalation for a
sustained excursion is `node_pressure`'s own board path. Falsifiable core: a **7-case fixture battery**
(clock-reset-on-recovery / single-dip-not-ruin / within-grace / sustained-ruin / **deficit-dependent-deep-ruin**
/ empty / barrier≤0-no-op) in `--test`; the deep-vs-shallow pair proves the deficit-dependence (same `run=2`,
deep fires where shallow stays an excursion). Seen **red→green** (flipped the sustained case to `excursion`,
watched `FAIL dwell`, restored → ok).

## Distinct from every existing axis

- **NOT `node_pressure_classify`** — instantaneous crossing (classical ruin); this is dwell-since (the Parisian refinement).
- **NOT `node_accel_classify`** — approach acceleration, *before* the crossing.
- **NOT `node_tau_eta`** — time-TO the barrier (forward); this is time-SINCE (backward at the excursion).
- **NOT the `CLEAN:<n>` hysteresis** — that suppresses re-posts *after* a fire; this governs whether the fire is warranted at all.

## Sources

- Czarna & Palmowski, "Ruin probability with Parisian delay for a spectrally negative Lévy risk process",
  *J. Appl. Probab.* 48(4):984 (2011). (base Parisian-delay model)
- Baurdoux, Palmowski et al., "Parisian ruin with random deficit-dependent delays for spectrally negative
  Lévy processes", arXiv:2111.02695 (*Stoch. Proc. Appl.* 2023). https://arxiv.org/abs/2111.02695 (the recent
  refinement implemented: deeper deficit → shorter grace clock)
- "Asymptotics of Ruin Probabilities in a Subordinated Cramér–Lundberg Model", arXiv:2603.01821 (2026).
  https://arxiv.org/pdf/2603.01821 (the area is live)
