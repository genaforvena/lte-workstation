# Literature-to-mesh capability map — 2026-09-16

This is an application-oriented first review for `literature-capability-frontier-20260916`.
The literature is used to generate testable mesh designs, not to claim that a paper's result
transfers automatically to this hardware.

## Findings

### 1. Event-triggered and learned sensing

The survey [Distributed Event-Triggered Estimation Over Sensor Networks](https://doi.org/10.1109/TCYB.2019.2917179)
frames event-triggering as a way to reduce unnecessary sampling/transmission and resource use.
[SmartON](https://arxiv.org/abs/2103.00749) adds learned wake timing and reports 1–7x more captured
events and 8–17x energy efficiency than a charge-then-discharge baseline in its target system.
Related work includes [ACES](https://arxiv.org/abs/1909.01968) and [Amalgamated Intermittent
Computing Systems](https://arxiv.org/abs/2303.13000), which treat energy and intermittent nodes
as scheduling/coverage problems rather than assuming every sensor is continuously available.

**Mesh application:** Note3's significant-motion wake sensor, barometer, light/proximity, and
environmental sensors should feed an event-triggered context collector. The collector should
publish event rate, sampling coverage, battery cost, and missed-event estimates; it must not turn
an absent or sleeping phone into a false zero. A first experiment can compare the current cadence
with motion/barometer-triggered capture over identical windows.

### 2. Multimodal local inference

[A Wearable Multi-Modal Edge-Computing System for Real-Time Kitchen Activity Recognition](https://arxiv.org/abs/2409.06341)
combines six sensor types and local inference, reporting a 184.5-KB model, 87.83% average accuracy,
and 25.26-ms inference on one MCU. Its design rationale is directly relevant: local processing can
reduce latency, transmission energy, and privacy exposure. It also explicitly notes that combining
modalities can improve robustness when error sources are not perfectly correlated, while missing or
private modalities remain a deployment limitation. Related systems include [Measuring what Really
Matters: Optimizing Neural Networks for TinyML](https://arxiv.org/abs/2104.10645) and
[FieldHAR](https://arxiv.org/abs/2305.12824).

**Mesh application:** Build a compact Note3 event classifier from inertial + pressure + light/
proximity + temperature/humidity before sending raw camera/audio. Use camera/mic only as an
escalation modality when the low-power context model is uncertain. Acceptance: measured latency,
energy/battery delta, confusion matrix on a small mesh-specific fixture, and a privacy log showing
which raw modalities stayed local.

### 3. Heterogeneous, intermittent coordination

[MAGEC](https://arxiv.org/abs/2403.13093) applies graph message passing with centralized training
and decentralized execution to coordination under agent attrition, partial observability, and
disturbed communications. Its key transferable constraint is that each agent acts from a local
neighborhood observation; the global state is not assumed to be continuously available. The
[X-IoCA cooperative-agent architecture](https://doi.org/10.3390/s21237843) similarly organizes
robots, hybrid sensor networks, edge/MEC centers, and human operators as cooperating layers.
Related work includes [Graph Neural Networks for Decentralized Multi-Robot Path Planning](https://arxiv.org/abs/1912.06095)
and [Amalgamated Intermittent Computing Systems](https://arxiv.org/abs/2303.13000).

**Mesh application:** Model mesh nodes as a capability graph whose edges carry freshness, coverage,
latency, and confidence—not just online/offline. Use local policy/routing decisions that degrade
gracefully when Redmi sleeps, Note3 USB disappears, or a compute node drops. A practical first
version is a capability-aware task allocator: select the least-cost node that currently satisfies
the task's sensor/actuator predicate, with explicit abstention when no node does.

### 4. Human-facing embodied agency

The search surfaced recent embodied-agent work, but the strongest immediately applicable evidence
for this mesh is architectural rather than a promise of general autonomy: human-facing output,
physical-device context, and distributed sensors need an explicit feedback loop. The iMac's live
`/usr/bin/say`, Note3 speaker/torch/IR, camera, and operator's physical-device credential lanes make
this a concrete mesh surface. It should be treated as a controlled actuator graph with receipts,
not as an unconstrained agent that can act on the operator's behalf.

## Prioritized proposals

| priority | proposal | affected nodes | why now | acceptance predicate |
|---|---|---|---|---|
| P0 | Capability registry with states `declared`, `reachable`, `wired`, `verified`, `stale`, `unknown` | all; especially Note3 + mesh-home | the live card already reports 27 identity conflicts; current declarations mix unlike epistemic states | a refreshed matrix reconciles node, source, artifact, freshness, and owner; mutation test proves missing artifact cannot render verified |
| P1 | Note3 event-triggered multimodal context collector | Note3 + mesh-home | rich physical sensor surface is live; literature supports adaptive sampling and local fusion | real sensor tape includes coverage/energy/freshness; benchmark compares periodic vs triggered collection and records missed events |
| P1 | Capability-aware task allocation/fallback | mesh-home, Note3, Redmi, iMac, phaedra | current fleet is heterogeneous and intermittently reachable | induced node loss selects a valid alternate or emits typed unknown; no stale registry claim is used as availability |
| P2 | Prove and safely expose Note3 IR actuator | Note3 + mesh-home | hardware declaration and root backend exist, but no frame artifact yet | one reversible, target-bounded frame emission with receiver-side or electrical artifact and rollback/disable path |
| P2 | iMac second human I/O vantage | iMac + mesh-home | `say` is live; camera/mic/notification capabilities are still unmeasured | end-to-end speech artifact plus explicit permission/target gate; camera/mic are separately probed and privacy-scoped |

## Limits and open evidence

- The event-triggered survey was verified from indexed metadata/abstract; its full text was not
  available through the research index, so no stronger claim is made.
- Research results are mostly simulations or purpose-built embedded systems. The mesh must measure
  its own battery, latency, modality quality, privacy, and failure behavior.
- Redmi's current SSH refusal prevented a fresh Termux capability read; it remains `unknown`, not
  absent. Phaedra's collector outputs and the iMac's camera/mic surface need direct artifact probes.

## Operational synthesis update — availability is a vector, not a boolean

The live census supplied a concrete failure case for the heterogeneous-coordination proposal:
Tailscale reported Redmi online at `100.103.99.16`, while a contemporaneous SSH/Termux battery
probe on port 8022 returned `Connection refused` (2026-09-16T14:47Z). Conversely, the iMac media
read succeeded over Tailscale SSH at 14:40:58Z, while mesh-home's own capability card at 14:46:01Z
reported `identity-coherence=CONFLICTED (27)` despite `invariant-check=OK`.

Therefore the capability-aware allocator should admit a capability only when all relevant axes
pass independently: node reachability, transport/service reachability, source freshness, artifact
coverage, identity coherence, and actuator safety. A node can be online while a requested organ is
unknown; a node can be physically healthy while its identity metadata is conflicted. This is a
direct mesh application of the intermittent-agent and resilient-coordination literature above.

Minimum acceptance predicate for the proposed registry/allocator:

```text
eligible(capability, request) =
  route_live AND service_live AND freshness_ok AND coverage_ok
  AND identity_consistent AND safety_policy_allows(request)
```

Any false or unknown term must yield `UNKNOWN`/abstain, with the failing axis and retry edge
preserved. This predicate is intentionally stricter than the current online/offline card and is
the central test target for the P0 capability registry and P1 fallback allocator.

## Closure audit — current status

| requirement | evidence status | authoritative evidence / remaining gap |
|---|---|---|
| Census Note3 and mesh-home | proven for current live checkpoint | `docs/mesh-capability-census-20260916.md` and `docs/mesh-capability-census-live-20260916-1428.md`; freshness is timestamped, not permanent |
| Census other reachable nodes | substantially proven for online Redmi, iMac, phaedra, and Windows reachability | direct SSH/ADB/Tailscale probes and explicit unknown states; offline peers remain unprobed |
| Literature review applied to mesh | proven for event-triggered sensing, local multimodal inference, intermittent coordination, and human-facing I/O | this document maps each to a concrete mesh predicate or proposal; purpose-built-system results still require mesh measurement |
| Prioritization with safety and verification predicates | proven as design | ranked P0–P2 packet and availability-vector predicate; no unbounded actuator was enabled |
| Exact-owner implementation tasks | provisional only | `docs/task-plans/mesh-frontier-ranked-implementation-20260916.tsv` and board handoff exist; canonical `mesh-task create` has not yet persisted rows |
| End-to-end first-win implementation | incomplete | Note3 environmental and iMac media reads are verified; registry, fallback allocator, Redmi trigger consumer, and iMac camera/mic promotion remain unimplemented or unverified |

This audit deliberately keeps the frontier goal open. Completion requires canonical owner-task rows,
then implementation and live acceptance evidence for the selected P0/P1 improvements.
