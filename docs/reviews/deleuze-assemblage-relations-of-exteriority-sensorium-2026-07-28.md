# Assemblage — relations of exteriority vs interiority (Deleuze & Guattari / DeLanda)

*Live literature review, 2026-07-28. Cross-domain transfer to a distributed sensor mesh.*
*Landed: `scripts/mesh-sensorium --exteriority` (report-only, additive, uncommitted for steward).*

## The concept

The **assemblage** (*agencement*) is Deleuze & Guattari's name for a whole whose properties
emerge from the interaction of heterogeneous parts, defined not by what it *is* but by what it
can *do*. Its **defining formal property** — the one that separates an assemblage from an organism
or a totality — is that its components stand in **relations of exteriority**:

> "A component part of an assemblage may be detached from it and plugged into a different
> assemblage in which its interactions are different." — DeLanda, *A New Philosophy of Society*

A part's identity is **not constituted** by its current links; it is self-subsistent and
re-pluggable. The contrary is a **relation of interiority**, where a part is co-constituted by the
whole and *cannot* be removed without both collapsing (the parts of an organism, a Hegelian
totality). DeLanda formalizes the assemblage on two axes: **material ↔ expressive** (the role a
component plays, from doing physical work to purely signifying) and **territorializing ↔
deterritorializing** (stabilizing vs destabilizing the assemblage's identity).

**Sources** (re-surveyed current, 2025–26):
- Deleuze & Guattari, *A Thousand Plateaus* (1980).
- Manuel DeLanda, *A New Philosophy of Society: Assemblage Theory and Social Complexity* (2006);
  *Assemblage Theory* (Edinburgh UP, 2016).
- Survey: [grokipedia — Assemblage (philosophy)](https://grokipedia.com/page/Assemblage_(philosophy));
  Ball, [*Parrhesia* 29](http://www.parrhesiajournal.org/parrhesia29/parrhesia29_ball.pdf);
  Understanding Society, [Assemblage theory as heuristic](https://undsoc.org/2016/02/11/assemblage-theory-as-heuristic/).

## Where we'd been — and the gap

The D&G lineage is already well-worked in the genome: **deterritorialization coefficient**
(`mesh-novelty --territory`), **inclusive disjunction** (`mesh-situation`), **order-word
redundancy** (board), **smooth/striated** (the mesh itself). And `mesh-sensorium --balance`
embodies Vervaeke's efficiency↔resiliency by measuring **streams-per-category**: how many
independent cached streams back each percept — the redundancy of the **producers** feeding one
fusion.

**Not embodied:** the *defining* property of the assemblage — relations of exteriority — and it is
the exact **consumer-side dual** of `--balance`. `--balance` looks **into** the sensorium (producers
per percept, resiliency). Relations of exteriority look **out**: for each cached stream, into how
many *other* assemblages is it re-plugged? A stream is only a genuine assemblage-component if it is
**detachable** — read by more than the pane that produced it.

## The transfer

`mesh-sensorium --exteriority` measures, for each of the roll-call's canonical cached streams, the
**consumer fan-out**: the count of *distinct other tools* that re-plug the stream (reference its
basename). The two aggregators (`mesh-sensorium`, `mesh-dash`) are **named-excluded** — they read
~every stream, so counting them would mask everything as detachable. Bands:

| refs (incl. producer) | class | reading |
|---|---|---|
| ≥ 3 | **EXTERIOR** | producer + ≥2 consumers — detachable, re-plugged across assemblages, robust to any one consumer dying |
| 2 | **WELDED** | producer + 1 consumer — a **relation of interiority**: a 1:1 coupling that *looks* modular but is co-constituted; either end dying orphans the other |
| 1 | **EXPRESSIVE-ONLY** | producer only — a pure sign that drives nothing downstream |
| 0 | **NOT-PRODUCED** | no tool references it — the pane reads a stream with no visible producer |

Report-only. No verdict, weight, or `.state` is touched (like `--balance`, `--levels`,
`--territory`). Exit codes: `0` EXTERIOR · `3` INTERIORITY-PINNED · `4` EXPRESSIVE-DEADENDS · `2` no
streams.

## The live finding (mesh-home, 2026-07-28T12:02Z)

```
streams: 12 exterior · 1 welded · 5 expressive-only · 1 not-produced  (of 19)
posture: EXPRESSIVE-DEADENDS — 6 stream(s) re-plugged by no other tool
```

- **`.watchtower-state.reach` — NOT-PRODUCED.** The `--cached` roll-call reads it, but **no tool in
  the toolset writes it**. The pane reads a stream with no visible producer — a dead or externally-fed
  cache. The strongest finding: a sign consumed with no source.
- **`.interruptibility.state` — EXPRESSIVE-ONLY**, and it is the **sole** COORDINATION stream
  ("*when may the mesh speak/alert?*"). Its cache is re-plugged by no other tool — yet the **sense**
  `mesh-interruptibility` *is* live-consumed by `mesh-precision` and `mesh-physical-context`. So the
  cached component is **welded to the pane** while functional consumers **pay to re-probe the sense
  live**. Same shape for `.media-scene.state` (cache unread; `mesh-media-scene` live-consumed by
  `mesh-operator-mood`).

## The honest caveat (in the `--balance`-caveat spirit)

This measures coupling of the **cached artifact** at **file granularity**. A consumer that re-invokes
the **sense live** (calls `mesh-<x>`) instead of reading its cache is **deliberately not counted**.
That is not a blind spot — it is the point: a cache classed EXPRESSIVE-ONLY *whose sense is
nonetheless live-consumed* is the interiority finding **sharpened**. The cached stream is a relation
of interiority (welded to the pane), while the sense keeps its exteriority via live calls — and every
live call is the **efficiency loss** the RR `--balance` frame exists to watch (a warm cache exists,
consumers bypass it and pay the live probe). The remedy a mesh would draw from this is: point the
live consumers at the cache, or retire the unread cache — either way the reading is actionable.

## The gate (RED-first verified)

`mesh-sensorium --test` drives the real `--exteriority` black-box against a **crafted toolset**
(`MESH_BINDIR`) with known reference counts, pinning three postures + per-line bands so no hardcoded
verdict passes: empty toolset → EXPRESSIVE-DEADENDS/exit4; every stream ref'd by 3 tools →
EXTERIOR/exit0; by 2 → INTERIORITY-PINNED/exit3; per-line `.perimeter.state` at refs 3 → EXTERIOR,
`.op-home.state` at refs 1 → EXPRESSIVE-ONLY. **Falsified:** flipping the EXTERIOR band `≥3 → ≥99`
turns the exit0 case RED (`got rc=4: EXPRESSIVE-DEADENDS`); restored → green. `smoke-test: ok`.

## Distinctness

Not a duplicate of prior landings. Distinct from `--balance` (producer-side resiliency, not
consumer-side detachability), from `mesh-precision --independence` (Kish n_eff measures whether
inputs are *correlated/redundant*, not whether a stream is *re-pluggable*), and from `mesh-doctor`'s
orphan check (finds unrun *producers*; this finds unread *streams* — the consumer-side orphan).
Verdict-preserving and additive, so it needs no sign-off.
