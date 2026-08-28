# Literature review — swarm intelligence & stigmergy → `scripts/mesh-watchtower`

**Arm:** treated (assigned)
**Date:** 2026-08-28
**Window:** genome@mesh-home
**Target organ:** `scripts/mesh-watchtower` — assigned by coin at p=0.20 from the 557 never-reviewed
tools in the lane's own denominator. Not chosen by me, not retargeted.
**Area:** swarm intelligence & stigmergy, from the angle of an OPERATIONAL mechanism.

---

## Verdict

**It applies, and it lands on a defect that is already in the code — not on a metaphor.**

The concept I am importing is **the third pheromone operator: DIFFUSION (dispersion)**, as distinct
from deposition and evaporation. The mesh embodies the first two everywhere under other names
(a log append is a deposit; a sliding window, a throttle, a decay band is evaporation). It embodies
the third **nowhere**: every sense in this mesh aggregates strictly per-key, and no key's evidence is
ever allowed to reinforce a NEIGHBOURING key's. That is the operator I could not find an analogue for,
and it is the one that makes an individually-subthreshold, collectively-structured pattern visible.

## Where it comes from (live sources, read 2026-08-28)

- **Phormica: Photochromic Pheromone Release and Detection System for Stigmergic Coordination in Robot
  Swarms** — *Frontiers in Robotics and AI* (2020), and the pheromone-mobility line that follows it
  (e.g. *Connectivity-Aware Pheromone Mobility Model for Autonomous UAV Networks*, arXiv:2210.06684).
  These are the papers that state the artificial-pheromone contract explicitly as **three** dynamics —
  *release/aggregation, evaporation, and **diffusion*** — rather than the two most engineering
  write-ups reduce it to. The diffusion term is not decoration: it is what converts a set of
  independent point measurements into a FIELD with spatial structure.
  <https://www.frontiersin.org/articles/10.3389/frobt.2020.591402/full> ·
  <https://arxiv.org/pdf/2210.06684>
- **Stigmergy: from mathematical modelling to control** — PMC11371424 (2024). The current framing of
  the open problem: *which* environmental modification do you actually need for a desired collective
  behaviour? It proposes treating swarm and environmental modification as continua so the required
  modification can be designed rather than guessed. This is the paper that makes "add a pheromone
  field" a design question with an answer instead of a vibe.
  <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11371424/>
- **Sematectonic vs marker-based stigmergy** — Phan & Russell, *Quantitative information in
  sematectonic stigmergy for swarm robots*. The distinction that names what watchtower is looking at:
  the scanners leaving SYNs on our public NIC are not signalling each other with markers, they are
  reading and modifying the **work itself** (the reachable-host space). Their coordination is
  sematectonic. <https://www.semanticscholar.org/paper/0ace6c0f231d1bb910f74d7a05a8acd8ed7eb44a>
- **H. Van Dyke Parunak, "Adversarial Stigmergy Patterns"**, INCOSE *Insight* 14(2) 2011 — stigmergy
  read from the defender's side, i.e. the frame in which watchtower's subject IS a swarm.
  <http://www.parshift.com/s/110701AdversarialStigmergyPatterns-Essay.pdf>

## Why it is not something we already embody

The mesh's doctrine already carries the *temporal* half of this in several rules — coverage =
window ÷ cadence, a saturated level is not a state, prefer the kernel's monotonic accumulator. Every
one of them is about a single key measured better over time. There is no rule, and no tool, in which
**an observation at key *k* raises the evidence at key *k±1***. Search the sense tier: `mesh-tcp-metrics`
keys per destination, `mesh-mlme-tap` per episode, `mesh-drop-stages` per stage, `mesh-lan-health` per
host. All marginal, all independent. Diffusion is genuinely absent.

## The defect it lands on (measured, in the current code)

`scripts/mesh-watchtower`'s radiation classifier (`RAD_PY`, lines 122-150) gathers exactly the 2-D
object this mechanism is defined on:

```
syns.append((f[1], int(f[2])))      # (source ip, destination port)
```

…and then, three lines later, **throws the joint distribution away and reports two independent
marginals**:

```
probes[port] = probes.get(port,0)+1     # 1-D marginal over ports
srcs[ip]     = srcs.get(ip,0)+1         # 1-D marginal over sources
...top(probes,5)... top(srcs,3)...      # top-5 ports, top-3 sources
```

Those two marginals cannot separate three threat shapes that mean completely different things:

| shape | what it is | marginals |
|---|---|---|
| 1 source × 5 ports | one host fingerprinting us | top-src 1 tall, top-ports 5 short |
| 5 sources × 1 port each | five unrelated bots, background noise | top-src 5 short, top-ports 1 tall |
| 5 sources × the same 5 ports | **a coordinated distributed sweep** | top-src 5 short, top-ports 5 short |

The third row is the one that matters and it is the one that renders as *quietest* — every cell low,
nothing at the top of either list. A field with a diffusion term sees it immediately, because the five
sources' deposits land in adjacent port cells and reinforce into one connected ridge whose **mass** is
large even though no **cell** is.

The same blindness sits on the `--edge` verdict, which is a scalar:

```
spike = " SCAN-SPIKE!" if (delta is not None and delta > int(os.environ["SPIKE"])) else ""   # SPIKE=200
```

`delta` is the change in the TOTAL knock count. The last live rows (2026-08-20T16:13Z) ran `Δ+48` and
`Δ+51` per 30-minute run, so the threshold sits at ~4x the observed rate: any scan that distributes
itself below a 4x total-volume bump is structurally invisible no matter how coordinated it is.

## The proposal — ONE concrete change

**In `scripts/mesh-watchtower`'s `RAD_PY`, keep the joint and add a diffusion pass over it.**

Deposit into a field `F[src_/24][port_bucket] += 1`. Evaporate across runs (it is already a bounded
sample, so the evaporation constant is the sample cadence). Then **diffuse**: one pass where each cell
gains a fraction κ of its neighbours' mass along BOTH axes — port-adjacency (a sequential sweep) and
/24-adjacency (a botnet renting one allocation). Publish, beside the existing marginals and never
instead of them, the mass and extent of the largest connected component above the field's own median.
That number is the shape the marginals cannot express: a broad low ridge is a **coordinated sweep**, a
single sharp peak is **one loud host**, and a flat field is genuine background radiation.

Publish κ, the bucket widths and the sample window IN the reading — a diffused value that does not say
how far it was smeared is not interpretable, and this mesh has already paid for readings that omit
their own window.

## Two things that must come first, and one of them is a live defect

1. **The organ is DORMANT and this proposal is worth nothing until it is wired.** `# reflex-cadence:
   off` (GPU-QUIESCE 2026-07-24); `reflexes.cron:138` is commented out; the last row in
   `~/.mesh/watchtower.cron.log` is **2026-08-20T16:13:03Z, eight days ago**. A mechanism proposed for
   a switched-off sense is a design note, not a capability.

2. **The knock census is contaminated by US, and diffusion would AMPLIFY that.** The last live rows
   read `loudest=100.94.116.17(??×21908)` out of `knocks=74168` — that is a **100.64/10 CGNAT
   Tailscale address, our own peer**, accounting for ~30% of what the tool presents as "who is scanning
   the mesh's public face". Under the current marginal report that is merely a misleading top-talker
   line. Under a diffusion field it is worse: a 22k-deposit peak smeared across its whole neighbourhood
   manufactures a giant false ridge and the new verdict is born lying. **Excluding the mesh's own
   ranges from the knock tally is a prerequisite for this change, not a follow-up** — and it is worth
   fixing on its own merits regardless of whether the diffusion idea is ever built.

   (Note the polarity trap when fixing it: an allowlist of "our own ranges" fails toward silence as the
   mesh grows. Gate on what the source CLAIMS to be — CGNAT/RFC1918 by prefix — and let anything
   unlisted count LOUD.)

## Cost / honest scope

The diffusion pass is ~25 lines of pure Python inside an already-pure, already-fixture-tested
classifier (`RAD_PY` has fixture assertions at lines 250-257), so it is testable without a network and
without the public node. The expensive parts are not the mechanism: they are re-wiring the organ (an
operator decision — it was quiesced deliberately) and the self-contamination fix. I did **not** write
the change: watchtower is not mine to re-arm, and `--radiation` is explicitly on-demand rather than
cron-wired, so this lands as a design with a named file, a named function and named line numbers.
