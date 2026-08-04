# second-order cybernetics — the Good Regulator Theorem, misread in our own genome

**Landed** 2026-08-04 · `scripts/mesh-homeostasis --imp` (report-only, uncommitted — steward lands)
**Angle asked:** a foundational idea we may have MISread or applied too loosely. This one was misread
in a header block we wrote ourselves, and the misreading was aiming a HELD piece of work at the wrong
deficiency.

## Source (live literature, read in full)

Manuel Baltieri (Araya Inc.), Martin Biehl (Cross Labs / Cross Compass), Matteo Capucci (University of
Strathclyde), Nathaniel Virgo (University of Hertfordshire; ELSI, Institute of Science Tokyo),
**"A Bayesian Interpretation of the Internal Model Principle"**, **arXiv:2503.00511v2 [math.OC]**,
v1 2025-03-01, v2 2025-04-19. PDF fetched and read (`pdftotext`; there is no arXiv HTML rendering for
this submission — `/html/2503.00511v2` is a 404, so the abstract page alone is not enough and was not
relied on).

Found by searching the live critique literature around Conant & Ashby rather than the concept itself;
the same sweep surfaced arXiv:2508.06326 ("A good regulator theorem for embodied agents") and
arXiv:2506.23032, **both of which `scripts/mesh-homeostasis:101` already cites** — so those were not
the landing. 2503.00511 is not cited anywhere in the genome (grep-clean) and is the one that
contradicts us.

## What the genome said

`scripts/mesh-homeostasis`, the "THE GOOD REGULATOR THEOREM" block, concluded:

> "good regulator = *you cannot reconfigure WELL without a model*" … "Per the theorem its regulation
> is bounded by the (absent) model."

and held, as the fix the theorem demands:

> "give the regulator a small DISTURBANCE MODEL — classify the egress-drift CAUSE (probe router
> reachability, `tailscale status`, the ip_forward sysctl, the upstream VPN handshake) and SELECT the
> matching correction"

## What the paper establishes

**(1) The model is a REPLICA, not a classifier.** Abstract: *"if a system (a controller) can regulate
against a class of external inputs (from the environment), it is because the system contains a model of
the system causing these inputs, **which can be used to generate signals counteracting them**."* The
model's role is generative — reproduce the exosystem's modes so the loop can cancel them — not
discriminative. §I is also explicit that the IMP *"[defines] **sufficient** conditions for the existence
of internal models"*: sufficiency, where our block asserted necessity ("bounded by the absent model").

**(2) The model the IMP guarantees is INPUT-BLIND.** §I, on the Bayesian filtering interpretation that
the IMP's internal model turns out to be: *"a simplistic case of Bayesian filtering in which the system
doing filtering **never makes use of its inputs** in any non-trivial way, meaning that although the
prior changes over time in order to track the changing hidden state, **the posterior for a given prior
does not depend on the observation or input**."* A thing whose posterior ignores its observations is
precisely not a cause classifier.

**(3) It is not even a part of the controller, and "model" is an interpretation an observer imposes.**
§I: *"although the controller isn't autonomous, its dynamics are effectively described by an autonomous
system that we call the 'autonomous attracting controller'. **This** autonomous system is the one with a
model of the environment."* And §III's contribution is a notion of *interpretation* — a map under which
a system **can be read as** a Bayesian reasoner — not a component you find inside it. That is the
second-order move proper, and it is the sense in which our block was too loose: we treated "has a model"
as an intrinsic property to be built, where the result makes it a reading to be checked.

## The transfer

Integral action **is** an internal model — of the **constant (step)** disturbance, the s=0 mode, and
nothing else. Per the IMP that buys exact asymptotic rejection of exactly that mode class. So the
theorem-licensed question is not *"does the regulator know WHY egress drifted"* but *"does the
disturbance actually live in the mode class the loop replicates?"* A drift recurring with a stable
**period** is a mode the integrator does not contain, and no amount of escalation reaches zero error on
it — the licensed fix there is a **resonator at that period**, not a classifier. The two deficiencies
are independent: a cause classifier does not help a periodic disturbance, and a resonator does not help
a one-off router reboot. The cause-classifier idea is not wrong; it is simply **not what this theorem
demands**, and it is now held as its own unlicensed idea rather than as doctrine.

## Shipped: `mesh-homeostasis --imp` (report-only, 0 behaviour change)

Reads `~/.mesh/egress-health.log` — the same essential variable the I-controller integrates — and asks
per disturbance class whether the breach process carries a periodic mode.

**Three guards, each of which changed the answer when it was added:**

1. **The null is grid-preserving.** Surrogates redraw the same number of breaches from the **same
   observed timestamp grid**: cadence and count preserved exactly, phase destroyed. A uniform-time null
   reads the *sampling*'s own rhythm as the disturbance's ([[rayleigh-rhythm-needs-sampling-cadence-null]]).
2. **The unit is an episode ONSET, not a breached sample.** A single multi-hour outage contributes
   dozens of consecutive rows 3 min apart; an independent-draw null can never reproduce that clumping,
   so burstiness alone manufactures a "period". **This is not hypothetical — it fired here.** Before
   the collapse the hard lane read `IMP-MODE-GAP @ 6h, p=0.001` on 72 breached samples; those 72
   samples are **10 episodes** (longest run 27 rows), and as episodes the class is below the floor and
   says so. A finding was retracted by its own instrument.
3. **Classes are never pooled.** `BAD` (unreachable) and `DERP` (Tailscale fell back to a relay —
   degraded, still reachable) are different disturbances on different exosystems
   ([[degraded-collapsed-to-offline-in-fusion-reader]]). Pooled, the tape read one mode at 900 s;
   un-pooled, that mode is carried **entirely** by DERP while BAD carries none of it. Pooling would
   have pinned a hard-breach mode gap that does not exist, at a period that is not the hard class's.

Candidate periods are **pre-registered, not scanned**: `[5m 10m 14m 15m 30m 1h 2h 3h 6h 8h 12h 24h]`,
each exact, multiplicity handled by taking the max over the same set inside the surrogates. A blind
geometric scan was the first draft and it did not merely lose power — **it reported the wrong period**
(an injected 6 h mode recovered as 720 s, because 21600 s fell between grid points and an on-grid
subharmonic beat it). Usable frequency resolution is ~1/span, so covering minutes-to-days by scan needs
thousands of trial frequencies. **Stated limitation: a mode at a period not in the list is invisible —
the axis answers "is it one of these", never "is it aperiodic".**

Attainable resolution is checked before any verdict: K surrogates cannot return p < 1/(K+1), so a bar
below that floor makes a positive verdict unreachable while every read says "no mode".

## Live reading (mesh-home, 2026-08-04T17:2xZ)

```
imp-mode: INSUFFICIENT
  hard      = INSUFFICIENT  breaches=10 need=12          (BAD, episode onsets)
  degraded  = IMP-MODE-GAP  period_s=900 R=0.5251 p=0.001 breaches=344   (DERP)
  samples=6265 span_h=499.0 surrogates=999 p_floor=0.001 tested=10 unresolvable=2
```

- **Hard egress breaches: no verdict is available.** 21 days of tape yield 10 outage episodes; below
  the floor of 12 the phase statistic is noise whatever the null says. This is the honest answer and it
  is the *retraction* of the pre-collapse 6 h reading, not a separate result.
- **Degraded (DERP) carries a 15-minute mode at the p-floor.** 344 episodes, every one isolated (344
  samples → 344 episodes, so the burst collapse does not touch it), R=0.5251, p=0.001 = 1/(K+1). Phase
  counts across the five sampled offsets of each quarter-hour: **50 / 0 / 97 / 178 / 19** for DERP
  versus **14 / 15 / 14 / 13 / 12** for BAD — the DERP lane clusters at 6–9 min past each quarter,
  the BAD lane is flat.
- 900 s is a cron harmonic. **Naming which `*/15` reflex is the exosystem is NOT claimed here** — the
  axis establishes that a 15-min mode exists in the degraded lane, not what emits it. That is the next
  measurement, and it is cheap.

## Gates

`--test` +8 IMP fixtures, suite 0.64 s total, rc=0. **6 mutants, each run from a scratch copy, each
rc=1:** uniform-time null (cadence trap goes red) · no episode collapse (burst trap) · no p-floor guard
(K=10 answers instead of refusing) · single fixed candidate period (injected 6 h mode missed) · no
minimum-episode floor (5 breaches get a verdict) · classes pooled (hard lane inherits DERP's mode).

**A gate the mutants caught being vacuous.** The first draft asserted `case "$out" in *INSUFFICIENT*)`.
The output line carries *both* classes, so `degraded=INSUFFICIENT` satisfied the pattern and the burst
mutant passed green. Fixed by anchoring every assertion to its own field (`hard=…`, `degraded_period_s=…`).
A live instance of [[substring-scan-turns-prose-into-a-verdict]], caught only because the mutant was
run — the suite had been green on a gate that asserted a *different class's* value.

`mesh-land --check` rc=0. Report-only: `--imp` writes nothing and no other path calls it.

## Held

- The **resonator** (an internal model at the measured period) is a behavioural change to a substrate
  regulator — same hold as the rest of this tool's actuator (`:68-72`), and today the hard lane has no
  verdict to act on anyway.
- **Naming the `*/15` exosystem** behind the DERP mode.
- The **cause classifier** stays held, now correctly labelled as an idea this theorem does not license.
