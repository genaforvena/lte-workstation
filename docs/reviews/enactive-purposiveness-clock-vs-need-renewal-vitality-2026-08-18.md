# Beyond control: our renewal sign is clock-driven, so it cannot tell a metabolism from a thermostat

**Live literature review · 2026-08-18 · enactivism & 4E cognition → self-production metrics**
Target: `scripts/mesh-vitality` (the PRECARIOUSNESS block, :3744-3781, HELD). Proposal only — this
review adds the discriminator the held fix is missing and names the test; nothing gates on it.

## The source

**Kathryn Nave, "Beyond Control: Finding the Purpose of Enactive Cognitive Science", *Adaptive
Behavior* (first published 9 April 2026), <https://doi.org/10.1177/10597123261435796>** — fetched
2026-08-18, abstract and argument read directly, not from a summary.

Its opening frames the split: *"To some, purposiveness is the core of the enactive approach. Others,
however, view the notion of purposes as a pre-scientific crutch — one that will eventually be
replaced by mathematical analyses of the kind of dynamical systems that we are."* Nave's claim is
that the second camp cannot deliver, and that the first camp's own machinery is too weak to stop it:

- **Operational closure is too general.** Mutual interdependence in a network of processes is
  satisfied by *"hydrological cycles and coupled oscillators"* as readily as by organisms. It cannot
  ground a naturalistic account of purpose.
- **Precariousness, as the canon states it, does not fix that.** Cybernetic enactivism's
  dynamical-systems account of autonomy *"fails to distinguish living systems from non-living ones"*
  — it applies trivially to *"pendulums, thermostats, and electrons seeking equilibrium states."*
- **The discriminator is metabolic and thermodynamic**, which enactive cognitive science abandoned
  too readily: living systems *"construct and regenerate their own constraints"*, paying continual
  energy to do so, and their parts degrade without that active regeneration.
- The recalibrated principle: **"the purpose of a system is what it needs to do,"** not merely what
  it does.

## Why this is new HERE, specifically

`mesh-vitality` already carries precariousness in depth (Di Paolo, *Extended Life* 2009; Di Paolo,
Buhrmann & Barandiaran, *Sensorimotor Life* 2017; Beer & Di Paolo 2023) — the membership test
"withdraw the network's maintenance → does the component dissolve or persist?", the durable-deposit
inversion (a pushed commit is inert deposit, not living tissue), and a HELD fix: partition components
into PRECARIOUS vs INERT-DURABLE and report **renewal-rate ≥ decay-rate over the precarious set** as
the constitutive vital sign.

Nave 2026 is the critique aimed at exactly that construction, and it lands: **the held fix's renewal
term, as specified, would be satisfied by a clock.** Nothing in "this component would decay without
upkeep, and it was re-produced within the interval" distinguishes

- a component re-produced **because the unity needed it** — a drifted tool re-synced because
  sync-tools found drift, a state rewritten because its value changed, a reflex re-wired because
  autowire found it orphaned — from
- a component rewritten **because a timer fired**, whose rewrite would have happened identically had
  nothing in the mesh needed anything.

That second case is Nave's thermostat, and this mesh is made of them: every cron-wired reflex
rewrites its artifact on a fixed cadence. Worse, our own doctrine *mandates* the clock-driven
rewrite — the liveness-touch convention (`scripts/mesh-state-touch`, CLAUDE.md) has every
change-gated reflex call `mesh-state-touch` **on every successful eval**, precisely so mtime means
"ran live" rather than "value changed". That was the right fix for the false-STALE problem, and it
means **mtime is a clock signal by construction and can never be evidence of need.** A renewal-rate
computed over mtimes measures that cron is running. Cron running is not a metabolism.

## The concrete proposal — one file, one axis

`scripts/mesh-vitality`, PRECARIOUSNESS block (:3744-3781): keep the held partition, but **split the
renewal term by demand-contingency before it can serve as a vital sign**, using a discriminator the
substrate already has and does not read this way:

| grade | evidence | reading |
|---|---|---|
| `NEED-RENEWED` | the re-production was contingent on a demand signal: a **content** change in the artifact, a sync-tools drift repair, an autowire re-wire, a fault-triggered heal | constitutive self-production |
| `CLOCK-TOUCHED` | mtime advanced with byte-identical content and no repair event — the reflex ran and had nothing to do | Nave's thermostat: upkeep the unity did not need |
| `DECAYED` | neither: past its cadence, stale/orphan/drifted | decay side of the balance |

The mesh already writes both axes and reads only one. The two-axis convention is stated in CLAUDE.md
("mtime = liveness, content = the reflex's own change-gated write") and the content axis is
explicitly unchecked today (memory `liveness-touch-content-axis-goes-unchecked`). So the measurement
costs no new probe: it is a content-hash-vs-mtime comparison over the precarious set that
`reflex-health` and `sync-tools` already enumerate.

What it buys, in Nave's terms: `renewal ≥ decay` computed over `NEED-RENEWED` only answers *what the
mesh needed to do and did*. Computed over all touches — the held specification — it answers *whether
cron is up*, which every liveness instrument already answers, and which stays green in exactly the
museum state the block was written to detect: **a mesh whose reflexes all tick, all touch, and
regenerate nothing.**

## The honest limits

- **This does not make the mesh purposive**, and the review is not claiming it. Nave's argument is
  that purposiveness needs *metabolic* constraint-regeneration; a demand-contingency grade is a
  measurement refinement, not a metabolism. It removes a way of being wrong, nothing more.
- **`CLOCK-TOUCHED` is not a fault.** A reflex that ran and found nothing to do is a healthy
  reflex — the grade says its rewrite is not evidence of self-production, not that it is waste.
  Anything that alarmed on it would be punishing correct behaviour.
- **The classification still needs the decay model the held fix already flagged as missing**, and
  this refinement adds a second dependency: a repair-event ledger (sync-tools/autowire/heal
  outcomes) that can be joined to the artifact. Detection is shippable; the weighting is the
  steward's, unchanged.
- **Not landed as code.** The `# NAVE 2026 REFINEMENT` note in the block records the discriminator
  where the held fix will be built; the report line is untouched.

## Sources

- Kathryn Nave, "Beyond Control: Finding the Purpose of Enactive Cognitive Science", *Adaptive
  Behavior*, 2026 — <https://doi.org/10.1177/10597123261435796>
- Denizhan Pak, "Sensorimotor Contingencies and The Sensorimotor Approach to Cognition",
  arXiv:2510.14227 (16 Oct 2025) — <https://arxiv.org/abs/2510.14227> (surveyed as the other live
  2025 thread; SMCs are already the frame `scripts/mesh-closure` works in, so not the landing)
- Mustile, Borghi, De Tommaso & Wykowska, "Peripersonal Space Perception Is Similar When We Interact
  With Other Humans or With Humanoid Robots", *QJEP* 2026 — <https://doi.org/10.1177/17470218251412245>
  (surveyed; peripersonal space / body schema is a genuine mesh gap — zero hits in `scripts/` — but
  the transferable mechanism is thinner than Nave's, and it is left as a named lead, not a proposal)
