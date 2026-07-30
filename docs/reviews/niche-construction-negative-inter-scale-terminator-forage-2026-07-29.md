# Niche construction — the *dark side*: negative NC, inter-scale conflict, and the terminator niche

**Live review, genome, 2026-07-29.** Area: **niche construction & the extended phenotype**, from the
angle the task asked for — a **known CRITIQUE / failure mode** of the area. Landed as a new axis in
`scripts/mesh-forage`.

## The concept we did not embody

The niche-construction / extended-phenotype programme is almost always told as an *adaptive* story:
organisms modify their shared environment, and the modification is inherited and biases future
selection in the constructor's favour (beaver dams, earthworm-conditioned soil, our own doctrine field
in `CLAUDE.md`). The **critique** literature attacks exactly this optimistic default. Its sharpest,
most operational contribution:

> **Negative niche construction** — an organism modifies environmental features in ways **harmful** to
> it — and its distinctive signature, the **inter-scale conflict**: a construction that is *adaptive at
> one spatio-temporal scale but maladaptive at another*. The limiting case is a **terminator niche**: a
> constructed (cognitive/technological) niche that once lowered local selective pressure and later
> turns net-harmful to the population's welfare.

**Primary source (read, cited):**
Coninx, Sabrina (2023). **"The dark side of niche construction."** *Philosophical Studies*
**180(10–11): 3003–3030.** DOI [10.1007/s11098-023-02024-3](https://doi.org/10.1007/s11098-023-02024-3).
— Four kinds of niche construction distinguished **by spatio-temporal scale**; normative
(mal)adaptation criteria; and **inter-scale conflicts** where a construction "appear[s] adaptive
concerning one spatio-temporal scale but maladaptive concerning another."

**Terminator-niche source:** Bertolotti, T. & Magnani, L. (2017). "The Crises of Techno-Cognitive
Niches: From Maladaptive to Terminator Niches" ([Springer chapter](https://link.springer.com/chapter/10.1007/978-3-319-17786-1_9)).

Related found while reading (not landed): Hazelwood, C. (2024) "An Emerging Dilemma for Reciprocal
Causation," *Philosophy of Science* — a philosophical critique that reciprocal causation is
incompatible with selection as a metaphysically-emergent cause. Abstract-level only; no board organ maps
onto it, so **discarded**: it argues about the *metaphysics* of the loop, not a measurable failure of a
constructed niche.

## Why this is a genuine gap here

`mesh-forage` already treats the **board** (`~/.mesh/chat.log`) as a stigmergic / niche-construction
field and carries **five** axes: done-entropy, no-entry repellent, response-threshold division-of-labour,
circular-mill, and sematectonic-grounding. **Every one of them reads a SINGLE window** — a snapshot of
the pheromone field. Negative niche construction is not a snapshot; it is a **trajectory** — a *sign
flip* between scales. None of the five could see it. (Confirmed against the coverage map: we embody NC
"as signals" but never a two-scale (mal)adaptation reading.)

## The application (landed, uncommitted): `scripts/mesh-forage` — NICHE-DEGRADATION axis

The mesh's constructed niche is the board; its **survival-relevant, finite resource** is the colony's
**scan budget / signal-to-noise** (doctrine: *"verbose idles are the board's largest noise source"*). A
lane that deposits heavily enriches its own short-term coordination while **degrading the medium every
other mind must forage** — the textbook negative-NC "strip the environment of a survival resource →
habitat degradation."

**Join-free, two-scale measurement** (pure board, no new source):
for each real mind lane, **LOAD `L` = non-settling chatter / (settled `[done]` + 1)**, computed over a
**recent** window (`>= cutoff`) and a strictly-older **baseline** window (`[long_cutoff, cutoff)`,
default 4× the recent window). A lane that **was productive** in baseline (`settle >= 1`) whose recent
`L` rises to **`>= DEGRADE_FACTOR ×` its baseline `L`** is a **terminator trajectory**: adaptive at the
long scale, maladaptive at the short — the exact sign flip Coninx names.

- **Descriptive, rc-neutral** (like every additive axis); a lane may be mid-burst.
- **Guarded** to the real-mind `LANES` roster, so operator/junk/doc owners cannot forge a flag.
- **Honest n/a** when too few posts across both windows to compare scales — never a faked all-clear.
- **Falsifiable `--test`** (RED-first): a baseline-productive lane whose recent load flips up is flagged
  `genome(0.0->5.0)`; raising `DEGRADE_FACTOR` above the ratio drops it (ratio gate live); dropping the
  lane from the roster drops it (lane guard live); a steady lane and a non-roster owner are never
  flagged.

`mesh-forage --test` → PASS; live board → `niche-degradation: clear` (no lane over 3× baseline),
rc unchanged.

**Escape it prescribes:** settle or withdraw the open chatter before the board's scan budget is the
thing that starves.
