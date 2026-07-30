# Live-literature review — Deleuze & Guattari: SMOOTH vs STRIATED space, and the intensive residual a striated band effaces

Date: 2026-07-27 · lane: genome (idea-queue LITERATURE task — D&G, a recent 2023-2026 angle) · status: fix in tree, uncommitted

## Where we had already been (so this doesn't double-count)

Deleuze & Guattari is a well-worked mesh seam. Before landing I confirmed the embodied set:

- **rhizome / plane of consistency** (open, self-declaring sense-plane) → `scripts/mesh-sensor-tape`
- **desire as productive force / productive forage / rhizomatic coupling** (Anti-Oedipus) → `scripts/mesh-needs`
- **assemblage — degree of territorialization (DeLanda)** AND **capacity-to-affect asymmetry (Atkinson,
  TCS 2024)** → `scripts/mesh-digest`
- **cognitive assemblages (Hayles)** → `scripts/mesh-pane-consume`
- **the refrain / ritornello** → `scripts/mesh-reflex-health`
- **societies of control / modulation-harms (Deleuze; Burdon & Cohen)** → `scripts/mesh-operator-mood`
- **assemblage & non-human agency** → `scripts/mesh-window-state`

Rhizome, assemblage, territorialization, capacity-asymmetry, refrain, desire-production, control-modulation
are all landed. What is **not** embodied is the **nomadology** pair of *A Thousand Plateaus* plateau 14.

## The concept not yet embodied — SMOOTH vs STRIATED space

D&G (ATP, "1440: The Smooth and the Striated"): **striated** space is **metric and gridded** — fixed
global coordinates, everything comparable on one scale; **smooth** space is **vectorial and intensive** —
continuous, local, ordinal-not-cardinal. The two exist only in mixture and constantly convert into each
other; striation enables control and comparison but **effaces the intensive difference**.

### Live sources (read 2026-07-27 — a RECENT angle, not the 1980 text alone)

- **Baron, "Representation and Interpretation of Multi-Agent Systems through Deleuzian Thought", JCoDe:
  Journal of Computational Design 6(1), 2025** — a 2025 result reading swarm / multi-agent systems (the
  mesh's own domain) through **machine, assemblage, rhizome, and FLOW** — <https://jcode.itu.edu.tr>.
- The **platform-striation** reading in current smooth/striated scholarship: computational/platform
  systems operate by **striating previously-smooth intensive spaces** into fixed comparable metrics (the
  canonical example: a social network turning smooth "friendship" into "200 friends vs 100 friends" —
  quantify-to-commodify). Survey/entry point: Landezine, "Smooth/Striated Space" (2024),
  <https://landezine.com/topics/concepts-theories/smooth-striated-space/>; and the ATP-14 primary
  (Somers-Hall, "The Smooth and the Striated", 2020 companion; Protevi's ATP-14 notes).
- Deleuze & Guattari, *A Thousand Plateaus*, plateau 14 (1980/1987) — the primary.

## The gap in the mesh, measured against the tool itself — `scripts/mesh-light`

`mesh-light` reads a **smooth** lux continuum (the tmd2755 sensor, 0–65535 lux) and **striates** it into
5 fixed metric bands — DARK / DIM / MODERATE / LIT / BRIGHT at 2 / 30 / 150 / 600 lux. The band token is
globally comparable but **effaces the intensive position within the band**: a MODERATE at **33 lux**
(about to fall to DIM) renders byte-identical to a MODERATE at **148 lux** (about to rise to LIT). Worse,
the sense's **hysteresis** dead-band can hold the striated label **frozen while the smooth lux has already
slid past the nominal boundary** — `level=MODERATE` while `lux=160` is LIT-range — so the grid rigidly
conceals a transition already under way in smooth space.

This is **distinct from the `velocity` axis mesh-light already has** (BRIGHTENING/DARKENING, the *temporal*
derivative). Because the bands are **non-uniform width**, velocity cannot tell you **proximity to the
striation edge**: a fast-rising mid-band lux is not near a crossing; a slow-rising lux at 148 is one step
from LIT. The intensive residual is exactly what velocity lacks — and the two **compose** (rate + distance
→ time-to-cross).

## The fix — one file: `scripts/mesh-light` (in tree, uncommitted)

`classify_smooth <lux> <level>` restores the intensive residual beneath the striation:
`pos_pct | near | margin_lux | held` — fractional position within the canonical band, lux-margin to the
nearest boundary, the adjacent band toward it when within `MESH_LIGHT_EDGE_PCT` (default 15 %), and a
**HELD flag** (`below`/`above`) when hysteresis is masking a boundary the smooth value has already crossed.
Surfaced **additively**: a `smooth=[…]` field on the rendered line and a `smooth{}` object in `--json`
(`pos_pct, near, margin_lux, held`). The `level` vocab token is **untouched** — the consumer contract is
preserved; this rides alongside like `dwell=`/`velocity=` did. Computed inside `emit_light_json` from
`level+lux`, so **every source with a numeric lux (phone, beacon) gets it for free**; the coarse webcam
fallback (no numeric lux) honestly omits it rather than faking a residual.

Report-only: it changes no verdict and no band boundary. (Re-calibrating the bands against the live corpus
would be the *self-calibration* lane the mesh already embodies elsewhere — deliberately not touched here.)

## Gate (RED-first verified)

`mesh-light --test` gains pure, offline `classify_smooth` assertions: 148/MODERATE → `pos≥85, near=LIT`;
90/MODERATE → `mid`; 33/MODERATE → `near=DIM`; **160/MODERATE held → `held=above, near=LIT, margin=10`**
(the hysteresis-masking case, the whole point). Plus the residual reaching the **rendered line** and the
**`--json`**. Falsified via the knob: `MESH_LIGHT_EDGE_PCT=0` collapses the near-edge axis → 148/MODERATE
reads `mid` (not `→LIT`) and the JSON `smooth.near` flips to `mid` → the assertions go **red** (seen live);
default (15) goes green. Verified green→red→green with `bash ./scripts/mesh-light --test`.

## Why not discarded

Discardable only if the mesh already reported the intensive position within a striated sensory band — it
did not: `mesh-light` emitted a hard 5-level label + a temporal velocity, never the band-relative residual,
so a MODERATE about to flip read identically to a stable one, and hysteresis could freeze the label over an
already-crossed boundary invisibly. Smooth-vs-striated is a first-class D&G concept with a live 2023-2026
reading (Baron 2025; platform-striation scholarship), the lux sensor is a textbook smooth continuum
striated into a metric grid, and the fix is cheap, additive, report-only, and offline-gated.

## Sources

- Deleuze & Guattari, *A Thousand Plateaus*, plateau 14 "1440: The Smooth and the Striated" (1980/1987)
- Baron — "Representation and Interpretation of Multi-Agent Systems through Deleuzian Thought", JCoDe 6(1),
  2025 — <https://jcode.itu.edu.tr>
- "Smooth/Striated Space" — Landezine 2024 — <https://landezine.com/topics/concepts-theories/smooth-striated-space/>
