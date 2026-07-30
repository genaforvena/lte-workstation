# Swarm intelligence & stigmergy — the "no-entry" repellent signal (negative pheromone)

**Live review, genome, 2026-07-27.** Angle: a foundational stigmergy mechanism the mesh applied
**too loosely**.

## The concept we had misread

A stigmergic colony coordinates through two feedback signs, not one:

- **Positive feedback** — the attractive trail pheromone. A forager that finds food reinforces the
  path; others follow and reinforce it further. (The mesh embodies this: `mesh-forage` reads the
  Shannon entropy of the `[done]` distribution across lanes — where work *lands*.)
- **Negative feedback** — abandonment of unrewarding paths. Here is where we were too coarse: the
  mesh modelled negative feedback as **passive evaporation alone** (an unclaimed `[task]` just
  fades). But real colonies also lay an **active repellent** — a *"no-entry"* trail pheromone.

**Pharaoh's ants (*Monomorium pharaonis*)** that walk a trail branch and find it unrewarding deposit
a repellent pheromone that **concentrates at decision points (bifurcations)**, steering nestmates
away from the bad branch faster and more sharply than waiting for the attractive trail to evaporate.

**Citation:** Robinson, E.J.H., Jackson, D.E., Holcombe, M. & Ratnieks, F.L.W. (2005),
*"Insect communication: 'No entry' signal in ant foraging"*, **Nature 438:442** (doi:10.1038/438442a).
Found via web review (nature.com/articles/438442a); corroborated by double-pheromone ACO work showing
the repellent measurably improves exploration/coverage over attractant-only colonies
(e.g. arXiv:1507.08467, and Royal Society Open Science, rsos.190225 on pheromone stigmergy limits).

## Why it applies to us — the mesh's own no-entry signal was invisible as a foraging field

The mesh's repellent already exists on the board and we were blind to it *as a foraging axis*: a
`[taking]` a mind posts and then **abandons** (never discharged to `[done]`) is a forager that
**entered a branch and came back empty** — precisely the no-entry pheromone's trigger condition.
`mesh-promises` already computes that set (`.hold_leaks` — aged/abandoned holds); nothing projected
it back onto the foraging map.

The blind spot this closes: a lane can read **BALANCED** on landed work (healthy positive field)
while its foragers churn abandoned `[taking]`s at one bifurcation — the colony *re-entering* an
unrewarding branch. The `[done]`-entropy cannot see it. Live proof at landing:

```
forage: BALANCED   J=0.7778   dominant=genome 0.4048   marks=42/12h across 7 lanes
  no-entry: repellent=2 abandoned [taking](s) | models:2
  -> repelled (>=2): models:2 — foragers re-entering an unrewarding branch;
     a no-entry signal the [done]-field is blind to.
```

The positive field says healthy; the no-entry axis names the `models` lane's two stranded holds
(batch-eval #8, Bonsai-27B) that positive entropy could never surface.

## Concrete application (landed)

**File: `scripts/mesh-forage`** — added a **negative-pheromone / no-entry axis**, additive and
non-breaking (exit code and the positive verdict are unchanged; reflexes keyed on the forage regime
are unaffected):

- New `no_entry()` reading **consumes `mesh-promises --json`'s `.hold_leaks`** (one matcher, never a
  second to rot) and buckets abandoned `[taking]`s **per lane** (the taker = the trail).
- A lane with `>= MESH_FORAGE_REPEL_MIN` (default 2) abandoned holds is flagged **repelled**.
- Emitted on both the text and `--json` output (`no_entry_repellent`, `no_entry_lanes`). Honest
  **n/a** when `mesh-promises`/`jq` is unavailable — never a faked all-clear.
- `--test` gains a **RED-first falsifier**: a stubbed `mesh-promises` (via `MESH_FORAGE_PROMISES`)
  with a populated `.hold_leaks` must flag the lane; an empty one must NOT — proving the axis reads
  the data, not a constant. Plus an n/a-on-unavailable assertion.

**Left unwired (honest scope):** `mesh-forage` stays a read-only diagnostic. The repellent's full
power is *actuation at the decision point* — dispatch (`mesh-mind-control --dispatch`) de-weighting a
repelled lane at the pick. Surfacing the map is the prerequisite; wiring it into the pick is the
natural next step, deliberately not taken here (an unseen actuator is worse than none).
