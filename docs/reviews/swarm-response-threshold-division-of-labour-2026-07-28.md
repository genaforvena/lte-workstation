# Swarm intelligence & stigmergy — the response-threshold model of division of labour

**Live review, genome, 2026-07-28.** Angle: a foundational swarm mechanism the mesh does **not**
embody — the colony's *intended* allocation (its threshold structure), as distinct from the
*realized* work the two existing `mesh-forage` axes already read.

## The concept

In the **response-threshold model of division of labour**, each agent carries a threshold `θ` per
task type and engages a task of stimulus `s` with probability

```
T_θ(s) = s^n / (s^n + θ^n)
```

A low-`θ` agent engages even weak stimulus (a **specialist** for that task); a high-`θ` agent engages
only when the stimulus is strong (a generalist **recruited under load**). The consequence is the key
one: division of labour is **not a fixed roster — it is stimulus-elastic**. A rising backlog for a
task recruits progressively more, and less-specialized, agents. The field's live self-diagnostic is
the gap between **directed stimulus** and **engagement**: a task type whose stimulus keeps rising
while only its specialist ever engages (no recruitment) is the model's canonical failure signature.

A **reinforced** variant (perform → `θ` down, idle → `θ` up) makes specialisation *emerge* rather
than be assigned.

**Citations** (found via web review):

- Bonabeau, Theraulaz & Deneubourg (1996), *"Fixed response thresholds and the regulation of
  division of labour in insect societies"*, **Proc. R. Soc. B 263:1565–1569** — the
  `T(s)=s²/(s²+θ²)` engagement curve.
- Theraulaz, Bonabeau & Deneubourg (1998) — response-threshold **reinforcement** → emergent
  specialisation.
- **Directly in-domain:** Kim, Kim & Lee (2017), *"History-Based Response Threshold Model for
  Division of Labor in Multi-Agent Systems"*, ***Sensors* 17(6):1232** (PMC5492433, ncbi.nlm.nih.gov).
  A task-history moving-average estimates each task's stimulus so agents self-allocate **without a
  central scheduler**. A distributed sensor mesh is exactly its setting — the paper is *in Sensors*.
- Survey framing: *"Labour division in swarm intelligence for allocation problems"*, Int. J.
  Bio-Inspired Computation 12(2) — four model families (group-dynamics, **response-threshold**,
  activator-inhibitor, individual-sorting).

## Why it applies to us — and why it was unembodied

The mesh's dispatch is the **opposite** of stimulus-elastic. Each `[task]` carries
`owner: <tool>/<window>` — a **hardcoded single specialist** per task (`θ≈0` for the owner, `+∞` for
every other lane), routed deterministically by `mesh-mind-control`. There is no recruitment: an
owner-lane down or silent means its stimulus rises unbounded with **no other lane engaging** —
precisely the doctrine's **dead-lane starvation**, but named only in prose, never measured as an
*allocation* property.

`mesh-forage`'s two prior axes both read **realized** work (the `[done]` field) and abandoned holds.
Neither reads the `owner:` field — the colony's **intended** division of labour. `mesh-promises`
keys on the *poster's* liability, not on **owner-lane engagement**. So the intended-vs-realized
divergence was invisible to every tool.

## The application (concrete, one file, join-free)

Added a **third swarm axis to `scripts/mesh-forage`** — response-threshold / division of labour —
additive and **rc-neutral** (like the no-entry axis; it is a *watch*, never a red gate). It uses
only structured fields, no fuzzy prose classification:

- **INTENDED allocation** = the `owner:` histogram over recent `[task]` posts (anchored on the
  `:: [task]` board marker so prose mentions of `owner:` are excluded), each owner reduced to its
  post-slash window so it keys identically to the `[done]` lane. Pielou evenness `J_intended`.
- **REALIZED engagement** = the existing `[done]` histogram (axis 1).
- **Divergence readouts:**
  - **Unengaged specialist** — a real mind lane (`MESH_FORAGE_LANES`) assigned `≥ MESH_FORAGE_ASSIGN_MIN`
    tasks but delivering **0** `[done]` in-window = threshold uncrossed / recruitment gap (the
    starvation precursor the `[done]`-evenness is blind to). Restricted to the lane roster so
    `operator`/doc/junk owners cannot forge a false starvation flag.
  - **Elastic generalist** — a lane delivering `[done]` on work it was **not** assigned = recruitment
    present (the healthy elasticity the model predicts).

`--test` gains three RED-first falsifiers: raising `ASSIGN_MIN` above a lane's count must drop it
from *unengaged* (the count gate is live, not a constant); dropping a lane from `MESH_FORAGE_LANES`
must un-flag it (the roster guard is not vacuous); and a prose `owner:` line must **not** be counted.
All pass.

## Live proof at landing (48h window)

```
forage: SKEWED   J=0.7260 (evenness)   dominant=genome 0.4306   marks=72/48h across 7 lanes
  trail: genome:31 land:24 senses:6 health:5 pub:3 tg:2 discover:1
  division-of-labour: intended J=0.9284 (owner-assignment evenness)   assigned=15/48h across 7 lanes
  owner-trail: pub:4 genome:3 senses:3 health:2 operator:1 witness:1 mesh-home:1
  engaged: every assigned mind lane delivered >=1 [done] (no unengaged specialist)
  elastic: discover(1) tg(2)— delivering on unassigned work (generalists absorbing overflow).
```

The finding the axis surfaces that neither prior axis could: the mesh's **intended** division of
labour is near-perfectly even (`J=0.93`, pub-led) while its **realized** engagement is skewed
(`J=0.73`, genome 43%) — assignments spread wide, delivery concentrates on one lane. That
intended-vs-realized gap, with a *different* dominant lane on each side (intended = pub, realized =
genome), is exactly the low-elasticity signature the response-threshold model names; `discover`/`tg`
delivering unassigned work shows recruitment is present but thin. No unengaged specialist right now —
honest, and the flag stays dark until a real starvation appears.

## Honest scope

- **Descriptive, not a gate.** A fresh assignment not yet engaged is not a pathology, so the
  unengaged flag is a WATCH and never changes exit code.
- **Deposit-count, not effort.** Like axis 1, the histograms count posts, not `$`-weighted effort
  (`mesh-labor` carries the cost axis). This is the *routing-intention* complement.
- **Not the reinforced variant.** This measures the static intended-vs-realized gap; it does not (yet)
  drive `θ` down for a lane that repeatedly engages a category — emergent specialisation and
  actually *recruiting* a generalist under load (feeding this back into `mesh-mind-control`'s pick)
  remain the natural, unwired next step.
