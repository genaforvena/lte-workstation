# Agency gain: the correlation miner could not tell its own hand from the world

**Live review** — information theory of agency (empowerment / predictive information), angle = a known
**failure mode** of the area. Landing site: `scripts/mesh-correlate` (PREDICTION lane).
2026-08-19, genome. Uncommitted; steward lands.

## The source (live, current)

**Evan Ye, "From Prediction to Self: Developmental Conditions for Agency in Minimal Neural Systems",
arXiv:2606.05605 (cs.LG; cs.NE), submitted 4 June 2026** — <https://arxiv.org/abs/2606.05605>.

Read: abstract + listing. Ye traces a 192-dimensional GRU through **40 controlled experiments** arranged
as a developmental sequence, adding one component at a time and asking at each step whether the system
can distinguish **self-caused from world-caused** change. Four conditions must hold **in strict order**:

1. persistent state forming stable attractors,
2. **a causal action loop linking output to input**,
3. proprioceptive feedback that makes implicit causal knowledge explicit,
4. asynchronous awakening — perceptual learning must consolidate before action learning begins.

The metric proposed to track the transition is **agency gain**:

> **A = Err_world − Err_self** — "the predictive advantage of knowing one's own action."

The self-aware predictor beats the self-blind one across periodic (sinusoidal) and chaotic (Lorenz)
environments, and the metric survives ablation of every auxiliary component. Only forward-sampled action
selection produces meaningful gain; two gradient-based alternatives degenerate. The paper also publishes
**12 falsified hypotheses** mapping where development stalls — the load-bearing one here being that
**predictive coding alone does not produce self-representation**. A predictor can be arbitrarily accurate
and still have no idea which of its inputs it caused. (Working draft, explicitly inviting feedback.)

## Why this is new ground for us (checked first — this seam is worked hard)

Thirty-odd prior reviews under `docs/reviews/info-theory-agency-*`, `…/fep-*`,
`…/predictive-processing-*`: open-loop vs process empowerment, channel capacity vs achieved flow,
per-factor empowerment, discounted (EELMA) empowerment, multi-agent interference-channel empowerment,
MI finite-sample bias and its surrogate null, relevant information, crypticity, PID synergy, semantic
information, plasticity, interface empowerment and the overwrite/identification separation
(Csaky arXiv:2605.06346, landed twice — 07-24 and 08-19), and corollary discharge as a **timing hub**
(`mesh-audio-active`, 08-14).

The nearest neighbours and why they are not this:

- **Overwrite vs identification** (07-24) is a *separation theorem* about how a prediction objective can
  be satisfied by the agent's own action. It named the shape. It did not give a **number** anyone could
  compute per candidate, and it landed on `mesh-promises`, not here.
- **Corollary discharge** (08-14) is the self/other split in the *audio* organ, where a reafference flag
  already existed. It is about the *timing* of a known self-signal, on an organ that has one.
- **Empowerment**, in every prior form, asks *how much control do we have* — channel capacity, a
  maximisation over a policy. It has been **held since 2026-07-05** inside `mesh-correlate` itself on the
  stated grounds that there is "no actuator-firing record on the sensor tape".

Agency gain asks a different and much cheaper question: **is this finding about the world, or about our
own hand?** No capacity, no policy, no maximisation — the *same lookup predictor run twice*, once blind
to our actuation and once seeing it. That is why it lands now, where empowerment still cannot.

## The defect it names, in our code

`~/.mesh/sensor-tape.tsv` carries **17 sense columns and zero action columns**. `mesh-correlate`'s
PREDICTION lane mines it for `A_t → B_{t+1}` regularities and emits the best one as a hypothesis to the
idea queue. Ye's condition (2) — a causal action loop from output back to input — is therefore
**structurally absent**, and the lane is **self-blind by construction**.

The consequence is concrete, not hypothetical. When `mesh-room-music` plays a mix into the room,
`room_sense` / `room_activity` / `tempo` / `ambient` move **because we moved them**. The resulting
regularity is reafference wearing a sensor's name — exactly the shape of this lane's already-known clock
confound (the *hour* wearing a sensor's name, 2026-07-25), and it gets the same answer: make the confound
**compete as a baseline** rather than argue about it.

And the blocker the empowerment note recorded was **true of the tape and false of the node**:
`~/.mesh/room-music-sent.log` is a dense, ISO-timestamped ledger of every mix this mesh actually played,
spanning the tape's own window. It was there to be read the whole time.

## What shipped (`scripts/mesh-correlate`)

1. **A self-actuation channel.** `_self_channel()` folds the node's real actuator ledgers
   (`room-music-sent.log`, `state-voice.log`) into a rows-aligned token — did the mesh **ACT** during
   `[ts_k, ts_k+1)` — with an **explicit source alphabet**: an unrecognised log basename is **refused
   loudly**, never matched by a permissive default (a default that counted every line of some heartbeat
   log as an actuation would make the mesh look permanently busy and mute this lane entirely).
2. **A SELF baseline** in the PREDICTION lane, beside majority-class / persistence / hour: predict
   `B_{t+1}` from *our own actuation alone*. If knowing only that **we** acted predicts the target as well
   as the candidate sense does, the "leading indicator" is our own hand coming back through a sensor and
   cannot clear the margin. This is the behavioural change.
3. **Agency gain reported** on every emitted finding — `A = Err_world − Err_self`, both measured on the
   same actuator-covered subset. **Null-corrected, and that is not optional**: adding *any* second
   variable to an in-sample lookup can only lower in-sample error, so a raw gain is `≥ 0` by construction
   and would accuse every finding of reafference. The null is a **shuffled** self channel through the
   identical two-variable lookup, and the reported `A` is the excess over it. Signed, never floored.
4. **`mesh-correlate --agency`** — report-only per-pair dump (`acc`, all four baselines, the gain) plus
   the channel's coverage. One definition (`_agency_gain`) serves both the dump and the emit path, so the
   number a human reads and the number that gates cannot drift apart.

### Honesty rules the block is written to (doctrine)

- **Missing evidence renders `na`, never `0`.** An absent or unreadable actuator record must not read as
  "we did nothing" — that is a fabricated innocence, the reboot-reset-counter-read-as-calm shape.
- **Coverage is published beside the value** (`88% covered`), and rows outside the record's own span are
  `None`, not `SILENT` — unknown is not silence.
- **A self-silent window is named**, not rendered `agency=0.00`: "we never acted" and "acting explained
  nothing" are different claims and must not be the same string.
- **The banner is rare and loud** — printed only when the axis is `na`, self-silent, or under `--agency`;
  the live value already travels inside every finding's `agency=` string.
- **Turning the knob off changes what the lane DOES, never what it can SAY.** Caught during the work:
  wiring the *reported* gain to `SELF_BASE_ON` made `CORRELATE_PRED_SELFBASE=0` print
  `agency=na (684 actuations, 88% covered)` — an `na` whose stated cause named the live channel it was
  not about. Reporting is now independent of the baseline knob; the finding says
  `(NOT competing — CORRELATE_PRED_SELFBASE=0)` instead.

### The subtlety that would otherwise mislead

**Gain and baseline answer different questions, and the gain is the weaker one.** Ye's `A` is
*incremental* — what our own hand adds **on top of** the candidate sense. In the worst case, and the one
this lane actually faces, the candidate *is* a proxy for our hand, so `A` collapses to ≈0 **precisely
because the reafference is total**: `A_t` already carries everything `SELF_t` would have told us. The
tool's own reafference fixture reads `acc=1.000, self=1.000, agency=+0.000`. **A small `A` is not a clean
bill of health.** The suppression is done by the self-alone baseline (*sufficiency*), never by `A`
(*increment*). Both are reported for that reason; read them together or not at all.

## Artifacts

**Gate seen RED then GREEN** (a gate never seen fail is not a gate). Fixture: 60 ten-minute rows in which
our own actuation alternately fires (a planted `room-music-sent.log`), `ambient_{t+1}` is LOUD exactly
when we acted at `t`, and `tempo_t` tracks our acting — a **perfect 100%** "leading indicator" that is
entirely our own hand. Ten-minute spacing, not hourly, so the *hour* cannot stand in for the actuation:
this must be caught by the SELF baseline, not the clock baseline.

```
red half  (CORRELATE_PRED_SELFBASE=0) : PREDICTION emitted — 100% vs 51% baseline, perm-p 0.001
green     (default)                   : suppressed
--agency                              : #agency tempo->ambient T=59 acc=1.000 maj=0.508 pers=0.000
                                        clock=0.508 self=1.000 agency=+0.000
```

Two source mutants, both **red** (`rc=1`):

- `SELF_BASE_ON=False` hard-coded → the reafferent 100% predictor is emitted as a world hypothesis.
- `agency=na (…)` replaced with `agency=0.00` → the absent-record leg catches the fabricated innocence.

Full suite green: `bash scripts/mesh-correlate --test` → `smoke-test: ok (… REAFFERENCE: a 100%
self-caused predictor is suppressed by the SELF baseline + red-half falsifier, --agency publishes
coverage and reports the same one definition, absent record renders na-with-cause (never 0.00), unknown
actuator log refused loudly)`.

**Live AFTER read**, real tape (3021 rows, 2026-07-14 → 2026-08-19), real ledgers:

```
agency-gain: self-channel 685 actuations, 88% covered → live
88 pairs measured
self baseline is the strict maximum on:  0 pairs
largest agency gain:  +0.026  tempo->light   (+0.012 room_activity->light, +0.012 tempo->desk)
```

**Read this honestly.** The axis is live and reads real numbers, and what it currently says is that on
*this* window the emitted-hypothesis stream is **not measurably reafferent** — persistence dominates
nearly every pair, and our own actuation buys at most +0.026 over its own null. That is information, not
a null result: the guard is now instrumented and its reading is `~0` rather than *unknown*. It is also
not a permanent verdict — `room-music-sent.log` is a live ledger and the sound lane's cadence changes.

## What this does NOT do

- It does **not** build the actuator-side empowerment metric held since 2026-07-05. No channel capacity,
  no maximisation over a policy, and the closed-loop caveat recorded there still binds whoever does. It
  removes the stated blocker ("no actuator-firing record") and nothing more.
- It does **not** add an action column to `~/.mesh/sensor-tape.tsv`. The channel is derived at read time
  from the node's own ledgers, so nothing rotates the tape and no alignment invariant is touched. Putting
  actuation **on** the tape remains the deeper fix, and is the one Ye's condition (2) actually describes.
- It covers **two** actuator sources. The mesh has more hands than that (`mesh-act`, `mesh-tv-dlna`,
  `mesh-sms`, the phone TTS path). Each must be added to `_SELF_MATCH` **deliberately**, with a predicate
  that knows which of its lines are actuations — which is why the unknown-basename refusal is a gate and
  not a warning.

## Sources

- [Evan Ye, *From Prediction to Self: Developmental Conditions for Agency in Minimal Neural Systems*, arXiv:2606.05605 (4 Jun 2026)](https://arxiv.org/abs/2606.05605) — the landing source.
- [R. Csaky, *Prediction and Empowerment: A Theory of Agency through Bridge Interfaces*, arXiv:2605.06346](https://arxiv.org/abs/2605.06346) — already embodied (07-24, 08-19); checked for overlap.
- [Tiomkin, Salge & Polani, *Process empowerment for robust intrinsic motivation*, J. Phys. Complexity 6 035011 (2025)](https://iopscience.iop.org/article/10.1088/2632-072X/adf2ec) — the held empowerment note this updates.
- [Wang et al., *ELDEN: Exploration via Local Dependencies*, arXiv:2310.08702](https://arxiv.org/pdf/2310.08702) — surveyed, not landed (its "empowerment controls the easiest-to-manipulate variable" critique is already embodied as per-factor empowerment, 2026-08-18).
- [*Intrinsic Motivation as Constrained Entropy Maximization*, arXiv:2502.02962 / Entropy 27(4) 372](https://doi.org/10.3390/e27040372) — surveyed, not landed (unifying frame, no per-candidate quantity).
