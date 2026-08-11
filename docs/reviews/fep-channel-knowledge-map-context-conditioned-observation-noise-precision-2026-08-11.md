# FEP / active inference — the CHANNEL KNOWLEDGE MAP: an agent's model of *its own sensor's* context-dependent noise

**Date:** 2026-08-11 · **Window:** live literature (2026 arXiv), cross-domain transfer → distributed sensor mesh
**Built:** `scripts/mesh-precision --ckm` (report-only, 8 `--test` legs, 9 mutants seen red)
**Adjacent coverage:** `~/.claude/.../memory/fep-active-inference-coverage.md`

---

## 1. The source

**Guangjin Pan, Zhuojun Tian, Mehdi Bennis, Henk Wymeersch — "Active Inference-Enabled Agentic
Closed-Loop ISAC with Long-Horizon Planning", arXiv:2604.19599, submitted 21 Apr 2026.**

An active-inference agent for closed-loop integrated sensing and communication. Abstract, verbatim:

> "we propose an active inference (AIF)-driven wireless agentic system for closed-loop ISAC, which
> jointly optimizes control and sensing resource allocation via backward–forward message passing on a
> factor graph. The AIF agent maintains a generative model as a digital twin by integrating a
> localization model for uncertainty-aware state inference and a localization channel knowledge map
> (CKM) for approximating observation quality during planning."

The mechanism I am importing is the **CKM**, §II-B.2, verbatim:

> "a localization channel knowledge map (CKM) … predicts the expected observation covariance from
> position and sensing resource: Σ̂^ckm(l_x, l_y, k) = F^ckm_φ(l_x, l_y, k)"
> "Since the planning stage needs to anticipate the localization accuracy … F^ckm_φ is trained on the
> outputs of F^loc_θ to capture its position- and subcarrier-dependent performance characteristics."

And what it is *for*, §IV, verbatim:

> "In Zone 1, where the predicted observation variance is high, AIF allocates more subcarriers to reduce
> localization uncertainty. In Zone 2, where the variance is low, AIF reduces the sensing resources."

Reached via a live search of 2026 FEP/active-inference publications; the neighbours read and set aside
are listed in §7.

## 2. The concept, stripped of the radio

The agent's generative model contains **two** models, not one: a model of the *world*, and a **model of
its own sensor** — a map from observable context to the *expected noise of the next reading*. The second
one is consulted **before** the measurement is spent, and it is **learned from the estimator's own output
history**, not declared.

That is the un-embodied half. Every precision number in the mesh is **unconditional and retrospective**:

| embodied | asks |
|---|---|
| `mesh-precision --num` | how noisy has this sense been, **pooled**, over a window |
| `mesh-precision --bme` | does the tape split into two regimes **in time** (a split by index, over MEANS) |
| `mesh-precision --conformal` | how wide a band covers 1−α of residuals, **pooled** |
| honest-fusion (`mesh-situation`, `mesh-sensorium`, `mesh-home-state`) | is the sense fresh/reachable — **binary** |

None of them can ask the CKM's question: **does an observable context predict how noisy the next reading
will be?** A consumer that thresholds or compares a raw sensor value against one fixed cut is *implicitly
asserting that no such map exists*. Until now that assertion was never measured — it was the shape of the
code, not a finding.

Distinct from the two nearest things already in the genome, and it must stay distinct:

- **`--bme` (Bayesian model expansion, landed 2026-08-04)** splits the tape by **index** and compares
  **means**. `--ckm` conditions the **variance** on an **exogenous label**. A tape can be one regime in
  time and still be strongly context-conditioned (measured below: it is).
- **`mesh-precision`'s `frame_coverage` caveat** names the *un-listed* variable (large-world blindness).
  `--ckm` is about a *listed* variable whose reliability is not constant.

## 3. What was built — `mesh-precision --ckm` (report-only)

```
mesh-precision --ckm <file|-> [--value N] [--context M] [--min-bucket K] [--reps R] [--seed S] [--alpha A]
```

Two-column tape (a value field and a context-label field). Verdicts:
`CKM_PREDICTIVE` · `CKM_FLAT` · `CKM_THIN` (<2 populated contexts — a refusal, not a FLAT reading) ·
`CKM_DEGENERATE` (a zero-variance bucket ⇒ infinite likelihood ratio, refused rather than fabricated) ·
`UNKNOWN` (unreadable tape). It weights nothing and gates nothing.

**Estimator — group means are FREE IN BOTH MODELS**, so only the variance structure is on trial:

```
LR = Σ_b n_b · ln( s²_pool / s²_b ),      s²_pool = Σ n_b s²_b / N     (MLE within-group variances)
```

This is Bartlett's statistic without its normal-theory correction, and it is deliberately **not** read
against a χ² table — Bartlett's χ² is famously non-robust to non-normality, and RSSI/RTT/PSI tapes are not
Gaussian. The reference distribution is generated instead.

### 3.1 The null is a CIRCULAR SHIFT, and that is the whole finding

Both a shuffle and a circular shift of the context labels break the value↔context association while
preserving every bucket size exactly. But sensor tapes are **autocorrelated** and context labels are often
temporally **blocky** (hour-of-day, congestion, occupancy). A shuffle scatters a block's serially-correlated
values across all buckets → the null narrows → the test manufactures a map.

Measured, three independent AR(1) tapes (φ=0.95) with **no relation whatsoever** to a blocky label
(alternating 20-sample blocks), `--reps 200`:

| fixture | true relation | shuffle-null p | **shift-null p** | verdict |
|---|---|---|---|---|
| ar_blocky (seed 11) | none | **0.0149** ✗ | 0.1443 | CKM_FLAT |
| ar_blocky2 (seed 12) | none | **0.0050** ✗ | 0.0896 | CKM_FLAT |
| ar_blocky3 (seed 13) | none | **0.0050** ✗ | 0.3184 | CKM_FLAT |
| recurrent_true (seed 21) | σ 1 vs 3 | 0.0050 | 0.0398 ✓ | CKM_PREDICTIVE |

**Three false positives out of three** under the naive null; the shift null holds. Same family as
`mesh-promises --empowerment`'s circular-shift null and [[cooscillate-parametric-p-ignores-autocorrelation]].
`--ckm` reports **both** p-values on every emission so the gap is visible rather than asserted, and takes
the verdict from the shift.

The price is stated, not hidden: on a **blocky** context the shift null is very conservative (row 4 clears
by a hair at a 3× σ separation). It will under-call, never over-call. Which leads to the sharper rule in §5.

### 3.2 Gates

`--test` leg (7) adds eight assertions, each another's red:
(a) σ 1-vs-4 → PREDICTIVE · (b) equal σ → FLAT · (c) **pure mean shift 0-vs-10 at equal σ → FLAT** (the
free-means property; without it "reads differently there" masquerades as "noisier there") · (d) the AR(1)
trap, asserting **both** halves — shift FLAT **and** shuffle p≤0.05 — so moving the verdict back onto the
shuffle null goes red instead of passing quietly · (e) 1 bucket → THIN **and carries no statistic** ·
(f) zero-variance bucket → DEGENERATE · (g) absent tape → UNKNOWN · (h) seeded determinism.

Nine mutants run from a scratch copy, each seen RED on the intended leg: verdict from the shuffle null
(→d) · means pinned to the global mean (→f) · means pinned to 0 (→c) · degenerate guard removed (→f) ·
thin guard weakened to 1 bucket (→e) · unseeded RNG (→h) · verdict hard-wired FLAT (→a) · hard-wired
PREDICTIVE (→b,c,d) · readable-check bypassed (→g). Whole `--test` runs in **1.7 s**.

One trap defused on the first live run and left as a comment in the source: the tape is handed to python
as a **path**, never as an env string — `presence.log` yields ~14k device-readings and the env-string form
died with `Argument list too long`, which reads as a broken tool rather than a big input.

## 4. Live readings

### 4.1 Context = TIME (congestion bucket, 4-hour bucket) → FLAT everywhere

`~/.mesh/presence.log`, 2168 scans, 2026-07-15 → 2026-08-11.

| tape | context | n | σ range | shuffle p | **shift p** | verdict |
|---|---|---|---|---|---|---|
| Bose Revolve RSSI | scan congestion (n devices) | 2128 | 7.88 – 13.70 dB (1.74×) | 0.0050 | 0.2239 | CKM_FLAT |
| Bose Revolve RSSI | hour-of-day /4 | 2134 | 9.39 – 11.60 dB | 0.0050 | 0.6517 | CKM_FLAT |
| Samsung TV RSSI | scan congestion | 1611 | 3.13 – 3.76 dB | 0.0995 | 0.2935 | CKM_FLAT |
| Samsung TV RSSI | hour-of-day /4 | 1614 | 3.39 – 3.72 dB | 0.6667 | 0.9254 | CKM_FLAT |
| egress RTT (`egress-health.log`, loss=0 rows) | hour-of-day /4 | 1725 | 36.99 – 53.74 ms (1.45×) | 0.0050 | 0.0995 | CKM_FLAT |

The Bose σ spread of 7.9→13.7 dB *looks* like a congestion map and is not one: it does not survive a null
that preserves the tape's own serial structure. **Three live tapes that the naive test would have called
PREDICTIVE.** On a time-blocky context, "the noise depends on context" and "the sense is non-stationary"
are the same hypothesis — and that is `--bme`'s question, not this one.

### 4.2 Context = DEVICE (interleaved, non-temporal) → PREDICTIVE, decisively

Same tape, one row per (scan × device), value = RSSI, context = MAC, `--min-bucket 30`:

```
CKM_PREDICTIVE — n=7021 of 13743 rows, 8 context buckets: LR=2853.13
  p_shift=0.0050 (floor at reps=200) · p_shuffle=0.0050 · null p95 shift=83.4 vs shuffle=24.4 (3.42× wider)
  σ 2.622 .. 10.890 dB (ratio 4.15×)
  28:11:A5:B8:9E:A2 (Bose Revolve) n=2134 σ=10.89   EC:C1:AB:D1:A7:EF (DV8235) n=937 σ=7.22
  19:47:44:E6:34:E9 n=69  σ=6.05    E7:4D:F9:65:B0:65 n=2088 σ=4.50
  5C:49:7D:92:1E:58 (Samsung TV) n=1614 σ=3.65      F0:A3:B2:DF:EB:83 n=32 σ=3.37
  48:E7:DA:C6:6F:26 n=53 σ=2.79     84:C8:A0:16:04:8A n=94 σ=2.62
```

LR is **34× the shift null's p95**. The map is real and it is over **device**, not over time — precisely
the paper's shape (its CKM indexes *position and sensing resource*, not the clock).

## 5. The rule this earns

**A context that is temporally blocky is confounded with the sense's own non-stationarity by construction;
a context that interleaves within the tape is testable.** Both live families above came from the *same
log, the same sense, the same window* — one direction is untestable and one is decisive. When looking for
a noise map, index it by something that recurs *within* the tape (device, node, band, channel, posture),
not by something that drifts *along* it (hour, congestion, load). If the only available context is blocky,
the honest answer is `--bme`'s: ask whether the tape has regimes, not whether the label predicts them.

## 6. The concrete application (named files) — and what is deferred

**Target: `scripts/mesh-presence-fuse`, `closest_node()` (:455-461).**

```bash
if [ "$lr" -ge "$pr" ]; then echo "$SELF"; else echo "$PEER_NAME"; fi
```

Two nodes' RSSI for the same MAC, compared with a **zero margin**. A 1 dB difference flips the room
attribution — on a sense whose per-device observation σ is **2.6 to 10.9 dB**. The device with a σ of
10.9 dB is the *personal* class device the attribution actually cares about; the 2.6 dB one is a fixture
that never moves. The margin needed for the Bose is ~4× the margin needed for the TV, and the code uses
the same margin for both: **zero**.

Second consumer, same root: **`scripts/mesh-proximity`, `rssi_to_distance()` (:53-63)** maps RSSI to a
distance with one fixed 10-dB-per-bucket ladder for every device. At σ=2.6 dB that is a ±1-bucket error;
at σ=10.9 dB it is ±4 buckets — the ladder is calibrated for the quietest device in the house and reports
the same confidence for the noisiest.

**Proposed (deferred as code, on purpose):** a per-device σ read from `--ckm`'s map, applied as a required
margin in `closest_node()` (`|lr − pr| < κ·σ_dev` → return `AMBIGUOUS` rather than a side). Deferred
because it **changes a live verdict** — `mesh-presence-fuse` feeds room attribution, and a new
`AMBIGUOUS` branch has downstream readers that must be swept first ([[a-format-fix-must-sweep-every-reader]]);
and because κ is exactly the constant the report exists to pick, not to guess. The report-only
measurement lands first, per the standing discipline
([[crypticity-vs-excess-entropy-hollow-on-short-logs]]). The instrument is what shipped today.

## 7. Caveats, stated where they live

- **Predictive, not causal.** The map says *where* the sense is noisy, never *why*; a context that merely
  co-varies with the true cause predicts just as well ([[a-shared-observable-cannot-name-the-mechanism]]).
  The paper's CKM is also purely predictive — it is trained on the estimator's outputs.
- **The device map is confounded with floor censoring.** A device sitting near the scanner's −90 dBm
  sensitivity floor has its low tail truncated, which *reduces* its measured σ. Part of the 4.15× spread
  is plausibly that, not radio geometry. The consequence in §6 does not depend on the mechanism: whatever
  produces it, a single margin is wrong for both ends of a 4× spread.
- **State variance vs observation variance are not separable here.** The Bose moves; the TV does not. A
  proper CKM is trained against a *localization estimator's* residuals, where the state model absorbs
  motion. The mesh has no such model, so `--ckm` measures total dispersion and says so in every emission.
- **Significance ≠ magnitude** — the standing caveat from the 08-03/08-04 builds. p_shift hits its
  `1/(reps+1)` floor at 0.0050; that is a resolution limit, not an effect size.
- `presence.log` is not a fixed corpus; every n above is today's answer ([[records-log-is-a-sliding-window]]).

## 8. Searched and set aside (do not re-serve)

- **arXiv:2606.04935**, Nuijten/Lukashchuk/van de Laar/de Vries, *What Type of Inference is Active
  Inference?* (3 Jun 2026, rev 7 Jul): EFE minimization rewritten as VFE on a model augmented with
  epistemic priors, decomposed into entropy corrections + a planning correction. **Adjacent to the
  entropy-regularizer finding already landed 2026-08-03** (Kenny arXiv:2511.20321) and, like it, has no
  continuous action score in the mesh to regularize. No new organ.
- **arXiv:2603.20927**, de Vries, *Active Inference for Physical AI Agents — An Engineering Perspective*
  (21 Mar 2026): reactive message passing on factor graphs, graceful degradation under fluctuating power,
  online structural adaptation. A position paper — its "coupled AIF agents are themselves AIF agents"
  scaling claim is the mesh's own shape already; no measurable mechanism to import.
- **arXiv:2606.20658**, *Expected Free Energy-based Planning as Variational Inference* (9 Jun 2026):
  same EFE-as-VI seam as 2606.04935.
- **arXiv:2503.18161**, dual-layer AIF for building/community energy: distributed AIF in engineering, but
  the mechanism is a two-level generative model over energy demand — no mesh organ it fits.

**Sources:**
- [arXiv:2604.19599 — Active Inference-Enabled Agentic Closed-Loop ISAC with Long-Horizon Planning](https://arxiv.org/abs/2604.19599)
- [arXiv:2606.04935 — What Type of Inference is Active Inference?](https://arxiv.org/abs/2606.04935)
- [arXiv:2603.20927 — Active Inference for Physical AI Agents: An Engineering Perspective](https://arxiv.org/abs/2603.20927)
- [arXiv:2606.20658 — Expected Free Energy-based Planning as Variational Inference](https://arxiv.org/abs/2606.20658)
- [arXiv:2503.18161 — Active Inference for Energy Control and Planning in Smart Buildings and Communities](https://arxiv.org/abs/2503.18161)
