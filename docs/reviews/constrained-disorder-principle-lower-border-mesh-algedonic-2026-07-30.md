# Constrained Disorder Principle — the LOWER variability border (mesh-algedonic)

**Live-review task** (homeostasis / allostasis / ultrastability, cross-domain transfer to a distributed
sensor mesh), 2026-07-30. Landed a concept the mesh did **not** embody.

## The concept (cited, current)

**The Constrained Disorder Principle (CDP).** Ofek Adar, Josef Daniel Shakargy & Yaron Ilan,
*"The Constrained Disorder Principle: Beyond Biological Allostasis"*, **Biology 14(4):339 (2025)**,
doi **10.3390/biology14040339** (MDPI, March 2025). Companion: Ilan, *"The constrained disorder principle
emphasizes the importance of variability boundaries for systems to function effectively"*, J. Med. Life 18
(2025).

CDP states that **every healthy natural system is characterized by noise CONSTRAINED WITHIN dynamic
borders** — their `B = F` formula, *borders define functionality*. Variability is not a nuisance to be
minimized around a setpoint (homeostasis) nor only a target that shifts predictively (allostasis); a
**bounded degree of disorder is itself the signature of health**, and both **too much AND too little**
variability is pathology. The clinical archetype is **heart-rate-variability collapse**: a heart whose HRV
flatlines predicts mortality while its *mean* rate still looks fine — the mean is preserved, the
constrained disorder is gone.

## Why it is new to us (checked against the coverage map)

`homeostasis-review-coverage` already lists the **UPPER** variability border: critical slowing down
(`viability_csd()` in `mesh-algedonic`; `mesh-therm-watch --csd`) reads **variance RISING** toward a
tipping point (Scheffer), and "Love the Noise" (arXiv:2508.12791) variability-is-info is embodied there.
But `viability_csd()` explicitly treats a **dead-flat series as benign** (`CSD_FLAT` = calm). CDP is the
**complementary LOWER border** — a *collapse* of variability toward a constant is pathology — and nothing in
the mesh read it.

The mesh keeps re-discovering this failure by hand and only ever at build time:

- a silent fallback pins an axis to a plausible **constant** — CLAUDE.md's `beat 500` grinder ran flat for
  **weeks**; `mesh-mag -n 1` raced its driver and sat **5 days stale** — and the per-tool `--test` stayed
  **GREEN** the whole time, because a green test proves the read *path* works **once**, not that today's
  artifact still carries constrained disorder.
- `joint_dysregulation()` already **drops** such a frozen axis (`keep = cov[j][j] >= varfloor`) so its
  covariance stays invertible — but *a filter's discard pile is another sense's signal*
  (`a-filters-discard-pile-is-another-senses-signal`): the axis it silently drops is exactly the CDP
  lower-border violation nobody raised.

CDP names the runtime, cross-axis health signal that the build-time `--test` gates structurally cannot
provide.

## The application (measurement half — READ-ONLY, no actuator)

`scripts/mesh-algedonic` — new sidecar **`constrained_disorder()`** + `--cdp` flag + row fields
`cdp=/cdpax=/cdpsr=/cdpsp=/cdpn=`, mirroring the `joint_dysregulation()`/`--dysreg` pattern exactly.

Over the same `axes=` window (therm/hw/egress/stress/crit ∈ [0,1]), per axis it splits prior vs recent
half and flags **`CDP_FROZEN axis=<name>`** when an axis that **carried real variability** (prior std ≥
`CDP_LIVE`) **collapsed** (recent std ≤ `CDP_COLLAPSE`·prior **and** ≤ absolute floor `CDP_FLOOR`) — a
stuck/hollow input silently biasing the fused pain. Else `CDP_BOUNDED`.

Design guards (against this codebase's own scar tissue):

- **Self-calibrated** — recent std vs the axis's OWN prior std, no hardcoded dispersion
  (`a-constant-outlives-its-reader`).
- **Collapse FROM live variability only** — a permanently-quiet constant-0 axis (healthy) is **never**
  flagged, so it does not re-land the naive "value unchanged = dead" that `mesh-state-touch` exists to
  refute.
- **Honest n/a** — `CDP_INSUFFICIENT` below `2·CDP_MIN_HALF` rows; `CDP_UNKNOWN` on empty/unreachable axes
  (short-log-hollow trap, cf. discarded crypticity/cooscillate estimators).
- **READ-ONLY, advisory** — never escalates; the actuator (reconfiguring a stuck producer) stays HELD, per
  the substrate-actuator rule.

**RED-first `--test`** (§11): a 20-row fixture where axis `a` always moves and axis `b` collapses to a
constant in the recent half → asserts `CDP_FROZEN axis=b` (not `a`, not a constant-0 axis). Proven by
swapping recent/prior in the detector → gate goes **RED** (`CDP_BOUNDED`, axis `-`); restored → green. Live
read on this node: `CDP_BOUNDED` (real axes are constant-quiet, correctly not flagged).

## Env knobs

`MESH_ALGEDONIC_CDP_N` (96) · `_CDP_MIN_HALF` (8) · `_CDP_LIVE` (0.05) · `_CDP_COLLAPSE` (0.20) ·
`_CDP_FLOOR` (0.01).

Uncommitted in the tree (steward lands). Not committed.
