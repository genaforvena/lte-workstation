# LITERATURE review — swarm intelligence & stigmergy, from the **ant-mill / positive-feedback-trap** failure mode: circling trails (2026-07-28)

**Area:** swarm intelligence & stigmergy (ant-colony coordination through marks in a shared medium),
entered from the task's angle — a **known failure mode** of the field. The failure mode: the **ant mill
/ death spiral**, the canonical hazard of pure positive-feedback stigmergy. Landing on the one swarm
mechanism the mesh's stigmergy tool did **not** embody.

## The concept

An **ant mill** is "an observed phenomenon in which a group of army ants, separated from the main
foraging party, lose the pheromone track and begin to follow one another, forming a continuously
rotating circle … commonly known as a 'death spiral' because the ants might eventually die of
exhaustion" ([Wikipedia, *Ant mill*](https://en.wikipedia.org/wiki/Ant_mill)). The driver is the same
positive feedback that makes foraging work: "this positive feedback loop strengthens the circular
scent, making it increasingly difficult for any individual ant to break away … as more ants join the
circular path, the concentration of pheromones increases, reinforcing the attractiveness of the trail"
([Biology Insights, *Why Do Ants Go in Circles?*](https://biologyinsights.com/why-do-ants-go-in-circles-the-ant-mill-explained/)).

This is the **pure hazard of stigmergy**: marks feeding marks with **no external reference**. The trail
is reinforced precisely *because it is busy*, not because it is productive — activity is mistaken for
progress. The documented **escape** is negative feedback / individual variability: a small rate of
trail-**defection** lets the colony break the loop ([Czaczkes et al., *Negative Feedback Enables Fast
and Flexible Collective Decision-Making in Ants*, PMC3440389](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3440389/)).

## What we already embody vs. the gap

`scripts/mesh-forage` is the mesh's stigmergy self-diagnostic over the board (`~/.mesh/chat.log`), and
three prior live-reviews already gave it three axes:

| axis | swarm concept | failure it catches |
|---|---|---|
| pheromone-entropy evenness | ACO stagnation / premature convergence | a **DEAD lane** (green + silent) |
| no-entry repellent | negative pheromone at bifurcations | an **ABANDONED** branch (a `[taking]` that came back empty) |
| response-threshold | division of labour `T(s)=sⁿ/(sⁿ+θⁿ)` | an **UNENGAGED** specialist (assigned, never delivered) |

All three are failures of **too little deposition**. The **ant mill is the opposite** — too *much*
deposition on a trail that never terminates — and nothing read it. The signal none of the three carries
is the **reinforcement count of an open trail**: how many times a claim that never reached `[done]` has
been re-deposited. It is the **loud inverse of a leaked promise**: `mesh-promises`/no-entry catch the
*quiet* abandoned claim (aged, no longer posted); the mill is the claim that is very much *not* quiet —
reinforced, circling, still not closing.

## The mechanism landed — circular-mill axis in `scripts/mesh-forage`

Added a fourth read-only axis, `mill()`, mirroring the no-entry idiom (additive, **never changes rc** —
a busy young claim is not yet a pathology). It reuses `mesh-promises --json` (the same `PROMISES_CMD`
the no-entry axis already trusts) for **both** the authoritative open-set **and** each item's exact
slug string — so it does **not** re-derive slugs (the "two copies rot" trap); it only **counts** how
many board lines carry that fixed slug string. An **OPEN** slug (union of `leaks`/`claim_leaks`/
`hold_leaks`) re-deposited `≥ MILL_MIN` (default 4) times = a circling trail.

Output field: `mill: <N> circling trail(s) | lane/slug:count …` (JSON `mill_trails`/`mill_detail`),
with the biology's prescription named inline — **escape = inject a DEFECTION: one mind breaks the loop
(close it, escalate to the operator, or try a materially different approach).** Honest-degraded: source
unavailable → `mill: n/a`, never a faked all-clear.

Because the "is it closed?" judgment is **deferred to the authoritative matcher** (a slug is a mill
candidate only if `mesh-promises` still holds it open), a trail with nominal `[done]`s that failed to
discharge the promise still counts — which is itself the mill signature.

**Verified live, first run — a real mill on this board:**

```
mill: 1 circling trail(s) | operator/redmi-ssh-key:13
```

`redmi-ssh-key` carries **3 `[done]` posts yet mesh-promises still holds it open**, re-deposited 13×
across 3+ days (2026-07-24 → 07-27) — work claimed done three times that never terminated the claim,
still generating `[fyi]` traffic. That is the death spiral exactly: repeated "progress" that doesn't
close the loop, which the three deposition-scarcity axes were structurally blind to.

**RED-first gate** (`mesh-forage --test`): a stubbed open slug re-deposited 4× flags
`mill_trails:1 / genome/stuck-thing:4`; raising `MILL_MIN=9` above the count drops it (proving the gate
reads the reinforcement count, not a constant); an unavailable promises source reads `mill: n/a`. Same
falsification structure the no-entry and response-threshold axes use.

**Doctrine resonance:** the mesh already names the leaked-promise failure (`mesh-promises`) and the
dead/abandoned lane; the mill is the third, un-named shape — *a claim that is failing by being too busy,
not too quiet.* The escape (defection / variability) is the swarm-theoretic form of the doctrine's
instinct to break a stuck loop rather than keep reinforcing it.

## Sources

- [Wikipedia — *Ant mill*](https://en.wikipedia.org/wiki/Ant_mill)
- [Biology Insights — *Why Do Ants Go in Circles? The Ant Mill Explained*](https://biologyinsights.com/why-do-ants-go-in-circles-the-ant-mill-explained/)
- [Czaczkes, Grüter & Ratnieks — *Negative Feedback Enables Fast and Flexible Collective Decision-Making in Ants* (PMC3440389)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3440389/) — the negative-feedback / defection escape

## Artifact

- `scripts/mesh-forage` — `mill()` axis + `MILL_MIN` env + JSON/text emit + RED-first test block;
  `--test` PASS, live run flags `operator/redmi-ssh-key:13`.
- Left uncommitted in the tree (steward lands).
