# Live-literature review — information theory of agency: PREDICTIVE INFORMATION (excess entropy) as a STRUCTURE-vs-NOISE discriminator the coefficient-of-variation is blind to

Date: 2026-07-28 · lane: genome (idea-queue LITERATURE task — information theory of agency / empowerment /
predictive information, from the angle of an OPERATIONAL mechanism to implement) · status: fix in tree,
uncommitted (steward lands)

## Where we had already been (so this doesn't double-count)

Information theory of agency is a worked mesh seam. Confirmed the embodied set before landing:

- **empowerment — action→future-sensor-state mutual information** (channel capacity of the sensor-actuator
  loop) → `scripts/mesh-algedonic` AGENCY_INFO sidecar (MI between board ACTION presence and the next
  algedonic pain-change bucket).
- **Maximum Occupancy Principle** (occupy future action-state path space; Ramírez-Ruiz & Moreno-Bote,
  Nat. Comm. 2024) → `scripts/mesh-vitality` `action_occupancy()`.
- **transfer entropy** (directed lagged info flow; Schreiber 2000) → `scripts/mesh-cooscillate`.
- **overwrite control vs hidden-state identification** (Csaky 2026) → review 2026-07-24.

What is **not** embodied is the predictive-information branch's *core measure*: **I(past;future) — the
"excess entropy" — of a single sensorimotor stream**, used as an operational **structure-vs-noise**
discriminator.

## The mechanism not yet embodied — PREDICTIVE INFORMATION (excess entropy)

Bialek, Nemenman & Tishby define **predictive information** as the mutual information the PAST of a stream
carries about its FUTURE — the *sub-extensive* part of the entropy, "the only part of the information in
the past that is useful for predicting the future." Ay, Bertschinger, Der, Güttler & Olbrich, and Der &
Martius's *homeokinesis*, operationalize it in the sensorimotor loop: **a controller that maximizes its own
predictive information self-organizes structured, exploratory behavior.** Used as a *measure* (not a
controller), it answers a question the coefficient of variation cannot.

**Citations** (found via web review, 2026-07):

- **W. Bialek, I. Nemenman, N. Tishby, "Predictability, complexity, and learning"**, *Neural Computation*
  13(11):2409 (2001) — the definition of predictive information / excess entropy.
- **N. Ay, N. Bertschinger, R. Der, F. Güttler, E. Olbrich, "Predictive information and explorative
  behavior of autonomous robots"**, *Eur. Phys. J. B* 63:329 (2008); **R. Der & G. Martius, *The Playful
  Machine*** (2012) — the sensorimotor operationalization (homeokinesis).
- **C. Salge, C. Glackin, D. Polani, "Empowerment — An Introduction"** (in *Guided Self-Organization*,
  Springer 2014) and the current **"Process empowerment for robust intrinsic motivation"**, *J. Phys.
  Complexity* 6 (2025), doi:10.1088/2632-072X/adf2ec — both restate empowerment as the **channel capacity
  of the sensor-actuator loop**, counting "only the influence the agent can itself SENSE"; predictive
  information is its passive-stream sibling (past↔future instead of action↔future). (LIVE, 2025 — confirms
  continuously-published literature.)

## Why it applies to us — the gap in `scripts/mesh-precision`

`mesh-precision --num` measures a sense's reliability as the **coefficient of variation** (sd/mean), with a
FROZEN floor for zero variance. **CV measures HOW MUCH a signal varies; it is blind to whether that variance
is PREDICTABLE STRUCTURE or WHITE NOISE.** Two senses can be indistinguishable to CV yet opposite in kind:

- a sensor tracking a real quantity — a smooth thermal drift, a diurnal oscillation — has high CV but its
  **past strongly predicts its future** (a LIVING signal);
- a hollow / flapping sensor emitting white noise has the *same* CV but its **past predicts nothing**.

Both read NOISY/UNRELIABLE and get down-weighted alike — **a false down-weight that discards a living signal
as noise.** Predictive information separates them: for a locally-Gaussian stream,

    PI₁ = -½ log₂(1 − ρ₁²)   bits,   ρ₁ = lag-1 autocorrelation

high PI = predictable structure (do NOT dismiss); PI≈0 = white noise (the CV down-weight is right). A
*deterministic oscillation* is correctly HIGH predictive information — it is a real signal, not noise;
per-switch FLAPPING is the categorical `--cat`/switch-rate axis's job. The three axes compose: **CV =
magnitude, switch-rate = persistence, PI = predictability-of-the-variance.**

## What landed (report-only axis, advisory — touches NO verdict or weight)

`scripts/mesh-precision --num` output now also carries `pred_info` (bits) + a
**STRUCTURED | WEAK-STRUCTURE | NOISE** label, keyed on `MESH_PREC_PI_HI`/`MESH_PREC_PI_LO` (defaults
0.5/0.15 bits ≈ |ρ₁| 0.70/0.42), on the numeric non-frozen path (JSON field + text clause). Same report-only
posture as the novelty / frame_coverage / independence axes already on this file — a consumer down-weighting
a NOISY axis can first ask whether the variance is structure (a living signal to KEEP) or noise (safe to
discard). It never overrides the CV verdict or a fusion weight.

**Verification (artifacts, not claims):**

- `mesh-precision --test` — GREEN. New RED-first assertion: two tapes with the **identical multiset**
  (→ identical CV 0.5311 → identical verdict UNRELIABLE) split on PI — the smooth ramp `1..12` reads
  **STRUCTURED** (PI 0.596b), its low-autocorrelation shuffle reads **NOISE** (PI 0.0b). CV is blind to the
  split PI catches. Broke it live — `MESH_PREC_PI_HI=99 mesh-precision --test` → **FAIL rc=1** (ramp drops to
  WEAK-STRUCTURE, can't clear the STRUCTURED bar) — then restored (default → `smoke-test: ok`).
- Live physical senses (both directions):
  - **hwmon temp** (real NVMe/CPU thermal): smooth cooling drift 44850→42850 → CV 0.020 RELIABLE, **pred_info
    0.66b STRUCTURED** — a living thermal signal.
  - **MemAvailable**: jitters around 22.3M with no trend → CV 0.000 RELIABLE (maximally trustworthy to CV!),
    yet **pred_info 0.02b NOISE** — the variance is structureless allocation jitter, not a tracked quantity.
    The low-CV end is exactly where CV's blindness bites, and PI catches it.
- Regression: `--num`/`--cat`/FROZEN/novelty/frame_coverage/independence/`--room-flap` assertions unchanged.

## One-line honesty note

PI₁ is a lag-1 (Gaussian) proxy for the full excess entropy — it captures first-order temporal
predictability, not long-range structure; a signal whose only structure is at long lag reads NOISE here. It
gates nothing until the steward validates against real sense tapes; it is a companion axis to CV, not a
replacement.
