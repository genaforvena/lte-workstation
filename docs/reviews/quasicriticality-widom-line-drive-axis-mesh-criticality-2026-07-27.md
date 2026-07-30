# LITERATURE review — CAS / edge-of-chaos, RECENT result (2023-2026): quasicriticality & the Widom line (2026-07-27)

**Area:** complex adaptive systems & the edge of chaos (Santa Fe lineage), entered from the task's angle
— **a RECENT result (2023-2026), what's new right now** — landing on ground `mesh-criticality` (which
already carries ~10 stacked SOC/edge-of-chaos reviews) has NOT been.

## The concept

**Quasicriticality** and the **nonequilibrium Widom line.** The self-organized-criticality / neural-
avalanche picture the mesh imported treats a system as sitting on a **1-D axis**: distance to the
critical point (branching ratio m=1). The quasicriticality program shows that picture is incomplete for
any *driven* system. A real system under external input does **not** sit exactly at criticality — it
hovers near it on a **nonequilibrium Widom line** whose **second axis is the drive**. The move onto that
line is governed by an assumption the whole avalanche framework rests on and that drive **violates**:
**timescale separation.** An "avalanche" is only well-defined when cascades are brief and separated by
**silence** — which requires the external drive (input rate) to be slow relative to cascade propagation.
Crank the drive up and input arrives *during* a cascade, avalanches **merge**, the silences vanish, and
the system slides along the Widom line: **m̂≈1 no longer certifies exact criticality**, and the critical
exponents (avalanche shape, crackling) **fall in absolute value with drive** while dynamical scaling only
approximately holds. This is the organizing idea that *resolves* the long-standing embarrassment that
measured critical exponents refuse to settle into one universality class — the system is **quasicritical,
not critical**.

Sources (read 2026-07-27 — a live, continuing program, not a fixed citation):
- Williams-García, Moore, Beggs & Ortiz, *Quasicritical brain dynamics on a nonequilibrium Widom line*,
  Phys. Rev. E **90**, 062714 (2014) — the origin; the Widom-line construction.
- Fosque, Williams-García, Beggs & Ortiz, *Evidence for Quasicritical Brain Dynamics*, Phys. Rev. Lett.
  **126**, 098101 (2021) — https://physics.aps.org/featured-article-pdf/10.1103/PhysRevLett.126.098101
- Fosque, Alipour, Zare, Williams-García, Beggs & Ortiz, *Quasicriticality explains variability of human
  neural dynamics across life span*, 2022, arXiv:2209.02592 (PubMed 36532868) — exponents shift with
  drive/age, not a fixed class.
- *Critical Neuronal Models with Relaxed Timescale Separation*, Phys. Rev. X **9**, 021062 (2019),
  arXiv:1808.04196 — the precise mechanism of breaking separation (input during avalanches).
- **RECENT anchor:** *A Minimal Network of Brain Dynamics: Hierarchy of Approximations to Quasi-critical
  Neural Network Dynamics*, arXiv:2512.22093 (Dec 2025) — the program is actively continuing into 2026.

## The gap — mesh-criticality never measures the DRIVE axis

`mesh-criticality` reports m̂ + a 1-D regime (SUB/CRITICAL/SUPER) and calls m̂≈1 "healthy/maximally
responsive." Its existing sidecars guard *neighbouring* axes but **not this one**:
- `bin_sanity()` guards the **Δt granularity** of avalanche detection (Δt vs ⟨IEI⟩).
- `drift_classify()` / `csd_classify()` guard m̂ **non-stationarity over the tape**.
- **Nothing** asks whether **timescale separation even HOLDS for the current window** — i.e. whether the
  near-critical m̂ is a bona-fide criticality reading or a **Widom-line (driven) artifact**. That is
  exactly the second axis quasicriticality says a 1-D m̂ omits, and it bites hardest during a flood — the
  moment the alarm matters — where drive is high, silences vanish, and a SUPERCRITICAL m̂ may be a
  driven merge rather than a genuine runaway.

## The concrete application (implemented, read-only, RED-first)

**File: `scripts/mesh-criticality`** — added `drive_regime()` + a `--widom` mode + a `Widom=` field in
the default text and `--json` output. It measures the **drive axis** over the same board event stream,
with the classic **avalanche-separation criterion**: the **silence fraction φ = empty-bins / total** (an
avalanche is a run of active bins bounded by *empty* ones), plus the **longest merged-run coverage ρ**:

- **SEPARATED** (φ ≥ 0.5) — clear silences; timescale separation holds → m̂ is a real criticality reading.
- **DRIVEN** (0.15 ≤ φ < 0.5) — silences eroding → quasicritical Widom-line reading; m̂≈1 under-determined.
- **SATURATED** (φ < 0.15, or one merged super-avalanche ρ ≥ 0.66 spans the window) — separation BROKEN,
  deep on the Widom line → m̂ and the shape/crackling exponents are drive-contaminated.
- **INSUFFICIENT** — < 3 events / < 8 bins (honest, never a faked verdict).

**READ-ONLY** — never touches m̂ / regime / the alarm gate (same restraint as `bin_sanity`/CSD/Shape). It
says *which axis* a near-critical m̂ lives on, not whether to alarm.

Gate: `mesh-criticality --test` — a clustered-with-long-silences stream → `SEPARATED`; every-bin-active
(no silence) → `SATURATED`; eroding silences → `DRIVEN`; < 3 events → `INSUFFICIENT`; plus a
label-is-not-a-constant check. **RED-first verified:** forcing the label to a constant `SEPARATED` turns
the SATURATED assertion red (`every-bin-active / no silence must be SATURATED … got 'SEPARATED'`);
restoring it goes green.

**Live run 2026-07-27 on the real board:**
`m̂=0.879 [CRITICAL] … Bin=CALIBRATED ⟨IEI⟩=175s … Widom=DRIVEN φ=0.43 ρ=0.08`.
The payoff in one line: the board reads a **near-critical, "healthy"** m̂ — but `Widom=DRIVEN` says it is
currently **driven**, sitting on the Widom line, so that m̂ is a **quasicritical** reading, not certified
exact criticality. ρ=0.08 (no single merged super-avalanche) correctly keeps it DRIVEN, not SATURATED —
separation is eroding, not gone.

## Why not discarded

Discardable only if the drive axis were already measured. It is not: every existing sidecar guards Δt
granularity or m̂ non-stationarity; none asks whether the avalanche framework's own precondition
(timescale separation) holds *now*. The concept is the field's own current organizing principle (Widom
line / quasicriticality, actively published into Dec-2025), and it is computable — cheaply — over the
exact event stream the tool already bins. Honest limits: φ is read WITH `bin_sanity` (a GLUING Δt would
deflate φ artificially) and the thresholds are heuristic, env-tunable, and advisory — never an alarm
input. The rigorous next step (unwired): join φ to the m̂ tape to trace the board's actual trajectory
*along* the Widom line (drive × proximity), the 2-D read the 1-D regime picture still flattens.
