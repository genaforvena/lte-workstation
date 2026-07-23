# Study finding — SOC partial redistribution (self-organized criticality / power-law dynamics)

**Source:** auto idea-queue task — LITERATURE (live review): self-organized criticality & power-law
dynamics, from the angle of an OPERATIONAL mechanism we could implement (2026-07-23).
**Verdict:** Finding + concrete proposal for `scripts/mesh-load-gate`. NOT built (load-bearing shed
reflex; needs design review + hysteresis test).
**Date:** 2026-07-23 · owner: genome

## The concept we do NOT embody

**Tunable partial-redistribution (graded toppling) in a driven sandpile**, the operational core of
self-organized criticality. Recent, live sources:

- *Self-organized criticality and structural dynamics in evolving neuronal networks: a modified sandpile
  model*, Physica A **666** (2025) — <https://www.sciencedirect.com/science/article/abs/pii/S0378437125001876>:
  BTW threshold spiking with directed weights; avalanche sizes follow a power law (mean-field exponent 3/2).
- BTW extended to critical-infrastructure networks with a **tunable redistribution parameter controlling
  what fraction of stress propagates to neighbors** — partial redistribution at intermediate values is
  what yields SOC dynamics (2024 infrastructure SOC work, surfaced via
  <https://ideas.repec.org/a/eee/phsmap/v666y2025ics0378437125001876.html> search cluster).
- *Optimization by Self-Organized Criticality*, Sci. Reports 8 (2018) —
  <https://www.nature.com/articles/s41598-018-20275-7>: control = any action interfering with load
  ACCUMULATION reduces the probability of extreme (large-avalanche) events.

**Operational mechanism:** instead of a single global hard threshold that fires all-or-nothing, each node
topples a *fraction* of its accumulated stress to neighbors when it exceeds a local threshold. Partial,
staggered redistribution keeps the system SUBcritical — many small avalanches (power-law tail) instead of
one large synchronized one.

## Why it isn't already embodied here (checked, not assumed)

`mesh-load-gate` is a **binary global threshold**: when `load1 > threshold` (default 11), a heavy reflex's
tick SKIPs entirely; below it, it runs (`scripts/mesh-load-gate`, "SHED gate … proceed only when the box
has headroom"). 17 heavy reflexes share this gate. The failure SOC predicts is real for us: the reflexes
shed *together* the moment load crosses 11, and *resume together* the moment it drops — a synchronized
shed→recover avalanche (thundering herd), and if the resumed reflexes re-spike load past 11 you get
oscillation. We embody the driven side (load accumulates) and a global dissipation rule; we do NOT embody
graded partial redistribution or subcritical tuning.

## Concrete proposal — `scripts/mesh-load-gate`

Replace the binary shed with graded, hysteretic redistribution (still fail-open: a bad load read PROCEEDS,
unchanged):

- **Fraction, not all-or-nothing:** shed a fraction of the heavy-reflex set proportional to overload
  `(load1 − threshold)`, sorted heaviest-first (deterministic by reflex weight/name), so mild overload
  defers only the heaviest one or two, not all 17.
- **Hysteresis band:** shed above `threshold`, resume only below `threshold − H` (e.g. H=2). Breaks the
  shed-at-11 / resume-at-11 oscillation — the exact "interfering with load accumulation" that SOC says
  suppresses large avalanches.
- **Optional avalanche log:** record shed-set size per tick to `~/.mesh/load-avalanches.log`; a heavy tail
  toward "all 17 at once" is the health signal that we are running critical, not subcritical.

## Disposition

Filed as a proposal, not landed. `mesh-load-gate` is prepended to 17 live cron lines; changing its
proceed/skip semantics needs a design review and a test that asserts the hysteresis (a load that crosses
threshold then dips 1 below must NOT immediately un-shed). Cited, operational (not philosophy), and a
mechanism we do not currently have.
