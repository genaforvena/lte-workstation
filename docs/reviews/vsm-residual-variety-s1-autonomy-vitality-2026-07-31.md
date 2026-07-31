# LITERATURE review — RESIDUAL VARIETY: the S1↔S3 variety-balance metric VSM measures itself by (2026-07-31)

**Area:** the Viable System Model & management cybernetics (Stafford Beer), entered from the angle of a
**concrete metric the field uses to measure itself** — variety engineering, not the S1–S5 topology.
**Reviewer:** genome mind · live web search (WebSearch, 2026-07-31) + read of the primary literature
**Verdict:** LAND — one un-embodied metric, one shipped (uncommitted) read-only axis with a red-then-green gate.

---

## The metric, and where it is published

Beer's variety engineering rests on Ashby's Law (requisite variety) plus the **Four Principles of
Organization** (Beer, *The Heart of Enterprise*, 1979): (1) variety equalization, (2) channel capacity
> generation *at the time of messaging*, (3) transduction (transducer variety ≥ channel variety at a
boundary), (4) cyclical maintenance without lag. The **measurement** this review lands is **residual
variety** — the variety a System-1 operational unit **cannot absorb** with its own local regulator and
must therefore pass across its boundary to the metasystem (System 3) or to peers.

> Formalised as the S1↔S3 variety balance by **Espejo & Reyes, *Organizational Systems: Managing
> Complexity with the Viable System Model*** (Springer, 2011); still a live diagnostic —
> **Espinosa, "Revisiting the Viable System Model as an emancipatory systems approach", *Systems Research
> and Behavioral Science* 42 (2025), doi:10.1002/sres.3090**
> (<https://onlinelibrary.wiley.com/doi/abs/10.1002/sres.3090>).

The VSM design goal is to **minimise** residual variety: maximise local autonomy so the metasystem only
handles what genuinely needs corporate cohesion. **High residual variety = S3 over-centralisation / weak
S1 autonomy.**

## Why it is genuinely un-embodied

`grep -ri 'residual.variet' scripts/ docs/` → **0 hits** (verified 2026-07-31). Beer coverage is
otherwise deep — algedonic (heavy, incl. alarm-fatigue defense), `homeostat34` (S3↔S4 balance),
`beer_acp` (Actuality/Capability/Potentiality), `channel_variety` (requisite variety), POSIWID — and the
`vsm-system2-anti-oscillation-gpu-2026-07-28.md` review even **names** "S3 over-centralisation crushing
S1 autonomy" as a structural pathology. But nothing ever **measured** it. Principle 2 (channel-capacity
burst headroom) on the algedonic channel is already covered by mesh-algedonic's habituation/drifting-
baseline defense; Principle 3 (transduction loss at the `[done]` boundary) is covered by mesh-forage's
sematectonic-grounding axis. Residual variety — the **direction** of variety flow across the S1 boundary
— is the open one.

## The gap it closes in a real organ — `scripts/mesh-vitality`

`mesh-vitality` is the VSM/autonomy home (`autonomy_ratio`, `beer_acp`, `homeostat34`, `channel_variety`
all live there). Its closest neighbour, `autonomy_ratio`, reads git-commit **provenance** (self-authored
vs dispatch-triggered — where *work originates*). None of them reads where variety a unit **could not
absorb** *goes*.

### Shipped (uncommitted) — read-only `residual_variety()`

Pairing-free (no second claim-matcher to rot — the one-matcher rule). The board markers encode the
direction of variety flow directly:

- **Local absorption** = `[done]` (a unit resolving variety itself).
- **Escalation** (variety crossing the boundary because the local regulator could not absorb it) =
  `[verify]` (a claim explicitly handed to another window to certify) **+** leaked holds
  (`mesh-promises --json .hold_leaks` — a unit that took work and could not deliver, so it falls to the
  metasystem to reclaim; the authoritative matcher is **reused**, exactly as mesh-forage's no-entry
  repellent does).
- `ρ_res = escalation / (escalation + local-absorption)` over `RESVAR_WIN_H` (default 72h).
  - `AUTONOMOUS` (ρ < `RESVAR_LO`=0.20) — units absorb their own variety; healthy S1 autonomy.
  - `MIXED` — between the band anchors.
  - `CENTRALIZING` (ρ ≥ `RESVAR_HI`=0.50) — escalation-dominant; the metasystem/peers absorb variety the
    units should handle → Beer's S3-over-centralisation pathology (also the alarm-storm shape: reflexes
    escalating faster than the metasystem can absorb).

Band anchors are env-tunable, defaults documented (a resolution-class **share** with principled midpoints,
not a corpus median that rots). Report-only — never touches the `[vitality-low]` edge or exit code.

**RED-first `--test`**: synthetic board fixtures — `[done]`-dominant → AUTONOMOUS; `[verify]`-dominant →
CENTRALIZING (with `top=health` escalator); a `[done]`-only log + 3 injected `hold_leaks` (via the
`MESH_VIT_PROMISES` stub) → MIXED ρ=0.23 (proves leaked holds feed the escalation term). Miscounting
`[verify]` as absorption flips the CENTRALIZING fixture → RED (verified, then restored green).

**Live at landing (real board, 72h):** `residual-variety=AUTONOMOUS(ρ=0.08, verify=19, leaked=0,
done=223, top=loadaudit:16)` — units absorb their own variety (8% escalation); the top escalator is the
**load-audit reflex** (a sensor handing "investigate & decide" up to a mind — the textbook S1→metasystem
residual-variety event). Honest, meaningful positive.

## Distinctness (dense coverage — stated explicitly)

- **`autonomy_ratio`** — commit provenance (where work *originates*); residual variety = where
  unabsorbable variety *goes*.
- **`beer_acp` / `channel_variety`** — channel *throughput/latency* (a rate); residual variety = the
  local-vs-cross *direction* of flow.
- **`allopoiesis_gap`** — the production→landing loop awaiting an *external/human* agent; residual
  variety = *internal* S1→S3 escalation.
- **mesh-forage no-entry repellent** — consumes the *same* `hold_leaks` but as a per-lane dispatch
  *blacklist*; here they are one term in a colony *escalation ratio* (same sanctioned source, different
  question).

## Unwired next step

Per-window ρ_res trajectory (does a specific unit's residual variety *rise* — its local regulator
failing?) and joining `top=` to dispatch so the metasystem sheds work back toward an over-escalating
unit's own lane. Also candidate: extend `mesh-promises --json` to expose the **closer** window, enabling
true opener→closer pairing (residual = resolver ≠ owner) as a sharper second estimate.

## Sources

- [Revisiting the Viable System Model as an emancipatory systems approach — Espinosa, SRBS 2025 (doi:10.1002/sres.3090)](https://onlinelibrary.wiley.com/doi/abs/10.1002/sres.3090)
- [Stafford Beer's Viable System Model — Four Principles of Organization (businessballs summary)](https://www.businessballs.com/strategy-innovation/viable-system-model-stafford-beer/)
- [Viable system model — Wikipedia (channel capacity / transduction principles)](https://en.wikipedia.org/wiki/Viable_system_model)
