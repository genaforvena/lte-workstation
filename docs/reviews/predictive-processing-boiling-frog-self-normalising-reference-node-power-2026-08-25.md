# The reference re-learns the wear, so the wear has zero prediction error — by construction

**Live review, 2026-08-25 — predictive processing & the Bayesian brain, from the angle the task
asked for: a foundational idea we may have MISread or applied too loosely.**
**Arm:** treated (assigned) — target organ `scripts/mesh-node-power` drawn by coin at p=0.20 from
the 568 never-reviewed tools, not chosen by me or by the lane.
Landed in `scripts/mesh-node-power` (uncommitted; steward lands from the tree).

## What was already ours (checked before searching, so the review could not re-land)

Twenty-six prior reviews sit in this area — it is the most worked ground in `docs/reviews/`:

| embodied | where |
|---|---|
| precision as inverse variance, allocated across channels | `fep-interoceptive-precision-allocation-*`, `mesh-precision` |
| context-conditioned observation noise | `fep-channel-knowledge-map-*` |
| expected free energy, ambiguity, the price of an honest `na` | `fep-expected-free-energy-*` → `mesh-reflex-health` |
| Bayesian **surprise** vs Shannon surprise | `predictive-processing-bayesian-surprise-vs-shannon-*` |
| circular inference / overcounting one's own prior | `predictive-processing-circular-inference-*` |
| **volatility vs stochasticity** — which term a change belongs to | `predictive-processing-volatility-vs-stochasticity-*` (2026-08-25, same day) |
| uncertainty-driven vs error-driven boundaries | `predictive-processing-uncertainty-driven-vs-error-driven-*` |
| a monotone **ramp** invisible to a trailing-median baseline | memory `a-ramp-drags-its-own-baseline` (`mesh-algedonic`, 2026-08-18) |
| a sliding window having already smoothed its own output | memory `a-sliding-window-has-already-smoothed-its-own-output` |
| a threshold re-derived from a corpus that contains its own subject | memory `a-self-calibrating-threshold-can-be-mostly-its-own-subject` |

So the *adaptive-baseline* family is ours. The delta below is the case where the adaptation is not
statistical at all.

## The concept, and where I found it

**Zhe Hong, "The Boiling Frog Threshold: Criticality and Blindness in World Model-Based Anomaly
Detection Under Gradual Drift", arXiv:2603.08455, submitted 2026-03-09.**

The claim: prediction-error anomaly detectors built on a learned world model have a sharp critical
drift rate **ε\***. Below it, corrupted observations are *absorbed into the noise floor the model
itself learned* and escape detection entirely; above it, drift is caught quickly. Within one
environment ε\* follows a power law in the detector parameters (R² = 0.89–0.97), but it does **not**
transfer — cross-environment prediction collapses to R² = 0.45, because ε\* is a three-way
interaction between noise-floor structure, detector sensitivity and the environment's own
∂PE/∂ε. Two results are the ones that bite here: *"sinusoidal drift is completely undetectable by
all detector families"* — a property of how models absorb variation, not a flaw in any one
detector — and, in fragile environments, **"collapse before awareness"**: the system fails before
any detector can trigger.

Found via a live search on predictive-processing precision/misinterpretation (August 2026); the
paper is not cited anywhere in `docs/` or `scripts/` — new ground.

## Where we read the foundational idea too loosely

"Prediction error minimisation" gets applied here as *"compare the reading to a baseline and alarm
on the deviation."* The half we skipped is that the **baseline is itself estimated**, and an
estimator that tracks the drift reports no error while the drift proceeds. Our prior art has this
for a *statistic* (`a-ramp-drags-its-own-baseline`: a trailing median chases a ramp). What Hong's
framing adds — and what `mesh-node-power` turns out to be a pure instance of — is the case where
the normaliser is not an estimate at all, but **definitional**.

## The finding in the organ

`mesh-node-power` classified everything from one field, `/sys/class/power_supply/BAT0/capacity`,
and never read `*_full_design`. The kernel's own documentation
(`Documentation/power/power_supply_class.rst`) defines the reference that field is a percentage of:

> `CHARGE_FULL` / `ENERGY_FULL` — *"last remembered value of charge when battery became full/empty"*,
> *"value of charge when battery is considered full/empty at given conditions (temperature, **age**)"*
> — **"real thresholds, not design values"**, in contrast to `CHARGE_FULL_DESIGN` / `ENERGY_FULL_DESIGN`.

So the denominator **is** the wear. A battery at half its design capacity reads `100%`, and the
organ was not slow to notice degradation — it was structurally incapable of noticing it. This is
Hong's blindness zone with the interesting parameter removed: the absorption is exact rather than
statistical, so **there is no ε\* to be under. No drift rate is detectable, however fast.** A cell
that lost half its capacity overnight would read exactly as it read the day before.

It reaches the thresholds too. `CRITICAL <5%` and `LOW-BATTERY <20%` are five and twenty percent of
a pool that shrinks, so on a half-worn battery the LOW edge fires at half the runtime it was
calibrated for — the edge did not move, the axis under it did. And the organ already carried the
honest absolute channel next door: `time_remaining = energy_now/power_now`, in hours, referenced to
nothing that adapts. Having both made the contradiction checkable rather than theoretical.

`cycle_count` was already read, but only in `--json`, and a cycle count is an odometer — it says how
much the battery has been used, never how much of it is left.

## What landed

`scripts/mesh-node-power` now keeps an **un-adapted channel beside the adapted one and publishes the
divergence, because the divergence is the drift**:

- `battery_health_pct` = `full / full_design × 100` — how much of the designed cell remains.
- `capacity_design_pct` = `now / full_design × 100` — charge against the reference that never moves.
- Both in `--json` and in the text line; `charge_*` (µAh) and `energy_*` (µWh) drivers both handled.
- Where a driver exposes no design capacity the fields render **`null` / `wear: na`**, never 100 —
  an absent measurement reading as a healthy battery is the same failure one ring in.
- `MESH_POWER_SYSFS` parameterises the sysfs root, because **this node has no battery at all**
  (`/sys/class/power_supply` is empty, the tool exits 2) and without it every assertion below would
  be unreachable on the machine that runs the gate.

Deliberately **not** landed: a `WORN` label or a health threshold. A new edge with no corpus behind
it is a constant calibrated once, which is the failure `calibrate-a-derived-axis-against-the-live-corpus`
already names. The axis is published first; the edge is an operator calibration call.

## Gates

`mesh-node-power --test` rc=0, with four fixture arms that run **before** the no-battery early
return, so they execute here:

- a battery at half design capacity still reads `capacity 100` **and** now reads `health 50` /
  `design-referenced 50` — the blindness and its cure asserted in the same breath;
- an unworn control reads `health 100`, or `health 50` above would prove nothing;
- a driver with no design capacity renders `null`, not 100;
- `energy_*` drivers compute it too (40% health, 30% design-referenced).

Three mutants driven red: absent-design-silently-reads-100, health-pinned-to-100, and text-line-
omits-the-`na`-wear-term.

One bug was found by the gate rather than by reading: the first cut iterated field-name triples with
`set -- $_pair`, which reassigns the **script's own argv** — by the time the renderer tested
`"${1:-}" = --json`, `$1` was a sysfs field name and `--json` printed plain text.

## Honest bounds

- **No live battery artifact.** `mesh-home` has no battery; no battery-bearing peer answered
  (`phaedra` is a VPS, the two other online peers are not ours to probe). Every number above is
  fixture-driven. The *semantics* are cited to the kernel's own documentation, not measured here.
- The claim that driver-supplied `capacity` is referenced to present-full rather than design varies
  by EC; where a driver supplies it directly it is the EC's own state-of-charge, which is likewise
  not design-referenced. Either way the organ read `capacity` **and nothing else**, so it could not
  express wear regardless of which full the percentage was taken against — that part needs no
  assumption.
- Hong's paper offers **no remedy**; it reframes ε\* as a three-way interaction. The un-adapted
  channel here is the implication of that framing, not a result reported in it.
