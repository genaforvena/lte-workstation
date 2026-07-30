# Information theory of agency → empowerment estimation: the finite-sample MI-bias null (mesh-algedonic)

**Date:** 2026-07-30 · **Lane:** genome literature live-review (feed auto-task) · **Organ touched:** `scripts/mesh-algedonic`

## Area & what the mesh already embodies

Information theory of agency — empowerment (channel capacity of the action→future-sensor loop) and
predictive information — is a **heavily-embodied seam** here already:

- **Open-loop empowerment** — `MI(action; Δpain-bucket)` = `mesh-algedonic` AGENCY_INFO.
- **Closed-loop / process empowerment** (Tiomkin, Salge & Polani, *Process empowerment for robust intrinsic
  motivation*, J. Phys. Complexity 6(3), 2025, doi:10.1088/2632-072X/adf2ec) — `I(action; Δpain | band0)`,
  the CL_UNDERCOUNT/CL_INFLATED companion.
- **Predictive information** `I(past;future)` = `mesh-precision --num pred_info`; **Maximum Occupancy
  Principle** = `mesh-vitality action_occupancy`; **transfer entropy** = `mesh-cooscillate`; **assistive
  empowerment + multi-party disempowerment** = `mesh-interruptibility` (Yang/Kleiman-Weiner).

So the *concepts* are covered. The live-literature question is about **estimation**, which is where the
recent (2024–2026) empowerment work actually lives.

## The recent result & the gap it exposes

Recent empowerment papers — open-loop empowerment, **discounted empowerment**, process empowerment
(J. Phys. Complexity 6, 2025), and RL empowerment pre-training (arXiv:2510.05996, 2025) — all center on one
practical obstacle: **empowerment is a mutual information, and MI is hard to estimate at finite sample
size.** They reach for neural / variational / surrogate estimators precisely because the naive **plug-in
(maximum-likelihood) MI estimator is positively biased**: for two *independent* variables its expected value
is not zero but

> `E[MI_plugin] ≈ (R_a − 1)(R_b − 1) / (2 N ln2)` bits    (Panzeri & Treves 2007; Miller–Madow 1955)

**The gap in `mesh-algedonic`:** AGENCY_INFO's `mi_of()` **is** the plug-in estimator, and the label
thresholds on the **raw** MI (`mi < 0.02 → LOW`, `< 0.10 → SIGNAL`, `else STRONG`). Action is binary
(`R_a = 2`), the Δpain bucket is 3-valued (`R_b = 3`), so the finite-sample bias is `≈ 1.44 / N` bits. At the
`AI_MIN_N = 6` floor that is **≈ 0.24 bits — above the AGENCY_STRONG cut (0.10)**. An **independent**
action/pain stream at small N reads **"AGENCY_STRONG — the mesh steers its own pain"** from pure estimator
bias. The open/closed-loop pair does **not** catch it (both use the same biased plug-in; CL compares two
biased quantities).

This is the mesh's own recurring failure shape — *a naive statistic without a null is a hollow sense*. It was
fixed in `mesh-cooscillate` with a block-bootstrap surrogate null
([[cooscillate-parametric-p-ignores-autocorrelation]]), and in the crypticity discard (finite-L bias fired
CRYPTIC on a period-10 signal). **The rule was asserted at one call site and left unasserted at this one**
([[a-rule-asserted-at-one-call-site-is-not-asserted]]).

## The concrete application (this edit — report-only)

A **shuffled-action surrogate null** on AGENCY_INFO: shuffle the action column against the bucket column
`K = MESH_ALGEDONIC_AGENCY_SURR_K` (default 200) times — breaking action↔bucket dependence while preserving
both marginals **and N** — and take the surrogate **95th percentile** `mi_null`. That is exactly the
finite-sample bias distribution for these marginals at this N. New fields on the output line:

```
label mi n actn cl_label mi_closed  bias_label  mi_null
```

- `BIAS_SUSPECT` — a SIGNAL/STRONG whose observed MI **cannot clear** the surrogate p95 (may be pure
  estimator bias — do **not** trust it as empowerment).
- `BIAS_REAL` — observed MI clears the null (genuine influence above finite-sample bias).
- `BIAS_NA` — AGENCY_LOW/NO_ACTION: bias only *inflates*, so a LOW read is already safe, nothing to defend.

**Report-only**, seeded RNG (reproducible verdict — the null is a property of the marginals+N, not of luck),
mirrors the CL companion's posture: it never overrides the label or any weight.

## Verification

- `mesh-algedonic --test` green (rc=0).
- **RED-first, two mutations, each drops a distinct gate:**
  - never-flag-SUSPECT (`mi <= mi_null` → `mi <= -1`) → *"agency small-n signal is bias-suspect"* FAILs
    (`got BIAS_REAL`) — the n=6 showcase signal reads real on noise.
  - always-SUSPECT → *"agency large-n real dependence is bias-real"* FAILs (`got BIAS_SUSPECT`).
- **Live on this node** (large sample): `agency=AGENCY_LOW mi=0.002 action=503/1681 aginull=0.002
  agencybias=BIAS_NA` — the null floor is correctly **tiny** at N=1681 (`1.44/1681 ≈ 0.001`), so the guard
  does **not** cry wolf at large N; it bites only in the small-N regime (fresh node, sparse pain log, short
  window) the RED-test exercises. Calibrated against the real corpus, not an assumed scale.

## Cite

- Panzeri & Treves, *Analytical estimates of limited sampling biases in different information measures*,
  Network 7:87 (1996/2007); Miller (1955) bias.
- Tiomkin, Salge & Polani, *Process empowerment for robust intrinsic motivation*, J. Phys. Complexity 6(3),
  2025, doi:10.1088/2632-072X/adf2ec.
- *Information-Theoretic Policy Pre-Training with Empowerment*, arXiv:2510.05996 (2025).
- *Intrinsic Motivation as Constrained Entropy Maximization*, Entropy 27(4):372 (2025),
  doi:10.3390/e27040372.

## Status

Uncommitted in tree (`scripts/mesh-algedonic` + this doc). Steward lands.
