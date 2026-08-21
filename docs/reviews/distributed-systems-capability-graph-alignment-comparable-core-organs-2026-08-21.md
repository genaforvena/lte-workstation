# Live literature review — distributed systems coordination

**Area:** gossip / CRDTs / eventual consistency · **Angle:** a concrete METRIC the field measures itself with
**Date:** 2026-08-21 · **Organ:** `scripts/mesh-organs` (`--align`) · **Status:** uncommitted in the tree, steward lands

---

## The concept we did not embody

**Capability Graph Alignment (CGA)** — *"consistency of agent capability maps gossiped across peers
(e.g., which agent can do what task)."*

| Source | Where | What it says |
|---|---|---|
| **A Gossip-Enhanced Communication Substrate for Agentic AI: Toward Decentralized Coordination in Large-Scale Multi-Agent Systems** — Nafiul I. Khan, Mansura Habiba, Rafflesia Khan | [arXiv:2512.03285v1](https://arxiv.org/abs/2512.03285), 2 Dec 2025, **§10.3 "Semantic and Relational Consistency Metrics"** | Proposes four metrics for gossip-based *agentic* coordination — **Capability Graph Alignment**, Semantic Convergence Score, Relational Drift Index, Intent Consistency Rate — on the argument that *"one of the central gaps in current agent communication is the lack of semantic coherence across agents"*, and that these are *"absent from RPC-based systems like MCP or A2A"*. |
| **Revisiting Gossip Protocols: A Vision for Emergent Coordination in Agentic Multi-Agent Systems** | [arXiv:2508.01531](https://arxiv.org/html/2508.01531v1), Aug 2025 | Same turn in the live literature: gossip re-read as an *agent-coordination* substrate rather than a replica-repair one. |

The point of the family is that classical distributed-systems metrics — latency, throughput, set
convergence — **measure the wrong replicated structure** for a fleet of agents. They measure the
message log. They do not measure whether the agents' *maps of each other* agree.

## Why it was a gap here — checked, not assumed

Every convergence metric this mesh owns measures the **board**, a G-Set of immutable lines:

- `mesh-converge` — Merkle root + inconsistent window (2026-07-13)
- `mesh-chat-sync` — Jaccard J‰ / similarity regime (2026-08-15) · causal-stability frontier
  (2026-07-28) · PBS t-visibility `--lag` · vAoI/Age-of-Gossip · HLC ordering
- `mesh-chat --gaps` — omission detection (2026-08-20) · `mesh-promises` — CALM/I-confluence, ERA epoch finality
- `mesh-presence` — φ-accrual · `mesh-membership-crdt` — anchored OR-Set

The **capability map is a second replicated structure**, and nothing compared two copies of it.
`mesh-organs` builds the fleet map **from the calling node's own vantage** (local `mesh-card` + one
SSH per peer, `scripts/mesh-organs:226-302`); `mesh-organ` — the capability *router* — then routes
on that local map. Verified: no tool in `scripts/` SSHes `mesh-organs` to a peer, so two routers can
answer `mesh-organ camera` differently **forever**, both maps locally honest, nothing measuring it.

## The correction the paper's one-line definition needs

CGA as published is a single agreement number. A single number **cannot separate "we disagree about
X" from "one of us cannot SEE X"** — and in a real fleet the second dominates. The two have opposite
remedies (reconcile a roster vs. repair a path), and the naive number points at neither.

So the metric lands with the score computed **only over the COMPARABLE CORE** — nodes both sides
could actually read — and blindness reported **beside** it, never folded in. This is the honest-fusion
rule one ring out from `an-absence-qualified-by-its-field-reads-as-absence-of-the-fact`: `mesh-organs`
already renders a non-reading as `(ssh fail)`/`(offline)` with `live:0,total:0`, and **any consumer
that counts caps reads that 0 as "offers nothing"**. Three buckets the one number collapses:

- **BLIND** — one side sighted, one blind. Not a capability difference. And *blind* itself hides a
  repairable fault, so it is sub-classed: **STALE-ADDRESS** (the blind side's `~/.mesh/nodes` names
  an address that is not the peer's live one) vs **UNREACHABLE** (the peer really is unreachable).
- **UNPAIRED** — a key in only one map. A hostname/tailscale-name skew must never render as a
  capability fault, and must not enter the score.
- **OPAQUE** — blind at both. No evidence either way; excluded and counted.

## What the first measurement found — a live, silent, day-old fault

```
$ bash scripts/mesh-organs --align phaedra
=== CGA mesh-home vs phaedra ===
  CGA 1000 core=1 agree=1 differ=0 blind=1 unpaired=0 opaque=5 pairs_inter=7 pairs_union=7
  verdict: cga=1000permille over the comparable core
  BLIND    mesh-home — unseen at phaedra (marker: ssh-fail), seen at mesh-home
                    -> STALE-ADDRESS registry=100.74.178.97 live=100.81.222.19
  AGREE    phaedra — 7 cap(s), identical
  OPAQUE   GL-MT3000 / Redmi 10 / ilya / imozerov-Default-string / rip — blind at BOTH
```

**phaedra's capability map has believed mesh-home offers NOTHING** — `(ssh fail)`, 0 senses, 0
actuators — while mesh-home offers 13 (`ble body-motion camera irq light link-flap mic` /
`dlna-tv docker-compute shadowsocks speaker tv volume`). Cause, named by the tool and confirmed by
hand: phaedra's `~/.mesh/nodes` holds `mesh-home:mesh-home@100.74.178.97`, **the Tailscale device
deleted on 2026-08-20** when this node's identity was re-created (`CLAUDE.local.md`). The live
address is `100.81.222.19`, and SSH from phaedra to it works — measured in the same run:

```
$ ssh phaedra 'ping -c2 100.81.222.19; ssh mesh-home@100.81.222.19 hostname'
2 packets transmitted, 2 received, 0% packet loss ... mesh-home
```

So the path was never down. One stale line in one file made every capability on this node
unroutable from phaedra for a day, and **from phaedra's own vantage the render was honest** — which
is exactly why no local check could ever have caught it. It takes two vantages.

## The naive number would have libelled a perfectly aligned fleet

Run as mutant M1 (fold blindness into the score, i.e. score the maps exactly as §10.3 defines):

```
CGA 444 core=2 agree=1 differ=1 ...     # "the fleet's capability views are 44% aligned"
```

vs. the honest reading: **1000‰ on the comparable core, plus one blind edge with a one-line fix.**
The naive number both *understates* alignment and *invents a divergence* about a node nobody
disagreed about — it sends you hunting a capability drift that does not exist while the actual
fault (a stale address) is not mentioned at all. Same shape as
`a-two-arm-gate-against-a-live-world-measures-the-world`: an agreement score over maps built from
**different reachability** measures the reachability, not the agreement.

## Landed: `scripts/mesh-organs --align [<peer>]`

Read-only, on-demand, additive. Does **not** change routing — `mesh-organ` is untouched.

- `align_core` is the **hermetic** core: two capability-map JSONs → buckets + CGA per-mille. Pure —
  no network, no clock, no durable write, so `--test` drives the real math (not a stub, not a
  self-grep). Records are **tab-separated**: a node name with a space (`Redmi 10`) shifted the
  columns in the first cut and silently mangled every bucket line.
- Blind edges are sub-classed live by `blind_cause` (peer registry entry vs live Tailscale address).
- Honest exits: `0` measurement · `2` n/a (peer map unreadable, **or an empty comparable core** —
  UNKNOWN(-1), never a fabricated 1000‰) · `1` real fault.

**Gates seen RED** (a gate you have not seen fail is not a gate) — three mutants, each exit 1:

| Mutant | What it breaks | Caught by |
|---|---|---|
| M1 | folds blindness into the score (the published one-number CGA) | `blind edge changed the score: 'CGA 444 …'` |
| M2 | drops the UNPAIRED bucket — a one-sided key scored as an empty cap set | `real divergence mis-scored` |
| M3 | returns 1000‰ when the comparable core is empty | `empty comparable core did not render UNKNOWN` |

One live bug the hermetic tests could **not** catch, recorded honestly: `ts_ip_for` first read only
`.Peer` from `tailscale status --json`. This node is in `.Self`, never in `.Peer`, so our own live
address read as absent and the blind edge was misclassified `UNREACHABLE not-in-live-tailscale` —
a **repairable** fault wearing the word for an unrepairable one. Fixed (`.Self` first, with the
reason in the source); it is a network-shaped fault and stays outside the hermetic gate.

## The repair this points at (NOT applied — single-writer, and it is another node's file)

phaedra's `~/.mesh/nodes` should read `mesh-home:mesh-home@100.81.222.19`. That is a write to a
peer's registry, so it belongs to whoever holds the claim on phaedra, not to this review. Filed to
the board instead.

## Prior coverage checked

G-Set union · Merkle root + inconsistent window · Jaccard similarity-regime · causal-stability
frontier · PBS t-visibility · AoII/AoIV · omission detection · CALM/I-confluence · ERA epoch
finality · φ-accrual · Lifeguard local health awareness · MaxWait consistent cut · metastable
failure. **None of them measures the capability map** — all thirteen measure the board or the
liveness estimate.
