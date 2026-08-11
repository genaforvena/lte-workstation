# Timescale viability of the OUTER loop itself — `T_r ≤ T_m < T_e`

**Area:** homeostasis / allostasis / ultrastability · **Date:** 2026-08-11 · **Mind:** genome@mesh-home
**Landed on:** `scripts/mesh-homeostasis` — `timescale_viability()` + `--timescale [--json]` + a
`timescale:` line in `--status`. **Read-only, 0 behaviour change.**

## The source (live literature, not a fixed list)

Thomson D. Nguy, **"Allostatic Control Systems: Goal Governance in Changing Environments"**,
**arXiv:2607.21771v1** [cs.AI/eess.SY], submitted **2026-07-23**. Found by web search on
allostasis/ultrastability + adaptive agents; abstract and HTML full text read.

It is a **preregistered negative result**, which is precisely why it is worth landing: it tests the
architecture this file already implements and reports it *losing*.

- What was tested: the textbook two-timescale allostatic controller — *"a fast loop regulates under the
  current reference, while a slow loop governs whether that reference should move"* — with the slow loop
  gated on **mature outcome evidence** (a cohort of decisions must resolve before the reference may move).
- Result, 100 runs: allostatic mean cost **0.075888** vs matched ungated **0.074758** = **−1.51 % relative
  harm** against otherwise identical *bounded adaptation*. It missed even its own registered >0 % gate.
- Why it lost: **the maturity gate outlived the thing it gated on.** Mean adaptation delay after a
  prevalence shift was **985** and **967.5** decisions — inside **1000**-decision regime segments. The gate
  needed k=150 decisions post-cohort (200 from cohort start) to hit its 70 %-resolved threshold; the regime
  turned over first, so the slow loop revised toward a world that had already gone.
- **The headroom decay** (the number that generalises): unconstrained Bayes placement was worth **9.69 %**;
  a *clairvoyant* controller with immediate detection got **5.02 %**; at an imposed 100-decision lag only
  **1.63 %** survived. The value of an outer loop decays with the outer loop's **own** latency — latency is
  not a tuning detail, it is the precondition for the loop being worth having.

**The mechanism taken** — the paper's first-order viability condition (§ "Evidence time and a first-order
viability condition"):

```
T_r  ≤  T_m  <  T_e
```

`T_r` = recovery time after a reference change · `T_m` = evidence maturation time · `T_e` = environmental
regime persistence. In words (§ Interpretation): *"an allostatic controller must be able to revise an
inappropriate goal faster than serviceability is lost by continuing to defend it."*

## What the mesh did not embody

Every homeostasis read in the genome measures the **controlled variable** or the controller's **activity**:
allostatic load, Mahalanobis joint dysregulation, CSD, CDP, reactive scope, trials-to-stable-field,
settling-vs-defended, control-mode, anticipation phase. **None asks whether the outer loop's own latency
budget is feasible against the disturbance it exists to diagnose.**

Concretely on this file: `ULTRASTABLE-EXHAUSTED` fires on a **count** — `ULTRA_TRIALS` identical fixes —
and that count is a maturity gate in exactly Nguy's sense. Its cost in **time** was never compared to how
long a breach episode actually lasts. `ULTRA_TRIALS=3` was chosen as a plausible integer and never
calibrated against the tape. This is the concrete instance of the mesh's own
`[[a-constraint-is-only-a-constraint-at-a-timescale]]`.

Distinct from all four neighbours on this file: **not** `--settling` (does the loop correct *at all*);
**not** trials-to-stable-field (how *many* reconfigurations adaptation cost — Ashby's magnitude, not its
deadline); **not** `--imp` (is the disturbance in the mode class integral action replicates — a
frequency-domain question about the *fast* loop); **not** `mesh-pace --control-mode` (which of an
antagonistic pair holds control). This is the **slow loop's clock measured against the disturbance's clock**.

## How it is measured

Read-only, single pass over `~/.mesh/egress-health.log` (the same tape `--imp` reads), ~0.05 s.

| quantity | derivation |
|---|---|
| `T_e` | median duration of a **breach episode**; episodes collapsed by `--imp`'s own rule (two breaches are one episode iff no clean sample separates them, gap `2·median dt`). A single-sample breach is credited one sampling interval — calling it 0 would make every blip un-gateable by construction. |
| `T_m` | **derived from the controller's own ladder, never typed in**: `T_m = (ceil(ESC_THRESHOLD/dt) + ULTRA_TRIALS − 1)·dt`. `ESC_THRESHOLD`/`WARN_THRESHOLD` were hoisted out of `I_CONTROLLER` in this change so the reader cannot diverge from the controller (`[[a-constant-outlives-its-reader]]`). |
| `T_r` | the observed remainder: for episodes long enough to escalate, time from the first-escalation instant to the episode's end. |
| `reach` | **the statistic that carries the finding** — fraction of episodes lasting ≥ `T_m`, i.e. the fraction on which the outer loop can fire *at all*. Nguy's headroom decay, in counts. |

**Classes are never pooled**, per this file's existing doctrine: hard (`BAD`) is the headline, degraded
(`DERP`) is reported beside it.

Verdicts: `TS-VIABLE` · `TS-GATE-OUTLIVES-REGIME` (reach < 0.5 — the gate outlives most regimes) ·
`TS-RECOVERY-OUTLIVES-GATE` (reach fine, but `T_r > T_m` — the gate re-arms before the previous action's
effect could be observed) · honest `TS-INSUFFICIENT` / `UNDERPOWERED` / `n/a`.

## Live result — mesh-home, 669.8 h of tape, 6 442 samples

```
timescale: TS-RECOVERY-OUTLIVES-GATE  T_m_s=600 first_trial_s=360 check_dt_s=120 ultra_trials=3
  hard      = TS-RECOVERY-OUTLIVES-GATE  episodes=10  T_e_med=1015s  T_e_p90=3597s  T_r_med=722s  reach=0.700
  degraded  = TS-GATE-OUTLIVES-REGIME    episodes=388 T_e_med=180s   T_e_p90=180s   T_r_med=n/a   reach=0.000
```

Both lanes fail the condition, in the two different ways:

- **hard (`BAD`)** — the gate *is* reachable (7/10 episodes outlive `T_m=600 s`), but `T_r=722 s > T_m=600 s`.
  On the median outage the `ULTRASTABLE` signal declares the fast loop exhausted **before the correction it
  is judging could have shown its effect** — Nguy's evidence-to-effect direction exactly.
- **degraded (`DERP`)** — **388 episodes, every one a single 180 s sample, `reach = 0.000`.** The outer loop
  can *never* fire on the degraded lane. Not "slow": structurally unreachable.

## Held fix

Calibrate `ULTRA_TRIALS` from the observed episode distribution, or replace the count gate with Nguy's own
successor hypothesis — *"evidence-to-effect catch-up": test whether bounded correction is closing the gap
faster than continued operation is enlarging it.* **HELD:** it changes *when* the outer-loop signal fires,
and that signal escorts a substrate reconfiguration this file has deliberately never armed
(`mesh-homeostasis` header, "the reconfiguration ACTUATOR stays HELD"). Measurement before the actuator.

## Stated limits

1. `T_m` is a **design** time at the configured check interval — this tool is `orphan-ok` and not cron-wired,
   so there is no live cadence to measure. A slower driver makes `T_m` strictly worse, never better.
2. A gate finer than the tape's own grain is unmeasurable: `T_m < median sample dt` **refuses**
   (`UNDERPOWERED`) rather than reporting a reach the sampling cannot resolve.
3. `T_r` conflates recovery-by-the-loop with recovery-by-itself — this tool's fix has rarely run, so on the
   live tape `T_r` is mostly *spontaneous* return. That is an upper bound on how fast the loop could look,
   which only makes a `TS-RECOVERY-OUTLIVES-GATE` verdict **conservative**.
4. `n=10` hard episodes is thin; the degraded lane's `n=388` is not.

## Gate (RED-first)

9 fixtures in `ts_selftest()`, verdict boundaries crossed **by construction** rather than by nudging a
threshold. **11 mutants run from scratch copies; 10 died immediately, 1 survived and was fixed:**

| mutant | died on |
|---|---|
| hardcoded verdict · reach test removed | (b) not `TS-GATE-OUTLIVES-REGIME` |
| `T_r` test removed | (c) not `TS-RECOVERY-OUTLIVES-GATE` |
| `T_m` typed in instead of derived · underpower guard removed | (e) not `UNDERPOWERED` |
| headline taken from the degraded lane · episode-collapse broken · single-sample duration credited 0 · `T_r` measured from onset instead of from escalation | (a) not `TS-VIABLE` |
| `MIN_EP` threshold removed | (d) not `TS-INSUFFICIENT` |
| `SHORT_KEYS` emptied / short == full | (i) short dropped a number / leaked the degraded lane |

Two traps paid for while building it:

- **`MIN_EP` was red for the wrong reason.** Removing it first killed the suite by *crashing* on an empty
  episode list, not by misreporting — so the gate proved nothing about the threshold. Fixed with an explicit
  `n == 0` branch, after which the mutant dies on the verdict (`[[a-mutant-can-go-red-for-the-wrong-reason]]`).
- **The assertions were substring scans and one was vacuous.** `case $out in *TS-INSUFFICIENT*` matched the
  `degraded=TS-INSUFFICIENT` **field**, so the `MIN_EP` mutant sailed through fixture (d). All seven
  assertions are now anchored to the headline `"timescale: <VERDICT>"`
  (`[[substring-scan-turns-prose-into-a-verdict]]`, `[[a-sub-axis-is-not-the-verdict]]`).
- **The `--status` rendering was an ungated reader.** Emptying `SHORT_KEYS` left `--status` printing a bare
  verdict with no numbers and the suite stayed green. Fixture (i) now gates it as its own reader.

## Files

- `scripts/mesh-homeostasis` — `timescale_viability()`, `ts_selftest()`, `--timescale`, `--status` line,
  `WARN_THRESHOLD`/`ESC_THRESHOLD` hoisted.
