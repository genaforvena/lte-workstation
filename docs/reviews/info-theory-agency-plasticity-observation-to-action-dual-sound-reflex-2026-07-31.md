# Info-theory-of-agency review — PLASTICITY, the observation→action dual of empowerment

**Date:** 2026-07-31 · **Lane:** LITERATURE (live review) · **Seam:** information theory of agency
(empowerment / predictive information) · **Angle:** a critique/failure mode of the seam.

## The gap

Every information-theoretic agency measure the mesh embodies runs **one direction — action → world**:

- `mesh-algedonic` AGENCY_INFO = open-loop empowerment `MI(action; Δpain)`; CL_UNDERCOUNT/CL_INFLATED =
  process/closed-loop empowerment `I(action; Δpain | band0)`.
- `mesh-precision --num pred_info` = predictive information `I(past; future)`.
- `mesh-cooscillate` = transfer entropy (also action→other, or stream→stream).
- `mesh-vitality action_occupancy` = Maximum Occupancy Principle (action entropy).

All of these ask **"does the agent's action move the world?"** None asks the **dual**: *does the world's
observation move the agent's action?* That inward channel has a name.

## The concept (cited)

**Plasticity** — "the observation-to-action mirror of empowerment" — is the **inward directed
information**

```
    Plasticity  =  I( O^{T-1} → A^{T} )  =  Σ_t  I( O_{t-1} ; A_t | A^{t-1} )
    Empowerment =  I( A^{T}   → O^{T} )  =  Σ_t  I( A_t     ; O_t | O^{t-1} )
```

— "realized inward evidence that changes action," the exact transpose of empowerment's "realized
outward control." Named and formalised in **Richard Csaky, *Prediction and Empowerment: A Theory of
Agency through Bridge Interfaces*, arXiv:2605.06346v1 (May 2026)**, §6, crediting the plasticity notion
to **Abel et al., 2025**.

**The failure mode it diagnoses — and empowerment structurally cannot.** Csaky: a system can carry
**high empowerment while possessing low plasticity** — "a narrow interface can spend capacity on easy
outward control, leaving little capacity for evidence." An agent that *controls* effectively but whose
action is **not a function of what it observes**. Empowerment reads that agent as maximally agentic; it
is a **rock rolling downhill** — high outward effect, zero inward responsiveness.

## Why this is OUR failure mode, exactly

The plasticity=0 pathology is the CLAUDE.md **silent-fallback / hollow-sense** doctrine restated in
information theory. The canonical mesh incident (f51e36d): `mesh-room-music`'s beat detector raised under
a numpy-less python3, `|| echo 500` swallowed it, and the "beat-driven" grinder ran flat for weeks — the
mp3s looked fine; only the params log (`beat 500`, every line) showed the axis was dead.

In these terms: the grinder kept **full empowerment** over its output (it rendered audio, controlling the
sound) while its **plasticity collapsed to zero** — the recipe stopped being a function of the observed
beat. `mesh-sound-reflex`'s own header already fears exactly this, in prose: the recipe must be *"DERIVED
FROM THE RECORD… NOT random-within-absent (nothing connects the recipe to the material)."* That is the
plasticity claim — currently **asserted, never measured on the live channel.**

## The proposal — `scripts/mesh-sound-reflex --plasticity` (report-only)

**Target file:** `scripts/mesh-sound-reflex` (genome source). **Input:** `~/.mesh/room-music-params.log`
(1271 lines; each carries the OBSERVATION — `beat`, `band`, `fit`, `novelty`, `mode`, and the derive
axes — alongside the ACTION — recipe params `l w ss s c m pr rv sw rot pat`).

Add a live-channel plasticity estimator over a trailing window:

```
    mesh-sound-reflex --plasticity   # I(observed character ; chosen recipe) over the live params log
```

For each recipe axis A (length, width, stretch, cutoffs, mode) and the observation vector O
(beat_ms, band, fit, novelty), estimate `I(O; A)` on the trailing-N params-log rows, and emit a
report-only verdict per the honest-fusion convention:

- **PLASTIC** — `I(O;A) > null-p95` for the load-bearing axes: the recipe genuinely tracks the material.
- **HOLLOW** — `I(O;A) ≈ 0` while the axis is still *varying*: action decoupled from observation (a
  future f51e36d — the derivation function is fine but the LIVE input axis died upstream).
- **AXIS_DEAD** — the observation column itself is a constant over the window (`beat 500` every line):
  plasticity is *undefined*, and this is the loudest state — the sensor feeding the action is flat.

**Reuse the AGENCY_INFO estimator + its surrogate null.** The seam's live lesson (landed 2026-07-30) is
that plug-in MI is positively biased at finite N — a hollow channel reads PLASTIC on noise. Use the
**shuffled-observation surrogate** already built for algedonic (`mesh-algedonic` AGENCY_SURR, Panzeri-Treves
2007 / Miller-Madow 1955): permute O against A, take p95, subtract. Without it, `--plasticity` would be
the next hollow-MI-without-a-null site ([[a-rule-asserted-at-one-call-site-is-not-asserted]]).

**Why this catches what `--test` cannot.** `mesh-sound-reflex --test` is a **pure-function** gate
("character drives params") — it feeds the derivation function synthetic characters and checks the output
varies. That gate is **green forever even after f51e36d**, because the function is fine; it was the *live
input* that collapsed to a constant. `--test` measures the function; `--plasticity` measures the **live
channel** — the only place the flat-axis failure is visible. This is the doctrine's own distinction:
*"a `--test` MUST assert a real read produces data… a reachable phone whose driver returns empty is a
hollow sense."* Plasticity is that assertion for a derivation reflex.

## Scope / honesty

- **Report-only, seeded** (like the algedonic null and the PID proposal
  [[info-theory-agency-coverage]]) — it colours a verdict, never gates a render or blocks landing.
- **Doc-only proposal; NOT embodied in this pass** — same posture as the 2026-07-31 PID/`mesh-motion-fuse`
  entry. The estimator + null are already in `mesh-algedonic`; wiring is a follow-up strand.
- **n is a sliding window** — `room-music-params.log` turns over; quote no fixed n, re-derive live
  ([[records-log-is-a-sliding-window]]).

## Not discarded — but two adjacent ideas that DON'T apply

- **Full bridge-interface capacity accounting** (Csaky §6, "widen the bridge / split channels") is an
  RL-architecture prescription for a *learning policy*, not a passive measure on a fixed stream — out of
  scope, like empowerment-gain-as-difference (arXiv:2512.08230) was.
- Plasticity is **distinct from** predictive information (`mesh-precision`): pred-info is `I(past;future)`
  of the *world*, agent-agnostic; plasticity is `I(observation→action)` of the *agent's own coupling*. A
  clock has maximal predictive information and zero plasticity — the measures separate exactly where the
  seam's known confound (predictable-but-uncontrollable) lives.

**Sources:**
- Richard Csaky, *Prediction and Empowerment: A Theory of Agency through Bridge Interfaces*,
  arXiv:2605.06346v1 (2026) — https://arxiv.org/html/2605.06346
- Abel et al., 2025 — plasticity as the observation-to-action mirror of empowerment (via Csaky §6).
- Panzeri & Treves 2007; Miller & Madow 1955 — finite-sample MI bias (the reused null).
