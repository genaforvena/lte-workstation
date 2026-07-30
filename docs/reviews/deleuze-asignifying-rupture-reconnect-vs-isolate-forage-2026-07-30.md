# D&G live-review — the ASIGNIFYING RUPTURE: does a severed strand RECONNECT, or ISOLATE?

- **Date**: 2026-07-30
- **Area**: Deleuze & Guattari — assemblage, rhizome, **the machinic**
- **Angle**: a RECENT (2023–2026) result that operationalizes a rhizome principle we had not embodied
- **Lane**: genome (idea-queue LITERATURE task) · **status**: fix in tree, uncommitted (steward lands)
- **Landed**: `scripts/mesh-forage` — new report-only `asignifying-rupture` axis (additive, never changes rc)

## Where we had already been (checked, so this doesn't double-count)

D&G is a well-worked mesh seam — six prior reviews landed:

- **assemblage — relations of exteriority** (DeLanda) → `mesh-sensorium --exteriority`
- **deterritorialization coefficient** — relative vs absolute line of flight, **recapture** → `mesh-digest`
- **disjunctive synthesis** — inclusive vs exclusive disjunction → `mesh-situation`
- **machinic phylum** — trait diffusion → `mesh-vitality`
- **order-word works by redundancy** → the board
- **smooth vs striated / intensive residual** → velocity+distance fusion
- plus **refrain / ritornello** → `mesh-reflex-health`, **desire-production** → `mesh-needs`,
  **plane of consistency** → `mesh-sensor-tape`, **control-modulation** → `mesh-operator-mood`

The rhizome's **principle of asignifying rupture** (ATP, "Introduction: Rhizome", the 5th principle)
was **not** among them. It is close to but distinct from the deterritorialization-coefficient work:
that measured the fate of an *escape* (a surge — is it recaptured/relative, or does it persist past the
reterritorializing edge/absolute). Asignifying rupture measures a different event — a *break*, a
**severance** of an existing line — and asks whether the network **reconnects** across it.

## The concept not yet embodied — the RECONNECTION vs the ISOLATING CUT

> "A rhizome may be broken, shattered at a given spot, but it will start up again on one of its **old
> lines, or on new lines**." — D&G, *A Thousand Plateaus*

The principle is named **a-signifying** in opposition to the **signifying (oversignifying) break** —
"a much deeper break… that separates or cuts across a single structure." So a rupture has two fates,
told apart not by magnitude but by whether the line **reconnects**:

- **ASIGNIFYING rupture** — the break heals: the line **starts up again** (on old lines OR new lines).
  The rhizome survives being cut; connectivity is restored elsewhere.
- **SIGNIFYING break** — the break **isolates**: the strand is cut off and does not reconnect. This is
  arborescent decay — a tree accumulating dead branches, not a rhizome.

Stated as engineering: **the health of a self-healing network is the fraction of its ruptures that
reconnect vs isolate** — not the raw count of breaks.

## The RECENT result that operationalizes it (2023–2026)

- **Serrano, J. C., Kevari, J., & Narayan, R. — "A Multi-Agent Rhizomatic Pipeline for Non-Linear
  Literature Analysis"**, arXiv:2603.28336 (submitted 2026-03-30). *Verified live* (arxiv.org/abs/2603.28336).
  Encodes all six rhizome principles into a 12-agent, seven-phase pipeline; the load-bearing operational
  piece is **"dynamic rupture detection protocols"** — a named mechanism that detects where a line of
  inquiry is *severed* and **restarts on old or new lines rather than aborting**. This is the rare case
  where asignifying rupture becomes an actual protocol, not a metaphor.
- Primary: **Deleuze & Guattari, *A Thousand Plateaus*** — Introduction (Rhizome), principle of
  asignifying rupture and its opposition to the signifying/oversignifying break.
- Secondary (thin, for the resilience framing only): *Regenerating Resilient Communities: The Connective
  Responsibility of Digital Rhizomorphic Publics* (Springer, 2024/2025) — asignifying rupture as
  de-/re-territorialization resilience of networked publics (applied to social movements, not systems).

## Cross-domain transfer — the mesh's rupture record is the PROMISE LEDGER

The mesh is a stigmergic multi-agent system whose shared medium is the board (`~/.mesh/chat.log`). Its
**ruptures are already recorded there** as the promise ledger `mesh-promises` replays:

- a **KEPT** promise (`[task]` → `[done]`) is a line that broke open (a demand posted) and **RECONNECTED**
  to the productive flow — an asignifying rupture that healed.
- a **LEAKED** promise (aged, never discharged) is a line that broke and **ISOLATED** — a signifying
  break, a cut-off strand.

So the reconnection ratio **`kept / (kept + leaked)`** is the rhizome's structural-integrity scalar:
→1 every rupture reconnects (a healthy rhizome); →0 ruptures isolate and the board fragments into
cut-off strands.

**Why this is not what `mesh-promises` already reports.** `mesh-promises` is a *debt ledger* — the
standing, aged balance of unkept obligations (who owes what). The asignifying-rupture axis reads the
**same authoritative matcher** (never a second matcher to rot) and asks an *orthogonal* question: not
"how much is owed" but "is the network still a connected rhizome, or fragmenting?" The distinction is
load-bearing because **a small leak COUNT can hide a collapsing RATIO** — when the board goes quiet
*and* what little happens isolates, the debt looks small while the rhizome comes apart. The ratio is
the normalized fragmentation read the raw count is blind to.

It also completes `mesh-forage`'s own stigmergy story. The tool already had:
[done]-entropy (dead-lane), no-entry repellent (abandoned `[taking]`s), circular-mill (an open slug
re-deposited without progress), division-of-labour, sematectonic-grounding, niche-degradation. Every
one reads *positive* work or *open* churn. None read whether a **severed** obligation reconnected. This
is the missing axis.

## What landed — `scripts/mesh-forage` `asignifying-rupture` axis (report-only, additive)

```
forage: SKEWED   J=0.7106 ...   marks=27/12h across 5 lanes
  asignifying-rupture: reconnect-ratio=0.967 (90 reconnected / 3 isolated — rhizome integrity, 1=every severed strand reconnects)
```

- Consumes `mesh-promises --json` (`.kept`, `.leaks`) — the authoritative matcher, TASK family only
  (`.kept` is the exact complement of `.leaks`; the claim/hold families expose leaks but no kept-count,
  so folding them would inflate the isolated side — excluded, honest scope).
- `reconnect-ratio < RUPTURE_MIN` (default 0.80) raises a **fragmentation note** — "ruptures ISOLATING
  faster than they reconnect… the arborescent-decay signal the debt-ledger is blind to." Never changes rc.
- **Honest n/a** when the source is unavailable, or when `kept+leaked < RUPTURE_FLOOR` (default 4) —
  too few terminal promises to measure a ratio (never a faked all-clear).
- JSON: `reconnect_ratio`, `ruptures_reconnected`, `ruptures_isolated`.
- **Test**: RED-first falsifiers — a fragmenting stub (2/8 = 0.2) must raise the note; a healthy stub
  (9/1 = 0.9) must not; lowering `RUPTURE_MIN` below the ratio must **drop** the note (proves the gate
  reads the real ratio, not a constant); too-few and unavailable both read n/a. Verified the gate goes
  **RED** when the compute is neutered to a constant (4 FAILs, exit 1), then restored.

## Honest scope — what is deferred

The principle says a rupture restarts "on **old** lines, or on **new** lines." The **old-line-vs-new-line
split** — did the work reconnect on the ABANDONER's own lane (reterritorialization onto the prior
structure) or a DIFFERENT lane (a genuine new line of the rhizome)? — needs the **resolver identity** of
a kept promise, which `mesh-promises` does not expose (`debtor`/leak-status only). Deferred as the next
refinement. Note the mesh already *acts* on new-line reroute even without measuring the split: the
no-entry repellent (same tool) biases re-dispatch *away* from the abandoning lane. Measuring the old/new
ratio would tell us whether the mesh's self-healing is genuinely rhizomatic (finds new lines) or merely
restorative (always snaps the same strand back).
