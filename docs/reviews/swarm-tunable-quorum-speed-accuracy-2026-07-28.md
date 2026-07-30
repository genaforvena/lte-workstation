# Swarm intelligence live review — the *tunable quorum threshold* (speed↔accuracy), 2026-07-28

**Area:** swarm intelligence & stigmergy · **Angle:** an operational mechanism we do NOT already embody.

## What we already embody (skipped, per [[mesh-forage-pheromone-entropy]])

The swarm/stigmergy lane already carries three landings: **pheromone-entropy foraging evenness**
(dead-lane diagnostic), the **no-entry / negative-pheromone** repellent (abandoned-hold detection), and
**density-adaptive evaporation** (congestion shrinks the stale-eviction rate in `mesh-dispatch`). Those
model *deposit feedback* and the *evaporation rate*. The distinct un-embodied neighbour this review
lands: **the quorum THRESHOLD itself, tuned along a speed↔accuracy axis.**

## The mechanism (named + cited)

**The tunable quorum threshold** — house-hunting ants (*Temnothorax / Leptothorax albipennis*) run a
*single* decision algorithm and tune **one parameter, the quorum threshold** (the number of nestmates
that must accumulate at a candidate site before the colony commits) to move the whole decision along a
**speed–accuracy trade-off**: **lower the quorum under harsh/urgent conditions → commit faster, accept
a good-enough option; raise it under benign conditions → slower, more accurate.**

Sources (read 2026-07-28):
- **Marshall, Franks et al., "A tunable algorithm for collective decision-making," *PNAS* 103(28):2006**
  (doi 10.1073/pnas.0604801103) — the "tune one parameter → speed vs accuracy" result. *(PNAS page
  returned 403 to the fetcher; grounded via the indexed abstract + the corroborating sources below.)*
- **Franks et al., "Speed versus accuracy in decision-making ants,"** and the *Temnothorax* nest-choice
  models (PMC4632542, "Computational model of collective nest selection … heterogeneous acceptance
  thresholds"): *"under harsh conditions, ants lower quorum thresholds and may accept relatively
  low-quality nests in order to prioritize speed."*
- **Live literature (still-published):** *"Minimalist Protocols for Quorum Sensing in Robot Swarms,"*
  Swarm Intelligence / ANTS 2024 (Springer, doi 10.1007/978-3-031-70932-6_11) — quorum-level estimation
  on resource-constrained robots, trading precision against speed of the quorum assessment; and *"A
  Geometry-Sensitive Quorum Sensing Algorithm for the Best-of-N Site Selection Problem"* (arXiv
  2206.00587). Confirms the mechanism is an active, continuously-published area, not a fixed classic.

Why it is genuinely un-embodied: the mesh has many count-then-commit decisions (arrivals debounce,
`mesh-lan-newdevice` promote-runs, presence miss-counts) but **every quorum count is a hard constant.**
No organ tunes its commit threshold to conditions — the exact move the ant literature makes.

## Concrete application (landed, uncommitted)

**File: `scripts/mesh-arrivals`** — the who's-around life-event sense. Its LEFT decision is a quorum:
a named device is declared `[left]` only after `MESH_ARRIVAL_MISSES` (default **3**) consecutive absent
BLE scans — a debounce against RSSI flicker. That quorum was a **fixed constant**; it is now
**posture-adaptive**, tuned to `mesh-operator-home`'s cached verdict (read READ-ONLY from
`~/.mesh/.op-home.state`, never invoked — no second writer):

| operator posture | condition analogue | quorum | trade |
|---|---|---|---|
| **AWAY** | departure EXPECTED, low false-left risk → *harsh/urgent* | **base−1 (→2)** | **SPEED** — prompt `[left]` edges |
| **HOME** | people milling → RSSI flicker, high false-left risk → *benign* | **base+1 (→4)** | **ACCURACY** — damp the flap |
| UNCERTAIN / unreadable / **stale** (>30 min) | no posture | **base (3)** | honest fallback — no adaptation |

This is faithful to the ant direction (harsh→lower→speed, benign→higher→accuracy) and it is *only ever
useful*: while HOME it suppresses the flicker-driven "left/arrived" spam that motivated the debounce in
the first place; while AWAY — when a departure is the likely truth and false-left risk is low — it
reports the real edge one scan (~5 min) sooner. Implemented as a pure `effective_misses()` function
(deterministic, file-read-only) so the gate can assert every branch.

### Verification (artifact, not claim)

- **Unit gate (RED→GREEN):** new `--test` block asserts AWAY→2, HOME→4, UNCERTAIN→3, stale→3, absent→3.
  Broke the AWAY branch → `smoke-test: FAIL (AWAY must LOWER the quorum for speed)` exit 1; restored →
  `smoke-test: ok` exit 0.
- **End-to-end (the real LEFT edge, not just the function):** seeded `Quest 3`, then fed empty scans.
  Under **AWAY** the `[left]` edge fired on the **2nd** empty scan; under **HOME** it was still held
  after the **3rd** — the adapted quorum steers the actual decision, not merely a helper.

Additive / non-breaking: default (UNCERTAIN/absent posture) behaves byte-identically to the old fixed
`MESH_ARRIVAL_MISSES=3`. Deltas overridable via `MESH_ARRIVAL_MISSES_{HOME,AWAY}`; freshness window via
`MESH_ARRIVAL_OPHOME_MAXAGE`.

**Natural next step (unwired):** the same tunable-quorum knob fits `mesh-lan-newdevice`'s
`PROMOTE_RUNS` (how patiently an unknown MAC is tolerated before auto-trusted) — AWAY should stay
suspicious longer, HOME accept sooner. Left for a future review so this one lands exactly one mechanism.
