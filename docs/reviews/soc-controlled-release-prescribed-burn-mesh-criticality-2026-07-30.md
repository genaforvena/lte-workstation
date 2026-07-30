# SOC controlled-release ("prescribed burn"): the first control-side signal on mesh-criticality

**Date:** 2026-07-30 · **Organ:** `scripts/mesh-criticality` · **Landed:** read-only sidecar
`prescribe_burn()` + `--prescribe` + `Prescribe=` summary field + JSON `prescribe` object · RED-first
`--test`. Uncommitted in tree (steward lands).

## The angle

Live literature review, cross-domain transfer of self-organizing criticality / power-law dynamics to a
distributed mesh. The coverage map (`memory/mesh-criticality-covered-critiques.md`) shows this tool
already carries ~11 stacked SOC reviews — **all of them MEASURE the state** (branching ratio m̂,
avalanche shape/crackling, micro/macro decomposition, dragon-kings, CSD, drift, CECP, bin-width, edge-
optimality, dynamic range, Widom drive-axis, SOB modality). Not one names an **intervention**. So the
un-embodied ground is the *control* side of SOC, not another measurement.

## The concept we did NOT embody

**Controlling self-organized criticality by proactive hub release.**

- **Aguirre, Sarmiento & Papa, "Controlling self-organized criticality in complex networks"**
  (Eur.Phys.J.B; **arXiv:1305.6656**). On a Bak-Tang-Wiesenfeld sandpile over ER / Goh-Kahng-Kim /
  the real Western-US power grid, the size of large avalanches is suppressed by *deliberately triggering
  a small avalanche at the highest-degree node that is NEAR to becoming critical* — its mass then
  dissipates **locally** rather than concentrating into a system-spanning cascade. Verbatim result:
  hub-targeting "works in the sense that the dissipation of mass occurs most locally avoiding larger
  avalanches" and beats a random-node strategy "much" — and the ability "is related to its ability to
  reduce the concentration of mass on the network."
- **Confirmation in current (2025) literature:** *"A Self-Organized Criticality Model of Extreme Events
  and Cascading Disasters of Hub and Spoke Air Traffic Networks"* (**arXiv:2506.16727**, Jun 2025) —
  optimized hub-and-spoke systems **self-organize into fragile configurations** whose few high-throughput
  hubs carry the power-law long-tail systemic risk, and it explicitly calls for "identification of
  critical nodes" + "proactive strategies for disaster risk reduction." That is precisely the
  target-identify-then-release loop.

Where found: WebSearch (SOC cascade-control / hub-fragility, Jul 2026), abstracts fetched from arXiv.

## The concrete application (a real file)

`scripts/mesh-criticality` — a read-only `prescribe_burn(evs, win_h, bin_s, reg, phi)`:

- **Transfer:** the "highest-degree node" ↦ the top **sender/reflex hub** of the board window (reuses
  the same `sender_id()` counting the DK gate already uses). "Near-critical but not yet toppled" ↦ that
  hub is **LOADED** (owns ≥ `CRIT_PRESCRIBE_LOAD`=0.35 of the window) while the board is still **QUIET**
  (Widom silence-fraction φ ≥ `CRIT_PRESCRIBE_QUIET`=0.50 — timescale separation intact, no active
  cascade). That is the cheapest, most-effective release window per the sandpile control result: shed
  *before* the pile reaches the angle of repose.
- **Labels:** `READY` (loaded hub + quiet + non-super → controlled-release candidate, names the target) /
  `CASCADING` (reg==SUPERCRITICAL → the DK/alarm gate owns a live cascade; prescribe defers) / `NONE`
  (no loaded hub, or board not quiet) / `INSUFFICIENT` (< `CRIT_PRESCRIBE_MIN_N`=20 events, or no
  identified senders).
- **Genuinely additive — not the hub-DK alarm re-treaded.** The DK ALARM fires **during** a forming
  cascade (SUPERCRITICAL + identity concentration). `prescribe_burn` fires in the **complementary**
  regime — loaded hub + SEPARATED/quiet + NOT supercritical — so the two are **mutually exclusive by
  construction** (`reg==SUPERCRITICAL ⇒ CASCADING`). The alarm answers "a cascade is happening, on whom";
  prescribe answers "who is loading toward one while it is still cheap to release." Different regimes,
  different questions.
- **Read-only, first control-side signal.** It only **names a target + window**. Never touches
  m̂/regime/alarm. The actuation — `mesh-mind-control` proactively re-routing that hub's queued redispatch
  to idle minds — is the **deliberately UNWIRED next step** (same restraint as every prior sidecar; same
  spirit as the `soc-homeostatic-setpoint` and `soc-decentralized-depression-recovery` proposals that
  spec the actuator but do not wire it into live dispatch).

## Verification (artifacts, not claims)

- `--test`: **GREEN**. RED-first proven — mutating the `CASCADING` branch to `READY` (collapsing the
  regimes) turns the gate **RED** (`smoke-test: FAIL … SUPERCRITICAL must defer … as CASCADING`);
  restoring turns it **GREEN**. Five branches asserted (READY targets the hub / SUPERCRITICAL→CASCADING /
  driven-φ-low→NONE / diffuse-no-hub→NONE / <min-n→INSUFFICIENT) + an explicit constant-label guard.
- Live on this board: `Prescribe=NONE target=genome@mesh-home load=0.15` (φ=0.37, n=206) — an **honest
  negative**: the top sender owns only 15% and the board is mildly driven (φ below the 0.50 quiet
  threshold), so there is no controlled-release window right now. Exactly the shape of the other
  negatives on this tool (SOB=UNIMODAL-SOC, Edge=NEUTRAL) — the sidecar reports the real state, it does
  not manufacture a firing.
- `--json`: `prescribe` object parses (`{"label":"NONE","target":"genome@mesh-home","load":0.146,
  "phi":0.366,"n":206}`).

## Env knobs (self-calibrating, no hardcoded magnitude)

`CRIT_PRESCRIBE_LOAD` (0.35 hub-share floor), `CRIT_PRESCRIBE_QUIET` (0.50 φ floor),
`CRIT_PRESCRIBE_MIN_N` (20). Labels are STRUCTURAL; the "how loaded" magnitude is left to the live
corpus (the constant-outlives-its-reader rule).

## Unwired next step

The actuator: on `Prescribe=READY`, have `mesh-mind-control`'s dispatch picker *proactively* shed the
named hub's queued redispatch to an idle mind — the controlled small release. That is the risky,
dispatch-core edit (2431-line engine); it needs its own review + RED-first gate before wiring, exactly
as the depression-recovery proposal (`soc-decentralized-depression-recovery-dispatch-2026-07-29.md`)
concluded. This landing supplies the read-only **trigger signal** that actuator would consume.
