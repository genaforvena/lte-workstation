# Trigger exogeneity: our self baseline is an observational score, and we read it as a causal one

**Live review** — information theory of agency (empowerment / predictive information), angle = a
foundational idea applied **too loosely**. Landing site: `scripts/mesh-correlate` (PREDICTION lane,
self-actuation axis). 2026-08-19, genome. Uncommitted; steward lands.

## The source (live, current)

**Jiaxin Liu (UIUC), "Discovering What You Can Control: Interventional Boundary Discovery for
Reinforcement Learning", arXiv:2603.18257v1, 18 March 2026** — <https://arxiv.org/abs/2603.18257>.

Read: the HTML full text (definitions 3.1–3.3 and the estimator). Liu defines an agent's **Causal
Sphere of Influence**: dimension *i* is inside it iff there exist an action dimension *j* and a
horizon *h ≥ 1* such that **the intervention do(a_t^(j) = u) changes the marginal distribution of
o_{t+h}^(i)** — stated with Pearl's do-operator and not conditional probability, "because the
do-operator severs all confounding paths by construction."

The load-bearing claim is **Proposition 3.2**: he constructs an MDP in which a *distractor* dimension
has **"the highest mutual information with actions among all observation dimensions, yet do(a) has
zero causal effect"** on it. A confounder drives both the true state and the distractor; the action
channel and the distractor then share information *entirely through the confounding path*. The
negative result is stated flatly — state-conditioned observational scoring cannot recover this:
**"a distractor whose dynamics covary with the agent's proprioceptive state can still receive high
scores."** No condition is offered under which the observational quantity equals the interventional
one; Prop 3.3 makes confounding-immunity a property *of using interventional data*.

His estimator is a two-phase probe: baseline trajectories under the normal policy, then trajectories
where **"all action dimensions [are] replaced by i.i.d. draws from Uniform(A)"** — do(a) = noise —
compared per dimension × horizon by a Welch t-test with Benjamini–Hochberg at α = 0.05, yielding a
binary mask over dimensions.

## Why this is new ground for us (checked first — this seam is worked hard)

`docs/reviews/info-theory-agency-*` runs to ~25 files, plus `fep-*` and `predictive-processing-*`.
Empowerment has been taken as channel capacity vs achieved flow, per-factor, discounted (EELMA),
multi-agent interference, process/open-loop, interface, relevant information, crypticity, PID
synergy, MI finite-sample bias with its surrogate null, plasticity, and — **this morning** — Ye's
agency gain `A = Err_world − Err_self` (`…agency-gain-self-blind-predictor-correlate-2026-08-19.md`,
landed in 9019dac's parent chain).

Nothing in that set is the **observational/interventional split**. The nearest neighbours:

- **MI finite-sample bias + surrogate null** (07-30) is about a number being *too large by chance*.
  This is about a number being large *for a real reason that is not the one claimed* — significance
  cannot touch it, exactly as this file's own clock-confound comment already says of the hour.
- **Agency gain** (this morning) *added* the self axis. It did not ask what generates the action
  channel. Liu's proposition is precisely the trap that opens the moment you add one.
- **Empowerment** in every prior form maximises over a policy *you set*. Nothing we have estimates
  the action side from a **logged, policy-generated** channel — which is what we now do.

## The misreading, on our own file

`scripts/mesh-correlate` grew a self baseline this morning: `selfb` predicts `B_{t+1}` from
`ACTED`/`SILENT` alone, competes in `base = max(maj, pers, clockb, selfb)`, and a pair it explains is
suppressed with the sentence *"REAFFERENCE-SUSPECT — treat as a fact about the mesh, not about the
world."*

`ACTED` is **not a randomised action**. It is the output of a policy: `mesh-room-music` grinds when a
record lands with the right measured character; `mesh-state-voice` speaks on a state edge. So the
moment the candidate `A_t` is (or proxies) the condition that fires us, `selfb` is high through a
confounding path with **no causal contribution from our hand**, and two worlds are indistinguishable
from the record:

```
A → act → B          genuine reafference     → suppressing the finding is right
A → act,  A → B      trigger confound        → suppressing the finding is a FALSE clearance
```

A false clearance is the worse error here, because it is silent: a real world link is dropped and the
log says we already explained it.

**Our own test fixture is the specimen.** The reafference fixture plants `tempo_t = BUSTLE` exactly
when the planted `room-music-sent.log` fires — so tempo predicts our firing at 100%, and the fixture
that exists to prove reafference is caught cannot itself tell reafference from trigger-confound. The
suite was standing inside Prop 3.2 without saying so.

## What shipped (and what deliberately did not)

**do(a) = noise is not available here.** Randomising `mesh-room-music` / `mesh-state-voice` fires real
audio into a real room to buy an estimate; the substrate doctrine does not trade a live actuator for
a statistic. So the *interventional* half of Liu's boundary is refused, on the record, with its
reason.

What is free is the **diagnostic** half — detect whether the confounding path `A → act` exists — by
running this lane's own lookup predictor **backwards**: how well does `A_t` predict our own firing?

- `_exogeneity()` — same lookup form, same covered subset as `selfb` and the agency gain, so all
  three describe one population. Returns `None` when the axis is `na` (never `0.0`: *"we cannot see
  the channel"* and *"the channel is independent of A"* are opposite claims).
- Above its majority class by `CORRELATE_EXO_MARGIN` (0.10) → **ENDOGENOUS**; at or below →
  **EXOGENOUS**.
- Published on every `--agency` row and inside every emitted finding's string
  (`trigger=EXOGENOUS (A_t predicts our own firing 67% vs 67% majority)`).
- The reafference lead sentence forks: ENDOGENOUS now reads **"SELF-ENTANGLED, UNIDENTIFIED — …
  reafference (A→act→B) and trigger-confound (A→act, A→B) are indistinguishable without an
  intervention on the actuator"**, and the REAFFERENCE-SUSPECT wording is kept only where our firing
  is *not* predicted by the candidate.

**Behaviour is deliberately unchanged**: `selfb` keeps competing in `base` either way. This file errs
toward silence by stated default, and an unidentified pair is not evidence of a world link. What
changes is the sentence — an unidentified suppression stops calling itself reafference, the same way
the `na`-with-cause rule stops a missing record calling itself innocence.

## Gates (both mutants seen red)

Two fixtures that are **each other's falsifier** — same tool, same lane, opposite verdicts, which is
stronger than a knob (a knob only proves the knob works):

- the existing reafference tape (we fire iff `tempo_t = BUSTLE`) must read `trigger=ENDOGENOUS`;
- a new `tape-exogenous.tsv`: we fire on a **period-3** cadence while tempo alternates on period 2
  (coprime → firing independent of tempo) and `ambient_{t+1}` follows tempo, not us. It must **emit**
  the finding *and* carry `trigger=EXOGENOUS`, and must not carry ENDOGENOUS.
- an absent actuator record must render `trigger=na`, never a verdict.

Mutation-tested from a scratch copy:

| mutant | result |
|---|---|
| verdict pinned to `EXOGENOUS` | `FAIL (an actuation channel fired by the candidate itself was not named ENDOGENOUS …)` |
| verdict pinned to `ENDOGENOUS` | `FAIL (an actuation independent of the candidate was not named EXOGENOUS — the trigger verdict is a constant, not a classifier)` |

Full suite green after: `bash scripts/mesh-correlate --test` → `smoke-test: ok (… TRIGGER
EXOGENEITY: … mutual falsifiers …)`.

## Live reading (the artifact), and its honest limit

`bash scripts/mesh-correlate --agency` on the real tape, 2026-08-19T12:03Z — self-channel **687
actuations, 88% covered**, **88/88 pairs EXOGENOUS**, and the lookup accuracy equals the majority
class **exactly** on every one (e.g. `A_t predicts our own firing 74% vs 74% majority`). So today no
finding is being falsely cleared, and `selfb` is the reafference claim it reads as. The gate is a
live classifier that is currently quiet, not a live alarm.

**The limit, stated because it matters more than the reading:** exogeneity is measured against the
tape's own 17 sense columns, so it is a **lower bound** on confounding. `mesh-sound-reflex` fires from
`~/.mesh/records.log`, which is **not on the tape at all** — an unobserved trigger is exactly Liu's
unobserved confounder, and no observational test on the tape can see it. `trigger=EXOGENOUS` therefore
means *"no column we can see predicts our firing"*, never *"our firing was exogenous"*. The way to
close it is to put the trigger channel on the tape, not to strengthen the test.

## Files

- `scripts/mesh-correlate` — `EXO_MARGIN` knob, the IBD doctrine block, `_exogeneity()`/`_exo_str()`,
  the `--agency` column, the emitted-finding clause, the forked lead sentence, and the two-fixture
  gate + `trigger=na` gate in `--test`.
- `docs/reviews/info-theory-agency-interventional-boundary-trigger-exogeneity-correlate-2026-08-19.md`
  — this file.

## Source

- Jiaxin Liu, *Discovering What You Can Control: Interventional Boundary Discovery for Reinforcement
  Learning*, arXiv:2603.18257v1, 18 Mar 2026 — <https://arxiv.org/abs/2603.18257>
