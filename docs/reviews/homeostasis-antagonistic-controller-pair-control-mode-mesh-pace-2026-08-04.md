# Antagonistic controller pairs: delegated / isolated / metastable control — and the zero-separation setpoint in `mesh-pace`

**Date**: 2026-08-04 · **Mind**: genome · **Area**: homeostasis, allostasis & ultrastability (Ashby, Sterling)
· **Angle**: cross-domain transfer to a distributed sensor mesh · **Landed**: measurement half, report-only.

## The source (live literature, retrieved 2026-08-04)

**Ruoff HP, "Flux organizations and control modes in antagonistically combined negative feedback loops",
bioRxiv 2025.11.09.687434** (v1 posted 2025-11-10, v2; University of Stavanger, CC0). Retrieved via the
bioRxiv details API (`api.biorxiv.org/details/biorxiv/10.1101/2025.11.09.687434` — the web page 403s).

Foundation it extends: **Drengstig T, Jolma IW, Ni XY, Thorsen K, Xu XM, Ruoff P, "A Basic Set of
Homeostatic Controller Motifs", *Biophysical Journal* 103(9):2000–2010, 2012**, doi
`10.1016/j.bpj.2012.09.033` (PMC3491718).

### The concept

The 2012 paper splits homeostatic controller motifs into two operational classes — **inflow control**
(maintains the variable by *adding* to the system) and **outflow control** (by *removing*) — and names two
ways a single-class controller **breaks down**: (1) a *dominating perturbation in its non-compensable
direction* ("inflow controllers break down when there are large uncontrolled inflows, whereas outflow
controllers lose their homeostatic behavior in the presence of large uncontrolled outflows"), and (2)
**integral windup**, when the compensatory flux saturates and "the error … becomes constant and one
observes a steady increase in E without decreasing the error". Combining an inflow and an outflow
controller **antagonistically** (the insulin/glucagon arrangement) removes breakdown type (1) — *provided*
their setpoints are separated, `Aset_in < Aset_out`.

The 2025 preprint asks what happens *inside* that combination. Its findings, verbatim from the abstract:

- "Dependent on the controllers relative setpoints two types of compensatory flux regulations occur, which
  have been termed **delegated** and **isolated control**." In delegated control one feedback submits its
  entire compensatory flux and the other is the actual controller, neutralizing the excess; in isolated
  control one controller's flux is negligible and the other regulates alone.
- "A third control type is **metastable control**. Here, additions or removals of the controller variable
  can cause a **switch to the antagonistic partner's control regime**, but resets to its original control
  mode once additions or removals stop."
- "Integral windup can induce temporary metastable setpoint changes."
- The load-bearing parameter throughout is the **separation between the two setpoints**.

## Why this is not something we already embody

Checked against `~/.claude/.../memory/homeostasis-review-coverage.md` and the genome. Everything on the
homeostasis axis we carry is a **single-controller** read: allostatic load, Mahalanobis joint dysregulation,
CDP lower-variability border, CSD, reactive scope, requisite variety, Ashby trials-to-stable-field
(`ULTRASTABLE-EXHAUSTED`), settling-vs-setpoint (`regulator_verified`), Good-Regulator disturbance model.
Every one of them asks a question *about one regulator*. **None can pose the question of a PAIR** — which of
two opposed controllers is currently in control, whether control is being handed back and forth, or how far
apart their setpoints sit. `grep -n "antagonis\|futile\|windup\|control mode" scripts/mesh-*` returns
nothing on this. Rheostasis was on the still-open list; this is the mechanism *underneath* it (the preprint
derives rheostasis as an emergent property of the interacting pair).

## The mesh instance: `scripts/mesh-pace` is an antagonistic pair and did not know it

`mesh-pace` is the spend governor. Its `eff_gap()` (`scripts/mesh-pace:172`) has **two opposed branches on
one controlled variable** (paid burn/h):

| branch | condition | action | motif |
|---|---|---|---|
| cold-shrink | `burn < COLD_BELOW` (7/h) | floor the gap to `MIN_GAP` = **60s** | **inflow** — adds work-creation flux |
| hot-stretch | `burn >= 7/h` (`burn_mult`, `:87`) | stretch base by 1.5×/2×/3× → **27000s** at the first step | **outflow** — removes flux |

Their setpoints are **the same number**. The file's own header states the coincidence as a feature
(`:43-45`: *"7 = the first hot-staircase step, so cold ends exactly where stretch begins — no flat-base band
survives between them"*). Ruoff's result says a **zero-separation** antagonistic pair is precisely the
configuration in which neither controller can hold delegated control — there is no dead band, so every
crossing of 7/h hands the variable to the antagonist. And the handover is not gentle: the controller output
jumps **60s ↔ 27000s, a ~450× discontinuity in released cadence at a single threshold with zero hysteresis**.

Distinct from the two reads already on the file: `--burden` (Ziegler 2026) reads the *trend* against the
gain's lag; `--runway` (McShaffrey & Beer 2026) projects the $-transient against the cap. Neither asks which
branch is in control.

## What shipped — `mesh-pace --control-mode` (report-only)

The **measurement half only**, matching `--burden`/`--runway`: it never changes `eff_gap` or the gate.

`control_mode_state()` reconstructs the governor's own input — paid burn/h = paid (`anthropic`) turns in the
trailing `CM_RATE_H`(5)h window ÷ 5, the same quantity `paid_burn_per_h()` reads from the labour ledger — at
`CM_STEP_S`(900s) steps across `CM_HOURS`(24h) of `~/.mesh/spend.log`, labels each sample COLD/HOT by the
**live** `COLD_BELOW` setpoint, and counts regime **crossings**:

- `ISOLATED-COLD` / `ISOLATED-HOT` — 0 crossings; one branch regulated alone, the other's flux negligible.
- `SWITCHING` — 1–2 handovers; a real burn transition, not yet chatter.
- `METASTABLE` — ≥ `CM_META`(3) handovers; the pair is trading control across the 450× discontinuity.
- `UNKNOWN` — fewer than `CM_MIN_SAMPLES`(8) samples, or no paid tape. Never a fake `ISOLATED` off a stub.
- `DISABLED` — `MESH_PACE_RESERVE=0`; `eff_gap` returns the flat base, neither branch exists, so there is no
  pair to be in a mode.

It also prints the setpoints, their **separation** (currently `0/h` — the finding as a number), and the gain
swing `60s↔27000s`. Added to `--status`. One awk pass, no `mesh-labor` call: the whole suite still runs in
**0.47s**, inside `mesh-doctor`'s 12s `--test` timeout.

**Honest limits stated in the code**: this is a *reconstruction* from the turn tape, not a recording of what
`eff_gap` actually returned (the governor keeps no such history) — a sample is what the cold/hot split *would
have been* on that tape.

## Live result on mesh-home

```
$ mesh-pace --control-mode
control-mode: ISOLATED-COLD · crossings=0/97 samples · now=COLD · setpoints cold<7/h hot>=7/h sep=0/h ·
  gain 60s↔27000s — the INFLOW branch (cold-shrink to MIN_GAP) regulated alone all span

$ MESH_PACE_CM_HOURS=168 mesh-pace --control-mode   → ISOLATED-COLD, crossings=0/673
$ MESH_PACE_CM_HOURS=480 mesh-pace --control-mode   → METASTABLE,    crossings=8/1921
```

So the risk is **not theoretical**: over the 20-day tape the pair handed control across the 7/h boundary
**8 times** — roughly once every 2.5 days, each handover a 450× swing in released cadence. It simply has not
fired in the last week, because the mesh has been running cold throughout. A 24h-only read would have
reported a clean `ISOLATED-COLD` and hidden it; the span is a parameter for exactly that reason.

## Gates (RED-first, mutants run from a scratch copy)

Three fixtures drive the real `control_mode_state` — only the tape and the span are injected, no override
short-circuits the classifier:

| fixture | tape | expected |
|---|---|---|
| (a) | 1 paid turn/h over 30h → burn 1/h | `ISOLATED-COLD`, 0 crossings |
| (b) | 10 paid turns/h over 30h → burn 10/h | `ISOLATED-HOT`, 0 crossings |
| (c) | 50-turn bursts at −23h/−15h/−7h | `METASTABLE`, ≥3 crossings |

plus: the two ISOLATED modes must be **distinct** verdicts; a 1h span → `UNKNOWN`; `RESERVE=0` → `DISABLED`.

Mutants, each copied to a scratch dir and **seen RED** (`exit=1`) before this shipped:

| mutant | effect | leg that went RED |
|---|---|---|
| m1 | crossing counter pinned to 0 | (c) read `ISOLATED-COLD` → RED |
| m2 | regime hardcoded `HOT` (burn ignored) | (a) read `ISOLATED-HOT` → RED |
| m3 | classifier always returns `UNKNOWN` | all three → RED |

## What stays HELD

The **fix** — separating the two setpoints so the pair gets a dead band / hysteresis, and a burn hovering at
7/h stops swinging the cadence 450× — is a **spend-behaviour** change. It stays the operator's call, exactly
as the pacing knob and the anticipatory pre-stretch do (`--burden`, `--runway` are report-only for the same
reason). Measurement before the actuator.

## Files

- `scripts/mesh-pace` — literature block, `control_mode_state()`/`control_mode_line()`, `--control-mode`,
  `--status` line, 7 new `--test` legs.
- this doc.
