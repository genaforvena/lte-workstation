# The link sense was reading its own hand and calling it weather

**Date:** 2026-08-25
**Lane:** LITERATURE (live review)
**Area:** free energy principle & active inference (Friston), angle = CROSS-DOMAIN transfer into a
distributed sensor mesh
**Arm:** treated (assigned)
**Assigned organ:** `scripts/mesh-link-flap` — drawn uniformly by coin at p=0.20 from the 568
never-reviewed tools in the lane's own denominator. Not retargeted.
**Verdict:** APPLIES. Landed on the assigned organ (uncommitted; steward lands from the tree).

---

## 1. The concept, and where I found it

**Kilteni, Cullen, Schneider & Schwarz, "Suppressing Sensation during Action across Species and
Sensory Modalities: Predictive and Nonpredictive Mechanisms of Sensory Modulation", *Journal of
Neuroscience* 45(46) e1351252025, published 12 November 2025** —
<https://www.jneurosci.org/content/45/46/e1351252025> (full text 403s to a fetch; the claims cited
here are the ones the abstract and the journal's own listing state, not inferred detail).

The review's spine is a **separation**, and the separation is the content:

- **reafference attenuation** — *predictive*, model-based, stimulus-specific: a forward model
  cancels the particular consequence **this** action was expected to produce.
- **sensory gating** — "a broader and often less selective mechanism that inhibits **both self- and
  externally generated inputs**".

The two are dissociable and are measured apart (they separate in primary somatosensory cortex, with
suppression differing by whether stimulus timing aligns with self-generated movement). Gating buys
quiet by going *partly blind*; attenuation buys quiet by being *right about itself*.

Two further live sources were read in the same sweep and are **not** what landed, recorded so the
sweep is auditable: Mathys, Legrand, Waade, Mikus & Weber, "Robust volatility updates for
Hierarchical Gaussian Filtering", [arXiv:2605.00966](https://arxiv.org/abs/2605.00966) (1 May 2026 —
the textbook volatility-coupled update can yield *negative posterior precision*, fixed by
interpolating a second quadratic expansion found via Lambert W), and "Closed-form predictive coding
via hierarchical Gaussian filters", [arXiv:2605.20293](https://arxiv.org/pdf/2605.20293). Both were
**discarded for this organ**: `mesh-precision`'s `stovol` axis already carries the
volatility/stochasticity decomposition (review 2026-08-18) and `mesh-novelty` already scales its
surprise bar by an HGF volatility term — landing there would have been a fifth pass over ground the
mesh holds.

## 2. What was already ours

58 prior reviews in this area. Checked before searching:

| embodied | where |
|---|---|
| corollary discharge / reafference-exafference split | `mesh-audio-active` (**audio only**), 2026-07-30 + 2026-08-14 |
| the CD is a *timed* prediction, retimed at one hub | `mesh-audio-active --cd`, 2026-08-14 |
| volatility vs stochasticity decomposition | `mesh-precision --stovol`, 2026-08-18 |
| volatility scaling a surprise bar (one-sided HGF use) | `mesh-novelty`, 2026-08-18 |
| Shannon surprisal over a categorical baseline | `mesh-novelty` |
| precision = inverse variance, as a measurement | `mesh-precision`, 2026-06-20 |

`reafference` returns **zero** hits in the link/network organs. The mesh had a corollary discharge
in exactly one sensory modality and none in the one where it owns an actuator that fires every
minute. And the **predictive-vs-nonpredictive distinction itself** — the thing that says *which*
kind of suppression you are implementing — appears nowhere.

## 3. The gap, measured

`mesh-link-flap` reads `/sys/class/net/<if>/carrier_changes` and calls a positive delta FLAPPING.
`mesh-link-heal` (`* * * * *`) repairs a wedged station by climbing a ladder: `wpa_cli reassociate`
→ `ip link down/up` → driver reload → USB re-enumerate. **Every rung moves the counter the sense
reads.**

Measured, not argued:

- **one `ip link down/up` = +2 `carrier_changes`** — a real kernel, in a private netns so the sole
  uplink was never touched: `sudo -n unshare -n -m`, `mount -t sysfs sys /sys`, veth pair,
  `carrier_changes` 2 → 4 across one admin down/up.
- **a freshly created netdev reads `carrier_changes=1`** (same run) — so a driver reload or a
  re-enumeration *restarts* the counter, indistinguishable from a reboot by the counter alone.
- since 2026-08-16 the healer took **14 bounces, 10 driver reloads, 3 re-enumerations**, and every
  one landed in this tool's fault count with nothing to tell it from the world.

### The forward model, calibrated against the actuator's own tape — with a control arm

`link-heal`'s `RECOVERED` rows carry `carrier_drops=N` (the kernel's `carrier_down_count` delta over
the episode; 1 drop = 2 `carrier_changes`), grouped by the rung the episode reached:

| rung | n | measured | mean drops | → carrier_changes | charged |
|---|---|---|---|---|---|
| **none (observed, did not act)** | 256 | 169 | **0.00** | 0.0 | — **the control arm** |
| reassociate | 44 | 28 | 0.75 | 1.5 | 1.5 |
| bounce | 4 | 3 | 2.00 | 4.0 | **2.0** |
| reload / usb | 10 / 3 | 0 | na | RESET | RESET |

**The control arm is the whole argument.** `none` is an episode the healer *watched* and did not
act in — a spontaneous deauth that recovered by itself — and across 169 of them the carrier counter
moved **zero** times. Without that arm the table is a correlation between severity and rung; with
it, the drops in the acting arms are our hand.

**Which way to be wrong.** The bounce arm is n=3 and its two independent estimates disagree — 4.0
from the tape, 3.5 from composing the netns-exact +2 with the n=28 reassociate arm. With n=3 there
is no basis to pick, so it is charged the **smallest defensible** value, 2.0, the part that is
exactly measured. The direction is not symmetric: over-charging our own hand *hides real flaps* (a
fault sense going silent), under-charging leaks a little of our hand into the world channel (a false
alarm, which is loud and gets looked at).

### And the size of it, stated so nobody mistakes it for the big fish

Since this boot the counter took **54 down-edges**; the healer's 27 episodes account for **3**.
**94% of this link's carrier activity happens where the healer never opened an episode** — the world
really does flap here, hard. Reafference is a real but ~6% contamination. The **reset/window bug it
sat next to was rendering the whole thing STABLE**, which is the larger defect and the same failure
wearing a second face: a *self-caused* counter discontinuity routed into the world channel's *quiet*
bucket.

The live artifact that provoked the review, printed by the deployed tool at 17:58Z:

```
[link-flap] STABLE  +0 flaps / 3497488s (0.00/min) · total=108
```

A **40.5-day** window (most of which this power-cycling node was OFF), on a link that had taken 108
carrier changes in the 7.9 h since boot — 13.7/h, the worst-flapping link in the mesh — rendered
**STABLE, 0.00/min**, because the prior counter (148, from a July netdev) was larger than the
current one and the code clamped the negative delta to zero.

## 4. What landed in `scripts/mesh-link-flap`

1. **Reafference subtraction, per rung, from the actuator's own ledger** (`~/.mesh/link-heal.log` —
   an artifact the mesh already produces; no re-probing). The reading now publishes
   `flaps_self` / `flaps_world` / `attribution` and the verdict keys on the **world residual**.
2. **We refuse gating, and the refusal is an executable assertion.** No blanket suppression during a
   heal window — that would blind the sense exactly when the link is most likely to be genuinely
   flapping. A larger delta inside a heal window still reads FLAPPING with the world's share intact.
3. **The unit of analysis is the EPISODE, not the action.** The ladder climbs *through* its lower
   rungs, so a bounce episode's measured cost already contains the reassociate that preceded it.
   Summing per action double-charges: the live 16:45–16:49Z episode logged reassociate *then* bounce
   and moved the counter by 2, while a per-action sum predicts 3.5. Actions are grouped into
   episodes and each is charged once at its highest rung.
4. **An over-prediction is never floored into a clean zero.** If we charge our own hand for
   transitions that did not happen, the forward model is wrong and the reading says
   `attribution: unknown` + `overpredicted: N` — a silently floored residual would render a broken
   prediction as a perfectly quiet link. (This arm fired on live data during development and is how
   the double-count in §4.3 was caught.)
5. **The reset channel.** A backwards counter, a window opening before this boot, or a reset-class
   rung in the window → verdict **RESET**, never STABLE, naming its cause — and the reading still
   publishes an honest `rate_since_start_per_min` off the counter's own start (boot, or the last
   time our own reload re-created the netdev), flagged `rate_floor` when only boot bounds it.
6. **CD-channel honesty.** Healer present but its ledger unreadable, or a window opening before the
   ledger's first line → `self=na`, `attribution=unknown`. No actuator on this node at all →
   an honest `self=0` that says *why* it is zero. Never a faked clean residual.

## 5. The gate, seen RED then green

Assertions are on the JSON, not on a pane. Three defect classes were reverted in a copy and each
was watched to fail:

| red arm | reverted to | observed |
|---|---|---|
| reset channel | the old silent `delta<0 → 0` clamp | `"verdict":"STABLE"` on a backwards counter — **the live bug reproduced** |
| reafference subtraction | `self` forced to 0 | `"verdict":"FLAPPING"` on a window whose only event was our own bounce |
| episode grouping | sum per ACTION | `"flaps_self":"3.5"` and a spurious `overpredicted:1.5` |

Green, all arms, plus the six original ones (selection, BASELINE→FLAPPING→STABLE, classifier,
missing-source exit 2). Live behaviour either side, same real state and real healer log:

```
OLD  [link-flap] FLAPPING  +2 flaps / 5037s (0.02/min) · total=108
NEW  [link-flap] STABLE    +2 flaps / 5083s (0.00/min) · world=0.0 self=2.0 (bouncex1, measured+bounce-floor)
```

— and `link-heal`'s own independent record of that episode agrees: `carrier_drops=1`, caused by the
bounce.

## 6. What this does not settle

- The `reassociate` charge (1.5) rests on 28 measured episodes against a 169-episode zero control;
  the `bounce` charge rests on 3 and is deliberately floored. Both re-derive from the tape with the
  one-liner in the tool's header — they are constants **with** their derivation, not magic numbers.
- `carrier_drops` is measured per *episode*, so transitions outside episodes (94% of them here) are
  outside the calibration entirely. The table says what our actions cost *within* an episode; it
  does not claim the world is quiet.
- The tool remains on-demand (`orphan-ok`) and its window is still whatever the caller's cadence
  makes it. The reset channel now refuses the absurd windows; it does not manufacture a cadence.
