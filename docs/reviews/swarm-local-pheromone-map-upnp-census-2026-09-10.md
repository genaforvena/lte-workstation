# Live literature review — swarm intelligence & stigmergy → `scripts/mesh-upnp-census`

**Arm:** treated (assigned)
**Date:** 2026-09-10
**Window:** genome@mesh-home
**Target organ:** `scripts/mesh-upnp-census` — assigned by coin at p=0.20 from the lane's
614 never-reviewed tools. It was not selected or retargeted.
**Area:** swarm intelligence & stigmergy, from the angle of a recent operational mechanism.

## Verdict

**It applies.** The new mechanism is **asynchronous local virtual-pheromone maps with
selective neighbour propagation**: every agent keeps its own map, deposits and evaporates
locally, and shares only nearby/interesting map information when contact occurs. A global
pattern emerges without a central map owner or synchronized rounds. The distinctive part is
the combination of a local external-memory analogue with *asynchronous, partial* propagation;
it is not just “append observations and gossip the whole log.”

## Live sources read

- Tinoco, Martins & Oliveira, **“PheroCom: Decentralised and asynchronous robot swarm
  coordination framework based on virtual pheromone and vibroacoustic communication,”**
  *Swarm and Evolutionary Computation* 99 (2025) 102083,
  [DOI and publisher abstract](https://doi.org/10.1016/j.swevo.2025.102083). The paper's
  mechanism keeps an independent pheromone map per robot, applies deposit and evaporation,
  and incorporates information from nearby robots; its ViBIT propagation is gossip-like and
  does not require whole-swarm synchronization. Its experiments compare environments and swarm
  sizes and report surveillance performance, while also naming local-neighbour contact and
  bandwidth/energy cost as limitations.
- Salman et al., **“Automatic design of stigmergy-based behaviours for robot swarms,”**
  *Communications Engineering* 3, 30 (2024),
  [full article](https://www.nature.com/articles/s44172-024-00175-7). I read the paper's
  Habanero design and results: modular probabilistic finite-state controllers are optimized in
  simulation and then run by physical e-puck swarms. It demonstrates that the semantics and
  use of a pheromone trace can be mission-specific even when the modules are generic, and
  explicitly leaves intensity/decay tuning and combinations of direct plus indirect
  communication open.
- Patiño Padial et al., **“Swarming intelligence in self-propelled micromotors and
  nanomotors,”** *Nature Reviews Materials* 10, 947–963 (2025),
  [review](https://doi.org/10.1038/s41578-025-00818-x). This recent field review places
  stigmergy, quorum sensing, taxis and synchronization among distinct collective mechanisms;
  it emphasizes the unresolved engineering problems of information storage and communication
  between swarms. That is why the PheroCom map-and-partial-propagation mechanism is the useful
  transfer here, rather than another generic “swarm is decentralized” claim.

## Why this is not already embodied

The repository already has pheromone-like deposition/evaporation, diffusion, quorum,
cross-inhibition, and board gossip in other organs. `scripts/mesh-upnp-census` does something
different: each successful run performs one local M-SEARCH, derives a complete current
`sig=...` from the replies, overwrites `~/.mesh/.upnp-census`, and emits `ARRIVED`/`DEPARTED`
only when that single sweep's set differs from the previous set. There is no per-device
continuous score, no local map with independent decay, no selective exchange of only changed
regions, and no asynchronous multi-observer merge. A missed reply therefore participates in
departure semantics immediately; another observer cannot contribute evidence without replacing
this organ with a separate consumer.

## One concrete application

Apply the mechanism inside **`scripts/mesh-upnp-census`** as a bounded, opt-in presence map keyed
by `(device IP, classified service kind)`: on each real SSDP reply deposit a weighted amount;
between sweeps exponentially evaporate the key; and accept from another mesh node only a compact
delta for the relevant device keys, asynchronously, rather than importing that node's whole
census log. Keep the current instantaneous `PRESENT`/`EMPTY` output unchanged, but have the
`--edge` decision consult the merged pheromone value with a declared horizon: emit `DEPARTED`
only after the value crosses the decay threshold, and emit `UNKNOWN` when the local node has no
valid multicast path or the peer evidence is stale. This directly addresses the organ's real
failure mode—one observer's silence being treated as device departure—while preserving the
existing multicast-path guard and making freshness/decay part of the reading.

The first implementation should be fixture-backed and measure false departures, bytes sent, and
time-to-confirm absence against the current single-sweep baseline. The literature does not
justify silently treating a remote node's view as equivalent: PheroCom itself limits propagation
to nearby contact, and UPnP visibility is LAN-scoped.

## Decision

**Land as an implementation lead, not code.** The concept is new at this exact organ and is
operationally relevant, but the review does not introduce a second network protocol or alter
departure semantics without a controlled fixture and a real multi-observer artifact.
