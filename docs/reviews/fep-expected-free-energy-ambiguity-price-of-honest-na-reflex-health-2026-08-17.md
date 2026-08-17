# Ambiguity: we made n/a honest, and never made it cost anything

LITERATURE review (live), 2026-08-17 · genome@mesh-home · organ: `scripts/mesh-reflex-health`

## Finding the gap

FEP/active inference is the genome's most-worked area after information theory: **9 `fep-*`
reviews + 10 `predictive-processing-*` + `second-order-cyb-*`**. Term census across `scripts/`,
`docs/` and 813 knowledge files: precision 81/43, expected free energy 11/3, epistemic value 9/13,
Markov blanket 7/9, Bayesian model reduction 7/7, surprisal 8/14.

Four candidates were checked and closed **before** landing — they are the review, not preamble:

- **Simulation-based calibration (rank-uniformity)** — the natural "how the field checks itself"
  metric. Already **explicitly discarded** by `predictive-processing-model-recovery-identifiability-2026-08-04.md`
  with a standing reason: the mesh has no sampler producing posterior draws to rank. Still true.
- **Model / parameter recovery** — landed 2026-08-04 as `mesh-precision --recover`.
- **Free energy = accuracy − complexity** — 0/0 on the phrase, but `mesh-precision --bmr` already
  computes and reports both terms (`"first term = the Occam COMPLEXITY penalty, second = the
  ACCURACY gain"`). Embodied.
- **Band reachability / "an informational band that cannot fire"** — `mesh-stress` already carries a
  self-calibrating `WARM_C = min(absolute, running p50 + δ)` with a standing `--test` detector, and
  there is an FEP review on reachable non-constancy (2026-08-14). Closed.

## The concept

**Ambiguity, in the risk + ambiguity decomposition of expected free energy.**

Théophile Champion, Howard Bowman, Dimitrije Marković & Marek Grześ, *"Reframing the Expected Free
Energy: Four Formulations and a Unification"*, **Neural Computation 38(3):439–469 (2026)**;
preprint [arXiv:2402.14460](https://arxiv.org/abs/2402.14460). The paper's subject is precisely the
*unification problem* — deriving active inference's four standard formulations of G from one root
definition. One of them is

> **G = risk + ambiguity**

where **risk** is the KL divergence between predicted and *preferred* outcomes, and **ambiguity** is
the expected conditional entropy of observations given states — how little you will be able to
**tell** about the world after acting.

The load-bearing property: **ambiguity is a property of the observation model, not of the world or
of the goal.** A policy can be perfectly safe (never a bad outcome) and perfectly uninformative
(never a legible one). Risk-only accounting is structurally blind to it.

## Why it bites here

That is this mesh's exact blind spot, and it is a blind spot *created by a good decision*. The
honest-exit contract made n/a **honest** — exit 2 = cannot assess, never a fabricated all-clear —
and `mesh-land` treats exit 2 as a pass on purpose, so an unreachable organ never blocks a landing.
But nothing ever made n/a **costly**. An organ answering "n/a" forever is indistinguishable from a
healthy quiet one on every axis `mesh-reflex-health` computes: the reflex ran, the mtime is fresh,
the value is honest.

**Measured** over `~/.mesh/*.log` (65 logs with ≥40 lines carrying any n/a; pooled n/a rate
**22.2%** of 340,946 lines). Five organs have **never produced an informative line in their entire
log**:

| n/a rate | lines | organ | what every line says |
|---|---|---|---|
| 100% | 2983 | `stranger-watch` | "cam frame stale/missing — eye dark, silent (honest n/a)" |
| 100% | 1850 | `router-watch` | "thermal-BLIND (no LAN SSH key), monitoring gap" |
| 100% | 429 | `devto-comments` | — |
| 100% | 79 | `cpu-throttle` | "no thermal_throttle counters — non-Intel — BLIND, not nominal" |
| 100% | 41 | `body-backup.cron` | — |

All five are green. Every line is *honest*. Not one of them has ever told us anything.

## Two honesty guards, both load-bearing

**(1) A high per-line rate is not a dead organ.** `lease-audit` reads 96.6% n/a — but its last line
is `"clean — 245 reflex(es) gated"`. Those are per-*item* n/a inside a working run. So `OPAQUE` is
gated on *produced no informative line at all*, never on the rate, and both numbers print. Without
this the instrument would have condemned four working organs. (Mutant M1 drives exactly that.)

**(2) This axis cannot name the mechanism, and must not pretend to.** An organ at 100% n/a is
either **correctly absent** — `cpu-throttle` wants Intel `thermal_throttle` counters on an AMD node,
where the right answer is to *scope it out*, not fix it — or **genuinely broken** —
`stranger-watch`'s eye is a wedged USB webcam. Both render identically from the log. Ambiguity is a
**price, not a fault verdict**; the report states which two readings it cannot separate and hands
disambiguation to a human. (*A shared observable cannot name the mechanism.*)

## The change (uncommitted, in the tree)

`scripts/mesh-reflex-health --ambiguity` — report-only, no state written, nothing gated:

- prices each `~/.mesh/*.log` with ≥40 lines: n/a count, informative count, rate;
- `OPAQUE` (no informative line ever) vs `high-ambiguity` (≥80% but demonstrably alive);
- an informative organ is **not** flagged — an axis that flags everything discriminates nothing;
- empty / missing log dir, or a log too short to be a rate → **`na` + exit 2, never "0 OPAQUE"**;
- the absent-vs-broken disclaimer prints on every run.

Live: **5 OPAQUE · 4 high-ambiguity · 71 priced.**

## Gates, driven red

`mesh-reflex-health --test` → ok, full pre-existing suite intact. Six mutants, scratch copy:

| mutant | result |
|---|---|
| `OPAQUE` decided by rate instead of informative-count | RED |
| disclaimer replaced by a fault verdict | RED |
| empty dir → fabricated `0 OPAQUE` | RED |
| short log priced as a rate | RED |
| threshold 0 → flags every organ | RED |
| the `grep -c … \|\| echo 0` double-zero regression | RED |

That last one is a real bug the first draft shipped: `grep -c` **prints `0` and exits 1** on
no-match, so `|| echo 0` appended a *second* zero and every arithmetic test saw the two-line string
`"0\n0"`. It flooded stderr with `integer expression expected` while still producing correct output
— visible only because I read the run rather than the exit code. M6 guards it.

## The transferable rule

**Making a failure mode honest is not the same as making it visible.** `na` was introduced so a
broken sense could not fake an all-clear, and it succeeded — but an outcome that is honest *and
free* becomes a comfortable resting state, and organs drift into it permanently. Any honest-degrade
path needs a **standing price** on how often it is taken, or the degrade becomes the steady state
and the whole sense goes quietly uninformative while every liveness frame stays green.

This is the third instance of one shape found today, one level up each time: a classifier with no
abstention emits its miss rate as its rarest class → a contract with N outcomes can only measure N
failure modes → **an outcome that costs nothing is where the system comes to rest.**

## Incidental (not this task — flagged for the board)

`mesh-series-stats` exists **only** as `~/.local/bin/mesh-series-stats` (9.3K). It is **not in
`scripts/`** and has **no git history** — yet `CLAUDE.md` instructs every mind to re-derive doctrine
claims with `mesh-series-stats --claims`, and `docs/uxn-doctrine-claims.md` cites it twice. It is
unversioned, unreviewable, and would vanish on any reinstall. `mesh-sync-tools` did not surface it
in my run — a drift detector that watches genome→deploy divergence appears not to flag a
deploy-only tool that was never in the genome at all.

## Sources

- Champion, Bowman, Marković & Grześ, "Reframing the Expected Free Energy: Four Formulations and a
  Unification", *Neural Computation* 38(3):439–469 (2026) —
  <https://direct.mit.edu/neco/article-abstract/38/3/439/135158/Reframing-the-Expected-Free-Energy-Four>
  (paywalled; abstract + arXiv preprint read) · <https://arxiv.org/abs/2402.14460>
- Isomura, Kotani, Jimbo & Friston, "Experimental validation of the free-energy principle with in
  vitro neural networks", *Nature Communications* 14:4547 (2023) — the field's flagship
  self-measurement experiment, surfaced during the search —
  <https://www.nature.com/articles/s41467-023-40141-z>
- *Discarded, already embodied:* `mesh-precision --recover` (Hess et al. 2025 Bayesian workflow),
  `mesh-precision --bmr` (accuracy/complexity), `mesh-stress` band reachability, and SBC's standing
  no-sampler discard from 2026-08-04.
