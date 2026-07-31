# Live review: φ (phi) accrual failure detector → BLE presence DEPARTURE suspicion

Date: 2026-07-31 · reviewer: genome@mesh-home · area: **distributed-systems coordination / failure
detection** · cross-domain transfer into the **sensor mesh** · status: **landed (uncommitted, steward lands)**

## The concept (named + cited)

**The φ accrual failure detector** — Hayashibara, Défago, Yared, Katayama, *The φ Accrual Failure
Detector*, IEEE SRDS 2004. Instead of a **binary** verdict ("node dead after N missed heartbeats /
a fixed timeout"), an *accrual* detector outputs a **continuous suspicion level φ** derived from the
**observed heartbeat inter-arrival distribution**:

> φ(t) = −log₁₀ P(next heartbeat arrives later than the current silence t)

so φ = 1 ≈ a 10 % chance we are wrong to declare it gone, φ = 8 ≈ 10⁻⁸. The decisive property is that
it is **self-calibrating per source**: a jittery source's larger variance automatically widens the
suspicion window, so temporary congestion does **not** cause a false conviction — the application picks
its own threshold (convict at φ) at query time rather than the detector hard-coding one deadline.

**This is LIVE, not a museum piece.** It is the current default failure detector in **Akka / Apache
Pekko Cluster** and **Hazelcast** (their 2024–2025 docs pin threshold φ ≈ 8–12) and underlies
Cassandra's gossip. Found via:
- φ accrual detector — Akka core docs (live): https://doc.akka.io/libraries/akka-core/current/typed/failure-detector.html
- Apache Pekko 1.3 failure-detector docs: https://pekko.apache.org/docs/pekko/1.3/typed/failure-detector.html
- Hazelcast 5.5 Phi Accrual Failure Detector: https://docs.hazelcast.com/hazelcast/5.5/clusters/phi-accrual-detector
- Original paper (φ Accrual Failure Detector, SRDS 2004): https://www.researchgate.net/publication/29682135_The_ph_accrual_failure_detector

## Why it's a concept we did NOT already embody

The mesh's distsys-coordination coverage is deep on *convergence* metrics (G-Set, PBS t-visibility,
vAoI, HLC, causal-stability frontier, CALM, metastable failure) and one *failure-detection* landing —
**Lifeguard local-health-awareness** on `mesh-reflex-health` (arXiv:1707.00788, 2026-07-29). But
Lifeguard fixes the **observer**'s self-suspicion; it does **not** touch the **shape of the liveness
verdict**, which everywhere in the mesh is still a **fixed timeout / mtime cliff**. The accrual detector
is the orthogonal, unembodied idea: *replace the arbitrary constant deadline with the monitored source's
own rhythm.*

## The cross-domain transfer (the point of the task)

A distributed **sensor** mesh's BLE presence sense is a failure detector wearing sensor clothes: a
device "heartbeats" when it appears in a scan, and we must decide when it has **LEFT**. Today that
decision in `scripts/mesh-presence` is a **fixed cliff** — `HISTORY_GAP_TTL=1800` (30 min unseen →
gap/departed): exactly the arbitrary constant φ-accrual exists to delete.

- A phone seen every scan then suddenly silent waits a flat 30 min to be called gone (slow).
- A device that naturally flaps with ~25 min gaps gets false gone/came-back churn (wrong).

φ-accrual replaces the constant with **the device's own inter-sighting distribution**.

## What landed (file named): `scripts/mesh-presence`

Visibility-only, additive — honest-fusion (raise a graded suspicion, do **not** flip the existing
binary `HISTORY_GAP_TTL` verdict):

1. **`departure_phi <intervals_csv> <seconds_since_last>`** — pure classifier, mirrors the tool's
   existing `rssi_trend_conf` python-heredoc idiom. Returns φ (2 dp) under Normal(μ, σ) of the observed
   inter-sighting intervals; **`UNKNOWN`** below `MESH_PRESENCE_PHI_MINSAMPLES` (default 3 — can't
   estimate variance, so refuse to guess); σ floored by `MESH_PRESENCE_PHI_SDFLOOR` (default 60 s,
   Akka's "acceptable-heartbeat-pause": σ=0 would make φ=∞ on the first stray second of lateness).
2. **`departure_band <phi>`** → `PRESENT` (φ<1) · `SUSPECT` (1≤φ<8) · `DEPARTED` (φ≥8) · `UNKNOWN`
   (Akka/Hazelcast convict-at-8 convention). FALSIFIABLE.
3. **`mesh-presence --phi`** — a per-device readout that reconstructs each MAC's sighting series from
   `~/.mesh/presence.log` (NO BLE scan — runs on an adapter-less node) and dispatches to the **same**
   `departure_phi`/`departure_band` the tests assert (single-source, like `--classify`). Prints φ + band,
   most-suspected-departed first. A graded input for `mesh-perimeter` / `mesh-arrivals` to opt into.

**RED-first gate** (6 new asserts, verified): steady 600 s beat silent 2400 s → **DEPARTED**; a flappy
beat (120/1800/300/2200/600/1700) with the **same** 2400 s silence → **not** departed; steady φ **>**
flappy φ for equal silence (the constant-timeout blind-spot, asserted directly); a device barely past
its mean (650 s) still **PRESENT**; <3 samples → **UNKNOWN**. Broke the variance term (`sd=100000`) →
both φ collapse to 0.31 → two asserts go **RED** (`rc=1`) → restored → GREEN.

**Live proof** (`mesh-presence --phi`, real board):
```
59:21:D1:22:26:74  96.96   DEPARTED  6152s-silent   ← regular device, genuinely gone
4D:86:58:61:49:D2  6.94    SUSPECT   1962s-silent   ← Quest 3, mid-departure (asleep?)
5C:49:7D:92:1E:58  0.27    PRESENT   162s-silent    ← Samsung TV, here
F0:A3:B2:DF:EB:83  0.03    PRESENT   9162s-silent   ← sporadic device: 9162s silence is UNsurprising
                                                       for IT — the flat 30m cliff would have wrongly
                                                       called it gone 2.5h ago. This is the whole win.
```

## Honest limitation (documented, not hidden)

BLE **random/privacy MACs rotate**, so a phone splits its heartbeats across many short-lived MAC
identities → most rotating devices land `UNKNOWN` (too few sightings per MAC). φ-accrual therefore pays
off on **stable-address** devices (public-MAC appliances, the TV/speaker, and any non-rotating peer) —
which is exactly where a persistent departure signal matters for perimeter/occupancy. Extending it
across a rotating device's *attributed identity* (not raw MAC) is the natural follow-on, and belongs to
the attribution layer, not here.

## Not committed — steward lands from the tree.
