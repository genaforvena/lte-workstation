# LITERATURE review — rheostasis: a defended, scheduled set-point (the "productive fever") (2026-07-27)

**Area:** homeostasis / allostasis / ultrastability (Ashby, Sterling), entered from the angle of a
**named regulatory mode the mesh does not yet embody** — one that sits beside the two it has walked
(homeostasis → allostasis) and beside homeorhesis, but is none of them.

## The concept — rheostasis (a THIRD mode, distinct from the two we embody)

- **Homeostasis** — defend a FIXED set-point by negative feedback.
- **Allostasis** — shift the reference in ANTICIPATION OF DEMAND; reactive to current/predicted context
  (Sterling). The mesh embodies this (mesh-body-power, mesh-algedonic allostatic load).
- **Rheostasis** — **N. Mrosovsky, *Rheostasis: The Physiology of Change*, OUP 1990**: *"homeostatic
  defences are present but there is a change in the LEVEL that is defended."* The set-point is
  programmatically MOVED — often on a schedule or program (fever, seasonal body-mass, torpor, pregnancy) —
  and the system then **defends the NEW value with full negative-feedback vigour**. The signature that
  separates it from allostasis: the system **RESISTS being pushed back to baseline** — a febrile body
  shivers if you cool it. The elevation is not error to correct; it is the point.

**Live literature (2025):** *Perspective: rheostasis revisited — hibernation and tanycytes*,
J Comp Physiol B (2025), doi:10.1007/s00360-025-01636-x — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12743108/ —
shows the hypothalamus coordinating a **scheduled, multi-system set-point shift** during hibernation
(lower defended core temp in torpor, higher on arousal), not passive conformity to ambient. Companion:
*Variable setpoint as a relaxing component in physiological control*, PMC5599866. Found live via
WebSearch 2026-07-27.

## Why this is not already embodied (checked, so it lands somewhere new)

Verified absent across `scripts/` and `docs/` (`grep -ril rheostasis|rheostatic` → 0). The neighbouring
modes are all present and are all a *different* claim:

- **Allostasis** (mesh-body-power, mesh-algedonic) — demand-driven, reactive; rheostasis is proactive,
  scheduled, and actively RESISTS being undone.
- **Reactive Scope Model** (docs/reviews/reactive-scope-wear-moves-the-threshold) — wear *lowers* a
  threshold involuntarily over time; rheostasis is a *voluntary, upward, reversible-on-schedule* shift.
- **Homeorhesis** (mesh-body-power:21, Waddington) — defend a TRAJECTORY, not a point; rheostasis defends
  a point, just a MOVED one.
- **Ultrastability / step-change** (mesh-homeostasis) — reconfigure the regulator on persistent breach;
  rheostasis doesn't reconfigure the regulator, it re-aims its set-point and keeps the same feedback law.
- **DUAL-ELEVATED / multicriticality** (mesh-resource-guard:20) — a joint two-axis *breach* (riskier true
  overload); rheostasis is elevation that is **not a breach at all**.

## The gap — `scripts/mesh-resource-guard` fights the productive fever

`mesh-resource-guard`'s every threshold is a **fixed homeostatic set-point** — RUNAWAY at RSS>3GB /
CPU>nproc×90%, NODE-PRESSURE at mem/swap bands — and it reads **all** elevation as potential
dysregulation. But some elevation is a **productive fever**: a node running a DECLARED heavy job (a grind
batch, a fine-tune, warm GPU inference) has high RSS/CPU that is EXPECTED, SCHEDULED, and to-be-DEFENDED
for the job's duration. With no notion of a defended-elevated set-point, the guard would renice /
oom_score_adj the very PID doing the work (bounded — it **never hard-kills**, operator decides) and,
worse, post RUNAWAY/NODE-PRESSURE as an *incident* when the "breach" is the point. Correcting toward the
old baseline a state the system is deliberately holding at the new one is exactly the rheostatic error.

The programmed-elevation signal is **already on disk**: `mesh-bg-register` writes a manifest per running
detached batch (`~/.mesh/bg/<window>/<batch>.manifest`, state=`running`) — a declared, lease-bounded
heavy job carrying its PID. `mesh-resource-guard` does not read it (checked, 0 hits).

## The concrete application (HELD — instrument-first, operator-gated)

On `scripts/mesh-resource-guard`: read the running bg manifests; when an elevated PID belongs to a
declared running batch, **re-label** its verdict `FEVER (declared <slug>, defended set-point, returns at
lease expiry)` instead of RUNAWAY, and suppress the renice/oom nudge **on that PID alone**. Report the
lease's remaining time as the trials-to-baseline horizon.

**Why HELD (load-bearing caveats, not shipped):**
1. The defended window MUST expire — a stuck or leaked manifest would blind the guard to a genuine
   runaway forever. `mesh-bg-register`'s crash-reap (dead-pid `running`→`crashed`) is the prerequisite,
   and the FEVER label must key on `running` only.
2. A **NODE-PRESSURE** breach that threatens OOM for the *whole node* still acts even mid-fever — defend
   the elevation, but not to the point of a node-wide kill. Rheostatic tolerance is scoped to the
   declared PID's own RUNAWAY line, never to the node-survival line.

Landed as: a literature-annotation block on `scripts/mesh-resource-guard` (before `set -uo pipefail`,
beside DUAL-ELEVATED) naming the gap and the HELD fix. **Zero behavior change** — the concept is embodied
as the named distinction so the fixed set-points can eventually honour a scheduled fever without going
blind to a real one.

## Sources

- N. Mrosovsky, *Rheostasis: The Physiology of Change*, Oxford University Press, 1990.
- *Perspective: rheostasis revisited — hibernation and tanycytes*, J Comp Physiol B (2025),
  doi:10.1007/s00360-025-01636-x — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12743108/
- *Variable setpoint as a relaxing component in physiological control*,
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5599866/
