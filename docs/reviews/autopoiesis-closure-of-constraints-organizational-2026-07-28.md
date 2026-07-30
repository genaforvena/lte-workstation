# Live-literature review — autopoiesis: organizational closure as a graph over our own reflexes

Date: 2026-07-28 · lane: genome (idea-queue LITERATURE task) · status: implemented + gated, uncommitted

## Area

Autopoiesis & the biology of cognition (Maturana & Varela), entered from the angle of an
**operational, computable mechanism** — not the philosophy. Searched the live literature (ALIFE
2026 tutorial track, HAL/Cambridge Core, arXiv 2024/2025), read, and landed on one mechanism the
mesh does not embody.

## The mechanism: closure of constraints (the operational form of autopoiesis)

Maturana & Varela's autopoiesis says a living system is *a network of processes that produces the
very components that produce the network* — **operational closure**. As a slogan it is philosophy;
the operational version is **closure of constraints**:

> Montévil & Mossio, *Biological organisation as closure of constraints*, J. Theor. Biol.
> 372:179-191 (2015) — https://hal.science/hal-01192916v1 · Cambridge Core reader:
> https://www.cambridge.org/core/product/66F5B26F146D1DF12CB1B3019B50734A/core-reader

Their move splits a system's causal regime in two: **processes** (the open thermodynamic flow) and
**constraints** (entities that act on processes while being *conserved* at the process's timescale).
A biological organization is then a set of constraints where each one is **maintained by other
constraints in the set** *and* **contributes to maintaining them** — a closed loop of mutual
dependence. Closure is the property that distinguishes an *organization* from a heap of independent
maintenance jobs. (Predecessor: Mossio & Moreno, *Organisational closure in biological organisms*,
2010.)

The freshest **computational** form is the process-enablement graph:

> Sousa, Hordijk et al., *Studying self-organisation across the biosphere with process-enablement
> graphs*, arXiv:2411.17012 (2024) — https://arxiv.org/pdf/2411.17012

Nodes are processes; a directed edge `A → B` means *A enables B*; a self-maintaining organization is
a subgraph **closed under enablement** (every member enabled from within the set). This is exactly a
computable object — and exactly the object the mesh has never computed over itself.

The angle is live, not a museum piece: the **ALIFE 2026** tutorial track
(https://autopoiesistutorial.netlify.app/) foregrounds structural coupling and operational closure
and ties them to Rosen's anticipation and the FEP — a current, published conversation.

## What we ALREADY embody (so this doesn't double-count)

- **Timescale separation of a constraint** — Montévil/Mossio's *other* operational criterion (a
  constraint must be conserved at the timescale of the process it governs) is partly embodied:
  memory `a-lease-must-exceed-its-producers-cadence`, and the liveness-touch convention.
- **Self-production LANES** exist and are metered for *whether they produce*: `mesh-vitality`,
  `mesh-fitness`, `mesh-needs`, the autopoiesis lane `mesh-generate → mesh-feed → genome`.
- **Wiring** is checked: `mesh-doctor`'s orphan check ("a tool built to be wired but isn't").
- **Firing** is checked: `mesh-reflex-health` / `mesh-pulse` (mtime aging).
- **Structural coupling / Umwelt** is covered elsewhere: biosemiotics functional-cycle review
  (`docs/reviews/biosemiotics-functional-cycle-closure-2026-07-24.md`), enactivism coupling metric.

## What we do NOT embody — the closure question itself

Every existing check reads each reflex **alone**. None asks the autopoietic question: *does the set
of wired reflexes form a closed loop of mutual dependence, or a feed-forward pipeline with inert
appendages?* Concretely, three axes are distinct and we only had the first two:

| Axis | Question | Tool |
|------|----------|------|
| wired? | is it in cron? (source+crontab) | `mesh-doctor` orphan |
| firing? | did it run? (mtime) | `mesh-reflex-health` |
| **enabled by whom / enabling whom?** | does any constraint DEPEND on its output? | **(none)** |

A reflex can be **wired, firing, and organizationally inert**: it spends a cron slot, CPU, and a
growing log every N minutes, while its product feeds **no other constraint**. That reflex is outside
the organization's closure — and both existing checks pass it green. Autopoiesis names exactly this
gap, and the process-enablement graph is exactly the instrument that sees it.

## Concrete application (ONE, implemented + gated file)

**File: `scripts/mesh-closure`** (new; on-demand, `orphan-ok`, advisory — never auto-acts). It
builds the process-enablement graph over the mesh's own constraints:

- **Constraints** = the wired reflexes in `~/.mesh/reflexes.cron`.
- **Enablement edge** `A → B` = "B's source *consumes* A's product", approximated **conservatively**
  by "B's source invokes `mesh-A`" (mention-based, so edges are OVER-counted → `PERIPHERAL` is
  UNDER-flagged; the peripheral list is a high-precision lower bound).
- **Classification:** `CORE` (consumes AND is consumed — interior of the organization) ·
  `SOURCE` (pure producer — a boundary sense) · `PERIPHERAL` (product feeds no other constraint) ·
  `UNKNOWN` (source file absent — honest degradation, never faked as peripheral) · plus `LOOP a↔b`
  (a literal *closed constraint pair* — mutual dependence, the atom of closure).

**Live run 2026-07-28** over the real genome + `reflexes.cron` (216 wired reflexes):

```
CORE=173  SOURCE=5  PERIPHERAL=36  UNKNOWN=2  LOOPS=82
```

The mesh is **mostly closed** — 173 interior reflexes and 82 mutual-dependence loops (e.g.
`mesh-autowire ↔ mesh-land`, `mesh-chat ↔ mesh-doctor`, `mesh-algedonic ↔ mesh-stress`): this is a
real self-maintaining organization, not a pipeline. But **36 reflexes are PERIPHERAL** — wired,
firing, maintained by their cron slot, yet no genome tool consumes their output. Some are legitimate
(an actuator's consumer is the *world*: `mesh-note3-*` raw senses, `mesh-bruno-watch`); others are
genuine candidates for review — `mesh-wakeup-attrib`, `mesh-unit-churn`, `mesh-gate-evolve`,
`mesh-child-sim`, `mesh-study-bridge` are mentioned by **no other tool** (verified by direct grep).
The output is **advisory** — "judge each flag" — matching `mesh-doctor`'s WARN discipline; it never
prunes.

**Gate: `mesh-closure --test`** — a synthetic fixture graph (`mesh-fa→mesh-fb↔mesh-fc` loop,
`mesh-fd` mentioned by nobody → PERIPHERAL, `mesh-fe` wired-but-no-source → UNKNOWN) asserts every
class and the loop. **RED-first verified:** forcing the classifier to call everything `CORE`
(`if false` on the PERIPHERAL branch) turns it red (`expected 'mesh-fd PERIPHERAL'` +
`--peripheral did not list mesh-fd`); restoring goes green. The gate proves the classifier genuinely
*distinguishes* enabled-nothing from interior, not that a string is present.

## Not discarded — why it applies

It is operational (a graph over a file we already keep, not philosophy), it is a *different axis*
from every existing check (wired / firing / **depended-upon**), it is genuinely un-embodied (no tool
computed our own enablement graph), the mechanism is live (2015 JTB → 2024 arXiv → ALIFE 2026), and
it produced a real, precise, non-vacuous artifact on the first live run. Landing point we have not
been: **the mesh's reflex set read as an autopoietic organization — which parts are self-maintaining
closure, and which are enabled appendages that enable nothing.**
