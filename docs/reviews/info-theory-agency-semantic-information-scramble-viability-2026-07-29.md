# Live-literature review — information theory of agency: SEMANTIC INFORMATION — most stored mutual information is syntactic (meaningless); only the fraction whose *scramble costs viability* is meaning

Date: 2026-07-29 · lane: genome (idea-queue LITERATURE task — information theory of agency / empowerment /
predictive information, from the angle of a **foundational idea we applied too loosely**) · status: fix in
tree, uncommitted (steward lands)

## Where we had already been (checked before landing, so this doesn't double-count)

Information theory of agency is a heavily-worked mesh seam. The embodied set, confirmed before landing —
every piece measures a *syntactic* quantity (a bit-count of correlation) and treats all of it as if it
mattered:

- **empowerment — action→future-sensor-state MI** (channel capacity of the sensor-actuator loop) →
  `scripts/mesh-algedonic` AGENCY_INFO sidecar.
- **instrumental / multi-agent empowerment** (through other minds; interference channel) →
  `scripts/mesh-mind-control:155`, `:1324`.
- **Maximum Occupancy Principle** (occupy future action-path space) → `scripts/mesh-vitality`.
- **predictive information / excess entropy** I(past;future) as a structure-vs-noise discriminator →
  `scripts/mesh-precision --num` `pred_info`, `mesh-sensorium`/`mesh-rhythm`.
- **transfer entropy** (directed lagged info flow; Schreiber 2000) → `scripts/mesh-cooscillate`.
- **synergy / redundancy / O-information** (leave-one-axis-OUT replay: does REMOVING an axis flip the
  verdict?) → `scripts/mesh-algedonic --synergy`, `scripts/mesh-home-state` ∂ᵢΩ gradient.
- **overwrite control vs hidden-state identification** (Csaky 2026) → review 2026-07-24.
- **assistive / process (closed-loop) empowerment**, **nostalgia / memory-depth** → reviews 2026-07-28.

Every one of these asks *how much* correlation a channel carries, or *whether removing the channel* changes
a verdict. **None asks the different, foundational question: of the correlation a channel DOES carry, how
much is causally necessary for the mesh to stay viable — versus present, logged, voting, and meaningless?**

## The concept not yet embodied — SEMANTIC INFORMATION

**A. Kolchinsky & D. Wolpert, "Semantic information, autonomous agency and non-equilibrium statistical
physics," *Interface Focus* 8:20180041 (2018)** — <https://arxiv.org/abs/1806.08053> ·
<https://royalsocietypublishing.org/doi/10.1098/rsfs.2018.0041>.
Live continuation read: **D. R. Sowinski, J. Carroll-Nellenback, R. N. Markwick, ... A. Frank, M. Gleiser,
"Semantic Information in a Model of Resource Gathering Agents," *PRX Life* 1, 023003 (Oct 2023)** —
<https://arxiv.org/abs/2304.03286> · <https://journals.aps.org/prxlife/abstract/10.1103/PRXLife.1.023003>
(popular write-up: <https://phys.org/news/2023-11-theory-semantic-realistic-survival.html>).

The move: **syntactic** information is the raw mutual information a system stores about its environment
(what Shannon counts; what all our MI/TE/PI tools count). **Semantic** information is the *subset of that
correlation which is causally necessary for the system to maintain its own existence* — its viability.
"Causal necessity" is operationalised by a **counterfactual intervention that SCRAMBLES the correlation
between system and environment while preserving the marginal statistics**, then measures the response of a
**viability function** (Sowinski: the forager's expected lifetime; viability is *endogenous* — no exogenous
reward/utility). Their central empirical finding: **there is a critical scramble fraction.** Below it,
destroying correlation costs *no* viability — that information was syntactic noise; above it viability
collapses. So **semantic efficiency < 1: most stored mutual information is meaningless**, and the meaning
lives in a thin, identifiable core.

**This is the loose application we've been making.** AGENCY_INFO, transfer entropy, predictive information
all report a positive bit-count and we read "this channel is informative → it matters." The KW/Sowinski
result says: a channel can be reachable, busy, correlated, *and semantically empty*. That is the exact shape
of our recurring failures — the hollow sense (`mesh-mag`/`mesh-gyro` cron-green while stale), occupancy≠
audibility, "non-empty is not correct." Semantic information gives the operational test we never ran: don't
ask whether the channel carries bits, ask whether **scrambling its tie-to-the-world costs the mesh any
confidence in what it decides.**

Distinct from what we have — this is not O-information/PID re-labelled:

- ∂ᵢΩ and `--synergy` **WITHHOLD** an axis (set it absent) and check a verdict flip. Semantic scrambling
  **keeps the axis present and voting** but feeds it *marginal-faithful-but-wrong* values — so a spuriously
  correlated sensor doesn't just go silent, it can actively **mislead**, and the graded viability response
  (with a critical fraction) is what separates load-bearing from empty. A sense can pass leave-one-out
  relevance yet be semantically hollow if its correlation was spurious.

## The application — `scripts/mesh-home-state --semantic` (report-only, on-demand)

`mesh-home-state` fuses the sensor stream into a home-situation verdict, and already carries the
*observational* O-information gradient ∂ᵢΩ (does adding axis *i* move the verdict). It had no *interventional*
counterpart. Added `--semantic`:

For each value-bearing sensor key in `~/.mesh/sensors.log`, time-permute a **fraction** of that key's values
(marginal preserved, correlation-with-the-instant destroyed), re-run the **real** inference against a
hardlink-cloned `$HOME` (instant; writable outputs get private copies so real state is never clobbered), and
read the drop in the winning-vote **margin** — the organ's confidence, i.e. its *viability as a situation-
resolver*. Sweep the fraction ∈ {0.25, 0.5, 0.75, 1.0}; the smallest fraction that spends ≥½ the full drop
is the Sowinski **critical fraction**. Verdict per key: `SPOF` (scramble flips the state) / `LOAD-BEARING`
(rel_load ≥ 0.5) / `PARTIAL` / `SEMANTICALLY-EMPTY` (present + voting, scramble costs ~no confidence) /
`CONSTANT` (identical values → permutation is a mathematical no-op → un-testable by temporal scramble,
reported as honest n/a, **not** faked "empty"). Honest n/a when there is no confident baseline to attribute
(state UNKNOWN / senseless node) → exit 2.

**Live readout on this node (mesh-home, base = ACTIVE, margin 1.0):**

```
ble_named   n=3031  rel_load=1.000  LOAD-BEARING   crit_f=0.50
ble_top     n=3031  rel_load=1.000  LOAD-BEARING   crit_f=1.00
ble_count   n=3031  rel_load=0.000  SEMANTICALLY-EMPTY
cpu_load1   n=3062  rel_load=0.000  SEMANTICALLY-EMPTY
mem_used_pct n=3062 rel_load=0.000  SEMANTICALLY-EMPTY
room_sense  n=3061  rel_load=0.000  SEMANTICALLY-EMPTY
```

The `ACTIVE` verdict rides entirely on **which BLE devices are named / how strong the top device is**;
`ble_count`, host CPU/memory, and — notably — `room_sense` are logged every cycle and vote, but scrambling
their tie-to-the-world costs zero confidence. `semantic efficiency < 1`, exactly as KW/Sowinski predict, on
real mesh data. (That `room_sense` reads empty *here* is a finding worth a senses look, not a claim the
organ is broken — its contribution may be conditional on states not present in the current window.)

## Verification (per doctrine — a gate seen to fail)

- Hermetic `--test` gate added: room-sense=EMPTY anchors an AWAY competitor, recent `ble_named` presence
  vetoes it → the margin *rides* on `ble_named`'s recent value (AWAY-vs-present is presence-driven, not
  clock-driven, so the load registers at any hour). Asserts `ble_named` reads load-bearing (rel_load > 0 **or**
  a flip) and constant `wifi_rssi` reads `CONSTANT`/zero-load.
- **Seen RED:** neutering the permutation to an identity (`# BREAK: no shuffle`) makes `ble_named` read
  `SEMANTICALLY-EMPTY` → `smoke-test: FAIL (... mechanism is vacuous ...)`. Restored → green. The gate
  asserts the scramble actually *bites*, not merely that the code path runs.
- Report-only; a mode of the already-cron-wired `mesh-home-state` (no new orphan, no cron change).

## Verdict

**LAND.** One un-embodied foundational concept (semantic information — the syntactic/semantic split via
viability-scramble, KW 2018 / Sowinski PRX Life 2023), one shipped report-only application naming the file
(`scripts/mesh-home-state --semantic`), validated live and gated with a break-seen-red test. Uncommitted in
the tree; steward lands.
