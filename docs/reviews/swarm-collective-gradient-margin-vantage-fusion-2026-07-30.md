# Live-literature review — swarm intelligence / stigmergy → distributed sensor mesh: collective-gradient confidence is the inter-sensor MARGIN, not the argmax (`mesh-presence-fuse`)

Date: 2026-07-30 · lane: genome (idea-queue LITERATURE task) · status: proposal, uncommitted · angle: cross-domain transfer to a distributed sensor mesh

## Area & angle

Swarm intelligence / stigmergy, transferred **cross-domain to the mesh's SENSOR layer** — deliberately
away from the board/coordination layer, where eight prior swarm landings already sit (pheromone-entropy,
no-entry repellent, density-adaptive evaporation, tunable quorum, response-threshold division-of-labour,
circular-mill, sematectonic grounding — all over `~/.mesh/chat.log` as a foraging field). This one lands
on **BLE presence fusion**, a genuinely distributed *sensing* problem, and on the swarm mechanism that is
about *sensing a field* rather than *allocating work*.

**Recent result (2023-2026):**

- **"Collective Gradient Following with Sensory Heterogeneous UAV Swarm,"** Springer LNCS,
  *Swarm Intelligence / ANTS* (2024), doi 10.1007/978-3-031-51497-5_14
  (researchgate.net/publication/377865629). A swarm tracks a scalar-field gradient **even though only
  some members can sense it and others are blind** — sensing ability is *heterogeneous*, and the
  collective estimate stays good because informed members modulate behaviour and the rest follow.
- Builds on **Collective gradient perception with a flying robot swarm** (2022, real nano-drone swarm):
  a swarm follows the gradient of a scalar field **with no member possessing gradient-sensing
  capability**, via *speed modulation* (slow where the field is strong) + *social coupling*.
- Foundation: **Berdahl, Torney, Ioannou, Faria, Couzin, "Emergent Sensing of Complex Environments by
  Mobile Animal Groups," *Science* 340:574–577 (2013)** (science.org/doi/10.1126/science.1225883). The
  group tracks a gradient **no individual measures**; robustness comes from the *spatial density
  gradient* the group forms, not from averaging individual estimates.

**The one idea we don't embody** — from this line: *a collective sensor's confidence must come from the
MARGIN / agreement structure across its heterogeneous members, not from the bare argmax. A near-tie
between two members is AMBIGUITY (co-present, uninformative), not a confident vote.* This is exactly the
distinction between **emergent sensing** (margin/density structure) and the naïve **"many wrongs"**
argmax/average that discards it.

## The mesh has a 2-vantage collective sensor that reads the argmax with zero margin

`scripts/mesh-presence-fuse` is a real distributed sensor: it scans BLE from **two vantages** (this node
+ peer `ds`), overlaps the devices both see, and assigns each device to "which node it's closest to" —
a coarse spatial localization of the operator's phone (the mesh's closest thing to a tracked gradient).
The assignment is a **hard argmax with no dead-band** (verified in-source):

```
scripts/mesh-presence-fuse:455  closest_node() {
scripts/mesh-presence-fuse:460    if [ "$lr" -ge "$pr" ]; then echo "$SELF"; else echo "$PEER_NAME"; fi
```

A device at `self=-70 / peer=-71` is assigned to SELF with the **same confidence** as `self=-50 /
peer=-90`. But BLE RSSI noise is ±5–10 dB — a 1-dB margin is **pure noise**, deep inside the sensor's
own error. The collective has no notion of "this reading is a TIE / on the border / not informative
enough to call a zone." That is precisely the emergent-sensing failure: **the argmax is reported as a
confident direction when the inter-vantage margin says the field is flat here.**

It compounds in the `--track` zone-change detector, which fires on **any** argmax flip:

```
scripts/mesh-presence-fuse:610   elif [ "$prev_closest" != "$closest" ]; then   # zone change → alert
```

A phone sitting on the border between the two vantages flips `SELF→PEER→SELF` on every scan's RSSI
jitter, emitting a stream of spurious `MOVED self→peer` alerts to the mind — the sensor-layer twin of
the board's circular-mill flap, and a live instance of [[both-edges-of-a-signal-need-the-same-gate]]
(a change gated at the midpoint with no hysteresis re-triggers on noise).

This is genuinely absent, not a re-description: `closest_node` has no margin parameter, and the two
prior swarm-quorum landings do not touch it — the **tunable quorum** landing
(`swarm-tunable-quorum-speed-accuracy-2026-07-28.md`) is a *temporal* absent-scan quorum on
`mesh-arrivals`; this is a *spatial* inter-vantage margin on `mesh-presence-fuse`. Orthogonal knob,
different tool, different axis.

## Proposal — a margin dead-band on the collective vantage estimate (`scripts/mesh-presence-fuse`)

Add `MESH_FUSE_MARGIN_DB` (default ~6 dB ≈ 1 RSSI σ) and make the collective estimate margin-aware:

1. **`closest_node` gains an explicit `margin` arg** (default `0`, so every existing caller stays
   byte-identical). When both RSSIs are present and `|lr − pr| < margin`, echo **`BORDER`** — the
   emergent-sensing "the field is flat here, no confident vote" state, distinct from a decisive
   assignment. Callers opt in by passing the margin.
2. **`print_overlap` (the dash-facing report) passes `MESH_FUSE_MARGIN_DB`** → the `Closest` column
   shows `BORDER` for near-ties, plus a `border: N` line in the summary. Report-only, dash-honest.
3. **`--track` adopts the margin WITH hysteresis** (the flap fix): a zone-change fires only when the
   phone crosses the *full* band — `prev=SELF` holds until `pr − lr ≥ margin` (not merely `pr > lr`),
   and vice-versa; inside the band the tracked device is `BORDER`, no MOVED alert. Enter-and-exit the
   band, never the midpoint. This is the load-bearing win: it kills the border-flap alert spam.

Emergent-sensing framing made concrete: the collective's confidence now reflects the inter-vantage
**margin** (Berdahl's density-gradient structure), and a **blind/tied member registers as ambiguity,
not a coin-flip vote** — exactly the sensory-heterogeneity robustness the 2024 UAV result formalizes,
in the mesh's one 2-vantage sensor.

## Implementation order (why this is a proposal, not a shipped edit this turn)

`closest_node`, `print_overlap`, and the `--track` block are all defined **below** the `--test`
dispatch (line 293) — the exact structural hazard the tool already documents for `scan_both` (a
definition below the arg-parse is undefined on the path that needs it; "passing `--test` ≠ running").
So a RED-first gate on the margin **requires first hoisting `closest_node` above the `--test`
dispatch** (as the tool already did for its `classify_peer_fail` / `scan_sampled` helpers at line 159,
"Defined ABOVE the arg-parse so --test can exercise it directly"). I will not ship an untested margin
change into a live presence sense that feeds `mesh-arrivals` and the senses dash — [[non-empty-is-not-correct]]
and "a gate you have not seen FAIL is not a gate". Step 1 is the hoist; step 2 is the margin + the
RED-first `--test`:

```
# RED-first falsifiers (after hoist):
closest_node MAC 6   with l_rssi=-70 p_rssi=-71  →  BORDER   (near-tie is ambiguity, not a winner)
closest_node MAC 6   with l_rssi=-50 p_rssi=-90  →  $SELF    (decisive margin still assigns)
closest_node MAC 0   with l_rssi=-70 p_rssi=-71  →  $SELF    (margin 0 = byte-identical legacy path)
# --track: a -70/-71 flip must NOT emit MOVED; a -70→-50/-90 crossing MUST.
```

Calibrate `MESH_FUSE_MARGIN_DB` against the **live** RSSI spread on the real board, not the assumed
6 dB — same discipline as [[pooled-corpus-rank-saturates-per-organ]] / [[a-constant-outlives-its-reader]];
6 dB is a starting hypothesis (≈1 σ of observed BLE jitter), a claim to be re-derived, not pinned.

## If it does not apply — the honest alternative

It applies: the mesh has a real 2-vantage collective sensor doing argmax with zero margin. The broader
emergent-sensing claim — *a group tracks a gradient no member senses* — is only *partly* transferable
(the mesh's vantages are static, not mobile speed-modulators), so I do **not** propose the full
speed-modulation/social-attraction loop; that half would be a stretch on a non-mobile mesh. The
**strictly transferable, unembodied** kernel is *confidence-from-margin on a heterogeneous collective
estimate*, and `mesh-presence-fuse:460` is where it's missing.

## Sources

- "Collective Gradient Following with Sensory Heterogeneous UAV Swarm," Springer LNCS (2024) —
  https://link.springer.com/chapter/10.1007/978-3-031-51497-5_14 ·
  https://www.researchgate.net/publication/377865629
- "Collective gradient perception with a flying robot swarm" (2022) —
  https://www.researchgate.net/publication/364765199
- Berdahl et al., "Emergent Sensing of Complex Environments by Mobile Animal Groups," *Science* 340
  (2013) — https://www.science.org/doi/10.1126/science.1225883 ; evolution-of-distributed-sensing:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4755780/
- In-source verification: `scripts/mesh-presence-fuse:455–461` (argmax, no margin), `:610` (flip-fires
  zone change).
