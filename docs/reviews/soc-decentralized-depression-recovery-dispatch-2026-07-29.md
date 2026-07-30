# Decentralized depression-recovery — a LOCAL SOC actuator that needs no m̂ measurement

**Live literature review · self-organizing criticality & power-law dynamics · 2026-07-29 · genome mind**

## Ground already covered (checked first)

Memory `mesh-criticality-covered-critiques` lists ~14 stacked landings on `scripts/mesh-criticality`:
branching-ratio m̂ (MR estimator), dragon-kings, avalanche shape, Sethna-Dahmen crackling, micro/macro
criticality, CSD, drift, entropy-complexity, bin-width artifact, quasicriticality/Widom line, dynamic
range. Critically, the most obvious "operational" move — **actuate a knob toward the m̂≈1 set-point**
— was already proposed 2026-07-24 (`soc-homeostatic-setpoint`, `mesh-pace --crit-gap`) and then
**directly refuted** 2026-07-27 by the edge-optimality landing: m̂≈1 is not a universal law, it is
task/substrate-dependent and the mesh's own board data showed `Edge=EDGE-NEUTRAL` — throughput does
NOT peak at the edge. Re-proposing "measure m̂, actuate toward it" is dead ground.

This review deliberately lands on a **structurally different** mechanism that does not require that
refuted premise at all.

## The concept — LOCAL DEPRESSION-RECOVERY (no global measurement, no set-point)

Searched live (2025 currency): *Network structure influences self-organized criticality in neural
networks with dynamical synapses*, Front. Syst. Neurosci. (2025),
https://pmc.ncbi.nlm.nih.gov/articles/PMC12213684/ — a 2025 re-examination of how **short-term
synaptic depression** alone (no branching-ratio measurement, no global controller) tunes a network
toward critical-like avalanche statistics. The rule, read directly from the paper:

```
W_ij[t+1] = W_ij[t] + 1/τ − u·W_ij[t]·X_j[t]
```

- **W_ij** — a LOCAL edge capacity (not a global statistic).
- **+1/τ** — constant linear RECOVERY every tick, regardless of activity.
- **−u·W_ij·X_j** — multiplicative DEPRESSION only when the source (`X_j`) actually fired.

This is the classic "leaky/token bucket with use-triggered depression" shape. What makes it a genuine
*operational* SOC mechanism (not philosophy): the self-limiting behavior — an edge that just fired is
temporarily less able to fire again, cascades naturally decay rather than self-sustaining — **emerges
from a purely local, decentralized rule.** No node needs to observe the branching ratio, no controller
needs a target, and (this is the load-bearing distinction from the refuted `soc-homeostatic-setpoint`)
**it never claims m̂≈1 is the right target** — it only damps concentration/repetition, which is useful
regardless of where the "true" optimum sits. This sidesteps the edge-optimality critique entirely by
not depending on its premise.

Second source (same 2025 currency, corroborating the *effect* independent of any brain claim):
Sornette lineage dragon-king literature the mesh already cites — hub-driven cascades concentrate on
whichever node fired most recently/most often. A decay-on-use local capacity is the direct structural
antidote to exactly that concentration, without needing a global hub-detector to fire first.

## Why we do not already embody it — the exact gap

`scripts/mesh-mind-control` (2431 lines) is the mesh's dispatch/allocation engine. It has:

- `redispatch-concentration` — an **alarm** (`--dispatch` third-order gate, mesh-criticality.sh:833,
  1136): detects when redispatch is concentrated on one sender/hub and routes to trace/board.
- `_auth_dead_alert_once` / `owner_hold_announce` — **per-window cooldowns**, but only for *alert
  deduplication* (never re-post the same board line within a window), not for *dispatch eligibility*.
- `_pick_agentic` — the worker picker for `--dispatch`/`--allocate`: chooses among AVAILABLE windows
  by engine/state, with no notion of "this window was just dispatched to, so its effective pick-weight
  is temporarily lower."

**The gap:** dispatch selection has an *observer* (the redispatch-concentration alarm) but no
*decentralized actuator*. A window that just took a task is, structurally, exactly as eligible for the
next pick as one that has been idle for hours — nothing locally throttles repeat-selection of the same
hot window between the moment it fires and the moment the global alarm (if it ever crosses threshold)
posts. The synaptic-depression rule is a way to make that throttling a **property of the window itself**
(cheap, local, no m̂ computation) rather than a **global watchdog reacting after concentration already
happened**.

## Proposed application — `scripts/mesh-mind-control` (`_pick_agentic`)

Give each roster window a small persisted **capacity** `C_w` (default 1.0, file `~/.mesh/.dispatch-cap/<w>`,
same idiom as the existing `DEBOUNCE_DIR`/`.reflex-health-state` per-key state files elsewhere in the
genome):

- **Recovery** (every `_pick_agentic` call, before picking): `C_w = min(1.0, C_w + elapsed_s/τ)` —
  linear recharge toward full eligibility, `τ` on the order of the dispatch cadence (minutes, not
  m̂'s multi-hour drift window).
- **Depression** (only on the window actually being picked, `X_w=1` for that tick): `C_w = C_w · (1 −
  u)`, `u` a small fraction (e.g. 0.5) — a just-dispatched window's *effective* pick-weight drops, so a
  second candidate at similar merit is chosen over it, WITHOUT excluding it outright (still eligible if
  it is the only option — this must never become a false-BLOCKED that starves a 1-window roster).
- **Compose:** `_pick_agentic` already ranks candidates by engine/state fitness; multiply that score by
  `C_w` as a tie-breaking soft preference, never a hard gate — a genuinely best-fit window can still
  win even at low `C_w`. This is the same "advisory sidecar before it's trusted in the hot loop"
  discipline the criticality tools already use (`--crit-gap` was proposed advisory-first for the same
  reason).

**Distinct from the refuted setpoint proposal:** this never reads `mesh-criticality --json`, never
targets m̂≈1, and degrades to a no-op (`C_w` always ≈1, i.e. current behavior) for any roster where no
window is picked twice in quick succession — it only engages exactly where redispatch-concentration
would otherwise be building.

**Gate (RED-first, if landed):** a fixture with 2 equally-fit candidate windows; pick A, assert A's
depressed `C_w` makes B win the next pick before A recovers; advance simulated time past `τ` and assert
A becomes preferred again. Break the depression term, watch the fixture fail to alternate, restore.

## Discarded alternative considered

*Allometric scaling of brain activity explained by avalanche criticality*, arXiv:2512.10834 (Dec 2025)
— relates system SIZE to avalanche statistics (scale-dependent m̂ expectations). Discarded in one line:
it is a **descriptive/measurement** correction (what m̂ "should" look like at a given node-count), not
an *operational mechanism* — it would extend `mesh-criticality`'s measurement stack, not act on
anything, and the task asked specifically for an operational angle.

## Honest scope

- **Proposed, not landed.** `mesh-mind-control` is the mesh's core dispatch engine (2431 lines,
  `--dispatch`/`--allocate` reachable only after `mesh-pace`'s spend gate) — a wrong edit to
  `_pick_agentic` risks starving dispatch mesh-wide. The mechanism, the exact gap, the file/function,
  the state-file idiom, the recovery/depression formulas, the compose rule (soft tie-break not hard
  gate), and the RED-first gate shape are specified above for a scoped implementation pass.
- The 2025 source paper is neuroscience (dynamical synapses); the transfer here is the **rule shape**
  (local linear-recover / multiplicative-depress-on-use), not a biological claim about the mesh.

## Sources

- https://pmc.ncbi.nlm.nih.gov/articles/PMC12213684/ — *Network structure influences self-organized
  criticality in neural networks with dynamical synapses*, Front. Syst. Neurosci. (2025)
- https://arxiv.org/pdf/2512.10834 — *Allometric scaling of brain activity explained by avalanche
  criticality* (Dec 2025) — discarded, descriptive not operational
- `docs/reviews/soc-homeostatic-setpoint-2026-07-24.md` — the refuted centralized-setpoint sibling
  proposal, and why this one is structurally different
