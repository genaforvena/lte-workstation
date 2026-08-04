# Deleuze & Guattari live review — the assemblage we misread: purpose-oriented *agencement*, and the reflex whose responding changes nothing

**Date:** 2026-08-04 · **Mind:** genome@mesh-home · **Organ touched:** `scripts/mesh-reflex-health` (`--discharge`)
**Angle requested:** a foundational idea we may have MISread or applied too loosely.

---

## 1. The misread, named

Every assemblage axis in this genome is **DeLanda's** reading of *agencement*:

| axis | organ |
|---|---|
| relations of exteriority | `mesh-sensorium --exteriority` |
| degree of territorialization · capacity-to-affect | `mesh-digest` |
| machinic phylum (trait diffusion) | `mesh-vitality` |
| rhizome vs arborescent call-graph | `mesh-vitality` `rhizome_index` |
| deterritorialization coefficient | `mesh-digest` |
| double articulation (content/expression) | `mesh-sensorium --articulation` |

Six axes, one lineage. Each measures **an arrangement of parts and their relations** — heterogeneity,
exteriority, concentration, topology. That is not a neutral choice of vocabulary; it is one side of a
live and explicitly *incompatible* split in the current literature, and the other side calls it a
misreading.

- **Ian Buchanan, *Assemblage Theory and Affect*, Bloomsbury, 19 Feb 2026, ISBN 9781350268784, 168pp.**
  The live continuation of his *Assemblage Theory and Method* (Bloomsbury, 2021). Its second argument,
  verbatim from the publisher's description: affect is *"not the measure of our response to a given
  stimulus, it is rather **the capacity we have to respond** to a stimulus in the way that we do"*.
  Argument 1: *"affect is a function of desire"* — a psychical agency alongside the body without organs
  and the abstract machine. Argument 3: that capacitating power *"depends upon the combinations of
  bodies without organs and abstract machines … put together by means of the assemblages available to
  us"* — what Deleuze means by an ethics of desire.
  (Publisher record verified 2026-08-04 via Google Books' Bloomsbury listing; Bloomsbury's own page
  blocks automated fetch.)
- **Bond & Mulholland, "Tussling with seascape character assessment and assemblage theories",
  *Journal of Environmental Policy & Planning*, doi:10.1080/1523908X.2023.2251905.** Names the split
  in the open: **systems-oriented** assemblage theory (DeLanda — emergent wholes of heterogeneous
  parts) vs **purpose-oriented** (Buchanan — desire, and the problem the arrangement answers), and
  argues the two are *incompatible*, not complementary. Buchanan's standing charge is that
  "assemblage" has drifted into a vague label for complexity/heterogeneity with desire and the problem
  deleted — which is precisely the use this genome has been making of it.
- Background for why the word itself invites the drift: John Phillips, "Agencement/Assemblage",
  *Theory, Culture & Society* 23(2–3), 2006 — *agencement* names the **act** of arranging (agency,
  purpose); English "assemblage" names the **heap**. The mesh has been measuring the heap.

This is not a claim that DeLanda is wrong. It is a claim that we have six axes on one side of a
two-sided question and none on the other, and never noticed we had chosen.

## 2. The mechanism we do not embody

Under the purpose-oriented reading an assemblage is individuated by **the problem it responds to**, and
its responding counts as affect only if it **capacitates** — only if it changes what the body can
subsequently do. A response that discharges the stimulus and leaves the disposition identical is not
affect; it is a reflex arc.

Apply that to the genome's reflex-tenders:

- `mesh-reflexes` — heals cron **drops** (is it scheduled?)
- `mesh-reflex-decay` — eats **unused** reflexes (is it wanted?)
- `mesh-reflex-health` — is the reflex **alive and writing** (did it respond?)

Alive · firing · fresh. Three ways of asking *did it respond*. **Nothing in the genome asks Buchanan's
question: after all that responding, is the fault still arriving at the same rate?**

A self-heal that has relaunched a mind 177 times, or a care reflex that has logged one peer
UNREACHABLE 11,000 times, is green on every existing axis while the problem it was born to answer is
completely untouched. In purpose-oriented terms the mesh has **territorialized** the fault — made it
liveable — and every instrument it owns reports that as health.

## 3. What landed — `mesh-reflex-health --discharge`

Read-only, off the cron path, never an alarm. For each entry in `DISCHARGE_TABLE` (fields `::`-separated
because the patterns are regexes that use `|` for alternation):

1. read the reflex's **own log**; count **RUNS** (its per-run/per-decision lines — the exposure) and
   **ACTS** (the intervention/fault lines);
2. split the run **sequence** in half by index, so the two halves carry equal exposure by construction;
3. test the acts against that exposure with an **exact two-sided binomial** (H₀: constant per-run
   incidence), **Bonferroni-corrected** across the entries that were actually testable.

| verdict | meaning |
|---|---|
| **CAPACITATING** | incidence fell significantly — the responding changed the disposition |
| **ESCALATING** | incidence rose significantly — responses beget responses |
| **DISCHARGING** | flat — pure discharge; a prosthesis, the fault is territorialized, not solved |

**DISCHARGING is deliberately not a fault verdict.** Some faults are external and a permanent
prosthesis is the correct engineering answer (the 14-minute deauth; a peer that is simply switched
off). What the axis adds is that the mesh can now *see the rent it is paying*, which no other
instrument reports.

### Live reading (2026-08-04, mesh-home)

```
== discharge vs capacitation (purpose-oriented assemblage; alpha=0.0167 over 3 testable) ==
• node-care          CAPACITATING 34.0%->28.4% over 10929 runs (3409 acts, p=1.72e-07)
• egress-quality     ESCALATING   58.0%->68.7% over 6614 runs (4189 acts, p=4.43e-08)
• channel-keepalive  n/a          SILENT 100.4h (>6x median gap) — the log stopped
• guardian-peer      DISCHARGING  73.3%->74.6% over 2933 runs (2168 acts, p=0.683)
• rent: 1 of 3 testable reflexes respond forever at an unchanged rate
```

`egress-quality` ESCALATING is a real standing signal, not a fixture: `QUALITY BAD` incidence rose
from 58% to 69% across the log, consistent with this node's egress having moved to a US exit
(~325 ms). `guardian-peer` is the textbook prosthesis — a peer that has been DOWN ~74% of every run
for the whole window, tended forever, unchanged.

## 4. The two gates, and why both exist

**A "cure" and a silent failure produce the same series.** This is the axis's central hazard, so both
directions are refused by name rather than shipped as the flattering half:

- **Liveness gate** — if the last run is older than 6× the median inter-run gap (floor 1800 s), the
  verdict is `n/a`: the log stopped, and a verdict here would be about a reflex that is no longer
  running. Derived from the log itself, not from cron, so it also covers the loop-driven reflexes
  (`channel-keepalive`, `node-care`) that have no crontab line at all.
- **Zeroed-act-branch gate** — the liveness gate **cannot** catch a reflex that keeps running and
  logging while its *act branch* dies. `acts → 0` then reads as the best news the mesh could get. If
  the second half has zero acts and the first had ≥ 10, the verdict is `n/a`: *"a cure and a disarmed
  act-branch are the same series here; check the branch, not the rate."*
- Under 10 acts → `n/a` (underpowered), never "cured".

**Seen RED, not asserted** (mutants run from a scratch copy):

| mutant | result |
|---|---|
| liveness gate → `if False` | `dead` fixture reads **DISCHARGING** — a verdict about a reflex dead for a week |
| zeroed-branch gate → `if False` | `zeroed` fixture reads **CAPACITATING** — the false cure, exactly as predicted |
| CAPACITATING branch disabled | `falling` fixture reads DISCHARGING |
| MIN_ACTS gate → `if False` | `thin` fixture (2 acts) reads DISCHARGING |

Fixtures are generated at a frozen `MESH_DISCHARGE_NOW` and act on a deterministic every-*k*-th
schedule — no RNG, so there is no seed to shop
(cf. `a-stochastic-gates-threshold-is-a-statistic`).

## 5. Weakest joints (stated, not hidden)

- **The exposure is the log, so the axis inherits the log's honesty.** A reflex that logs only when it
  acts has no denominator here and is simply absent from the table — not silently assumed healthy.
- **The zeroed-act gate refuses the interesting case rather than resolving it.** Distinguishing a real
  cure from a disarmed branch needs evidence the log does not carry (did the branch's *condition* ever
  hold?). The honest answer today is `n/a` plus a pointer at the branch.
- **Half-split by index assumes stationary composition.** `node-care`'s halves contain different node
  populations; a node joining or leaving moves the rate without any reflex having done anything. The
  verdict is about incidence-per-opportunity, not about causation
  (cf. `reproduction-is-not-causation`).
- **Four table entries is coverage, not census.** The scan of `~/.mesh/*.log` found only these with
  both a countable per-run line and a countable act line; the table is meant to grow.
- **The axis is report-only** and deliberately not wired into the cron path or the edge-trigger — a
  10-minute watchdog should not be scanning 30 k log lines.

## 6. Files

- `scripts/mesh-reflex-health` — `--discharge` mode, `DISCHARGE_TABLE_DEFAULT`, `discharge_report()`,
  literature block, and 7 new `--test` assertions.
- This document.

Left uncommitted in the tree for the steward, per task.
