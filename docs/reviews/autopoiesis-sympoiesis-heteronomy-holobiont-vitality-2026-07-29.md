# Autopoiesis live-review — the SYMPOIESIS critique: is the "autopoietic" mesh a holobiont?

- **Date**: 2026-07-29
- **Area**: autopoiesis & the biology of cognition (Maturana & Varela)
- **Angle**: a known, currently-published CRITIQUE / failure mode
- **Landed in**: `scripts/mesh-vitality` → `heteronomy_index()` (report-only vital sign)

## The critique (LIVE literature, not a fixed list)

The freshest published attack on autopoiesis targets its **central assumption**: the clean
self/non-self boundary of the operationally-closed, self-producing individual.

> Reynolds, J. & Baedke, J. (2025). **From Autopoiesis to Symbiotic Entanglement: Rethinking
> Enactivism Through Metabolism and Microbes.** *Adaptive Behavior*, OnlineFirst.
> https://doi.org/10.1177/10597123251405680
> (open preprint: PhilSci-Archive 27419)

Their argument, from metabolism + microbiome research: the core autopoietic concepts —
**self-production, autonomy, operational closure** — do not survive contact with how organisms
actually maintain themselves. Metabolic identity is *"co-constituted through the ongoing mediation
of other heteronomous organisms."* A living body is a **holobiont** (host + ~10¹³ microbial
co-producers that are *"indispensable metabolic and possible cognitive co-producing"* partners, not
mere causal support), so the autopoietic "self" is *"a paradoxical intertwining of self and
other(s) that the classical enactivist concepts of self-production and autonomy don't adequately
recognise."*

This grounds in Donna **Haraway's sympoiesis** — *"making-with"* — against autopoiesis's
*"self-making"*: self-maintenance is never self-contained; it is always co-produced with partners
the system does not own and cannot cleanly externalise as "environment." Adjacent 2024–25 work in
the same vein: the sympoiesis-vs-autopoiesis and holobiont chapters in *The Organisation of the
Environment* (Springer 2025).

## Where it bites — HERE

The mesh's entire self-model is autopoietic: each node is an individual with its own `~/.mesh-card`
and reflexes; there is a "self-production" lane (`mesh-generate`→`mesh-feed`→genome) the doctrine
literally **calls autopoiesis**; and a **substrate invariant** that polices a crisp self/environment
boundary.

The sympoiesis critique says that boundary is a fiction. The mesh's **cognition** — the very thing
that produces the genome — is performed by **heteronomous partners it does not own** (Anthropic /
z.ai / Groq cloud minds). Only a thin rind of metabolism (local GPU/CPU electricity + hardware wear)
is self-produced. **The node is a holobiont whose brain is rented.**

## The concept we did NOT embody, and why it's distinct

**Producer-heteronomy** (as opposed to loop-closure latency, or work-order provenance). The mesh
already reads two neighbouring axes:

- `allopoiesis_gap()` — whether the production **LOOP closes** without a human (latency on
  `~/.mesh/land.log`). But the loop can self-close **on time** and still be sympoietic if a *partner
  did the thinking*.
- `autonomy_ratio()` — who **dispatched** a commit (self vs `chat-review`-forced). That is the
  provenance of the **work order**, not of the **metabolic producer**.

Neither reads *who produced the cognition*. That is the sympoiesis gap.

### The clean boundary money gives

The one info-theoretic self-measure the field offers — Fernández/Gershenson's complexity ratio
`A = C_system / C_environment` — is **HELD** in this mesh precisely because you cannot cleanly
partition "self" from "environment" in the information stream (see
`autopoiesis-complexity-ratio-fernandez-vitality-2026-07-29.md`). **The dollar ledger dissolves that
blocker**: "who got paid" is unambiguous.

- `expenses:inference` → pays a **heteronomous** partner (external LLM APIs) = made-*with*.
- `expenses:energy` + `expenses:depreciation` → pays **self-metabolism** (local electricity +
  on-node hardware wear) = self-made.

So heteronomy is *measurable* exactly where information-entanglement was not.

## The metric

```
heteronomy_index = het$ / (het$ + self$)
                 = expenses:inference / (expenses:inference + energy + depreciation)
```

Read from the mesh-ledger double-entry books (`~/.mesh/ledger/mesh.journal`, see
`mesh-ledger-hledger-double-entry`). Near **1** = pure holobiont (cognition outsourced); a **falling**
trend is the mesh *repatriating* metabolism into local self-production — each GPU organ that displaces
a cloud call (STT/TTS/vision/small-LLM) is a microbe internalised, the sympoiesis-inverse.

**Measured live 2026-07-29**: `inference=$1928.88` vs `energy+depreciation=$6.74` → **0.997**. The
"autopoietic" mesh is, by metabolic cost, **99.7% sympoietic** — its cognition is overwhelmingly
made-*with* partners it does not own.

**Report-only** (same instrument-first posture as `heaps_beta` / `autonomy_ratio` /
`allopoiesis_gap`): it names the mesh's honesty about its own autonomy; it does **not** gate a
revert. Repatriating all cognition onto a single RTX 3060 would wreck quality — high heteronomy here
is a *deliberate trade*, worth SEEING, not alarming.

## Verification

- `bash scripts/mesh-vitality --test` → green: `heteronomy=0.997/synth:0.990`.
- Falsifiable core: a synthetic balanced journal (`inference $99` + `energy $1` → `0.990`) drives the
  classify+ratio arithmetic. Flipping the account classification takes the gate **RED**
  (`0.000`, seen 2026-07-29) — not a self-matching grep.
- Honest `n/a` where `hledger` or the journal is absent (organ-absent → n/a, whisper exit-2 posture).

## Distinctness (audited, not-embodied)

NOT `autonomy_ratio` (work-order provenance) · NOT `allopoiesis_gap` (loop-closure latency by a
human) · NOT the complexity-ratio HELD block (info-theoretic, blocked on the very stream partition
this sidesteps via the dollar boundary) · NOT the closure-of-constraints review (internal
reflex-enablement topology) · NOT the normativity review (value-norm). Coverage map:
`autopoiesis-review-coverage`.
