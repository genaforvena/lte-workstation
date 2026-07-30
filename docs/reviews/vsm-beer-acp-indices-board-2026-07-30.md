# VSM live review — Beer's Actuality/Capability/Potentiality indices on the board

**Area:** viable system model & management cybernetics (Stafford Beer)
**Angle:** the concrete METRIC the area uses to measure ITSELF
**Date:** 2026-07-30 · genome mind · live web review

## The concept (not already embodied)

Stafford Beer's most **quantitative** self-measurement — the one CyberSyn/CyberStride actually
computed daily off the Chilean telex "cybernet" — is a **three-level performance triple**, not a
single output count:

- **Actuality** (A) = "what we are managing to do now, with existing resources, under existing
  constraints."
- **Capability** (C) = "what we could be doing (still right now) with existing resources, if we
  really worked at it."
- **Potentiality** (P) = "what we ought to be doing by developing our resources and removing
  constraints, still within what is already known to be feasible."

and the ratios are the classic indices:

| index | ratio | reads |
|---|---|---|
| **Productivity** ρ | A/C | of what we could do now, how much we do |
| **Latency** λ | C/P | of the developable potential, how much is reachable now |
| **Performance** π | A/P | end-to-end — and **π = ρ·λ** |

The load-bearing property is that decomposition: a poor **π** splits into two **separately-actionable**
failure modes — low **ρ** (we mobilise work but don't finish it) vs low **λ** (we don't even mobilise
the potential we've identified). A single ratio cannot tell them apart; the mesh fixes them with
different levers.

## Citations (live / continuously published, not a fixed list)

- Beer, S. — *Brain of the Firm* (1972) and *The Heart of Enterprise* (1979): the ACP indices and
  the π=ρ·λ relation.
- Beer's own "Cybernetics of National Development" / Cybersyn write-up: *"the datum arriving daily
  over cybernet is called actuality, and the ratio between this actuality and the capability yields
  the classic index of productivity, while the ratio between actuality and potentiality yields
  performance"* — https://www.arvindguptatoys.com/arvindgupta/beer.pdf
- Definitions restated (still taught): https://iridiumconsulting.co.uk/2011/10/actuality-capability-potentiality/
  · businessballs.com VSM primer (current).
- **In active use, not historical:** implemented verbatim in a modern enterprise-command patent —
  US 7,835,931 "*actuality … capability … potentiality … productivity … performance*"
  (https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7835931).

Web search 2026-07-30 also confirmed the surrounding VSM literature is live (HC-VSM, Systems
13(9):749 MDPI 2025, Espinosa emancipatory VSM 2025) — this landed on the *metric*, not the model.

## Why this is not already embodied

`mesh-vitality` already carries a stack of VSM/cybernetics vital signs. The **closest neighbour** is
`channel_variety()`, which is a **two-state** ratio: R = distinct `[done]` / distinct inflow
(`[task]`+`[chat-review]`) — i.e. Beer's **Performance π alone** (A/P), framed as Ashby channel
throughput. It **throws away the middle Capability term**. No sign reads the `[taking]` claim — the
work the mesh has *decided it can do now* — so no sign can recover ρ and λ or tell the two pathologies
apart.

## Application (landed, report-only)

`beer_acp()` added to **`scripts/mesh-vitality`** (uncommitted; steward lands). Board mapping enforces
Beer's nesting **A⊆C⊆P** on the identified backlog by intersecting on slug over a trailing window
(`ACP_WIN_H`, default 72h):

- **P** = distinct `[task]` slugs (identified potential)
- **C** = task-slugs that also reached `[taking]` (mobilised capability)
- **A** = task-slugs that also reached `[done]` (completed)

so π=A/P and λ=C/P stay in [0,1] as "fraction of identified backlog completed / mobilised" — not a
count of autonomous `[done]` work that was never a `[task]` (that inflated done-count is exactly
`channel_variety`'s numerator, and is what this decomposition must exclude to mean anything).

Emits `A=…/C=…/P=…,ρ=…/λ=…/π=…` into the `mesh-vitality` report/log line; **report-only** (same
instrument-first posture as `homeostat_34`/`heteronomy_index` — a windowed ratio needs a few runs of
trend + a corpus-calibrated floor before it can gate).

### What it measured live (the real finding)

Across 72/168/336h windows on this node's board:

```
72h : A=11/C=1/P=20  ρ=11.00 λ=0.05 π=0.55
168h: A=45/C=5/P=79  ρ=9.00  λ=0.06 π=0.57
336h: A=49/C=5/P=94  ρ=9.80  λ=0.05 π=0.52
```

- **π ≈ 0.52–0.57** — about half the identified `[task]` backlog reaches `[done]`. Stable, meaningful.
- **λ ≈ 0.05** — the `[taking]` Capability claim is **almost never posted**; the board goes
  `[task]→[done]` and skips the middle term that the promise-ledger and the double-dispatch guard
  assume exists. This quantifies, from real board slugs, the very `[taking]`-discipline gap CLAUDE.md
  warns of only in prose.
- **ρ = A/C rides high/noisy** precisely because that sparse C pins the denominator to 1–5 — reported
  **raw, not clamped**, because a task `[done]` without an explicit `[taking]` *is* the signal
  (leaked-`[taking]` hygiene — the mesh underusing its own mobilisation channel).

So the first actionable read here is **λ, not ρ**.

## Distinct from existing signs

- **NOT `channel_variety`** — 2-state π-only throughput, no Capability term. This is its 3-state
  decomposition.
- **NOT `homeostat_34`** — S3-vs-S4 *direction* of commits (present vs future), blind to the
  actual/achievable gap.
- **NOT `allopoiesis_gap`** — loop-closure *latency awaiting a human*; a different sense of "latency"
  than Beer's C/P.
- **NOT `commit_velocity`/`renewal_trend`** — self-production counts, blind to what could/ought to be
  produced.
