# LIVE REVIEW — predictive processing / Bayesian brain: uncertainty over the sensor model

Date: 2026-09-10  
Area: predictive processing & the Bayesian brain  
Transfer: distributed sensor mesh  
Status: literature finding + one proposed application; no implementation landed

## Finding

The new seam is **Bayesian predictive coding (BPC) over parameters**. Standard predictive-coding
implementations usually keep point estimates of hidden states and maximum-likelihood parameters.
Tschantz et al. extend the model so that the *weights and noise parameters themselves have posterior
distributions*. Hidden-state updates remain precision-weighted prediction errors, but the system also
represents epistemic uncertainty: uncertainty about the learned sensor/world model, not merely random
noise in the current reading. The paper reports closed-form local/Hebbian updates and uncertainty
quantification for both epistemic and aleatoric uncertainty.

That distinction is not currently embodied in the mesh. The existing predictive-processing shelf and
`scripts/mesh-precision` cover surprise, volatility, likelihood precision, Bayesian model comparison,
conformal calibration, and epistemic value of reachable observation noise. `scripts/mesh-presence-fuse`
does have honest missingness and a time-skew/consistent-cut gate, but its zone decision still compares
the two current RSSI readings against a point-like `Closest` rule. I found no posterior over the
RSSI-to-zone mapping or over a vantage's reliability parameters in that reflex. This is therefore a
distinct candidate rather than a relabeling of an existing precision score.

## One concrete application

**File:** `scripts/mesh-presence-fuse`  
**Organ:** BLE two-vantage presence/proximity sense; reflex output is the tracked-device zone-change
edge.

Add a persistent, per-device/per-vantage posterior for the localization mapping, for example
`p(zone | self_rssi, peer_rssi, device_class, time-of-day)` with posterior parameters for each
vantage's RSSI offset and spread. On every *paired, non-skewed* scan, update that posterior locally
from the observed RSSI pair; emit the existing zone edge only when posterior mass for the new zone
crosses a calibrated threshold. Publish the two components separately:

* **aleatoric:** current scan noise / RSSI spread, which should widen the zone distribution but need
  not cause learning;
* **epistemic:** broad posterior over the mapping or a newly seen device/context, which should render
  `UNKNOWN` and request a deliberate calibration walk rather than fabricate `MOVED`.

This preserves the current MAXWAIT rule (never learn from a skewed cut) while adding the missing
question: “does this mesh know the localization model here?” A useful first artifact would be a
replay-only posterior and calibration report, not a live behavior change; compare false `MOVED` edges,
`UNKNOWN` rate, and calibration error against today's point comparison on the existing fusion log.

## Sources actually read (live web review)

1. Alexander Tschantz, Magnus Koudahl, Hampus Linander, Lancelot Da Costa, Conor Heins, Jeff Beck &
   Christopher Buckley, **“Bayesian Predictive Coding,”** arXiv:2503.24016 (31 Mar 2025), abstract and
   introduction/methods. The paper explicitly contrasts MAP/ML predictive coding with a posterior over
   parameters and states that the local updates preserve precision-weighted prediction errors while
   quantifying epistemic and aleatoric uncertainty: [arXiv full text](https://arxiv.org/abs/2503.24016).

2. Moumita Das, Dipanjan Ray & Sourabh Bhattacharya, **“Recursive Gaussian Processes and the Bayesian
   Brain,”** arXiv:2608.00503 (1 Aug 2026), abstract. This is a current independent implementation
   direction: hierarchical Bayesian inference, uncertainty propagation, and precision-weighted errors
   are carried together in a recursive process: [arXiv full text](https://arxiv.org/abs/2608.00503).

3. Shohei Furutachi & Sonja B. Hofer, **“Rethinking Predictive Processing,”** *Annual Review of
   Neuroscience* 49 (2026), 471–494; first published 16 Apr 2026. The review cautions that similarly
   shaped sensory prediction-error signals can reflect different underlying computations, supporting
   the decision to expose the uncertainty kind rather than collapse it into one surprise scalar:
   [Annual Reviews article](https://doi.org/10.1146/annurev-neuro-102124-031410).

## Decision

**Land this as a candidate application, not code, in this turn.** BPC is the one concept found that
adds a missing state variable to this organ: uncertainty about the learned generative mapping itself.
The next implementation task, if accepted, is a replay-only posterior/calibration report for
`mesh-presence-fuse`; do not alter the live zone reflex until the report earns a threshold.
