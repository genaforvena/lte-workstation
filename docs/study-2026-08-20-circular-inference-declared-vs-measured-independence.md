# Live review — predictive processing / the Bayesian brain: the half of precision that is architectural

**Date:** 2026-08-20 · **Lane:** LITERATURE (live review) · **Landed in:** `scripts/mesh-operator-home`

## The angle: a foundational idea we applied too loosely

`scripts/mesh-precision` opens with a 2026-06-20 live review and gets **precision** right as *gain*:
precision = inverse variance, down-weight the noisy axis, up-weight the reliable one. That is the
mainstream reading, and the current literature agrees it is the load-bearing one — Lao-Rodríguez,
Cacciato-Salcedo & Malmierca, *"The predictive processing embodied in brain conditions: the role of
precision"*, **Frontiers in Psychology 17:1887747 (2026)** frames the whole review as neuromodulatory
gain control: *"Precision acts as a weighting mechanism that determines the reliability or relevance
of prediction errors."*

What that review does **not** contain is the other half. Checked directly: it does not cite Jardri &
Denève and does not address message reverberation or evidence overcounting at all. The gain story and
the *architectural* story of precision have come apart in the live literature, and the mesh inherited
only the first.

## The concept we do not embody: the message exclusion principle, and κ

**Vincent Bouttier, Renaud Jardri & Sophie Denève, "Circular Belief Propagation for Approximate
Probabilistic Inference", arXiv:2403.12106 [cs.AI], 17 Mar 2024** — the algorithmic core of the same
lab's circular-inference account of psychosis (**Jardri & Denève, "Circular inferences in
schizophrenia", *Brain* 136(11):3227, 2013**).

Verbatim from §2.2, on why belief propagation is exact at all:

> a message m_{i→j} is computed based on all messages m_{k→i} received by the sender node **except**
> the opposite message m_{j→i}, therefore preventing this message from being reverberated and thus
> **counted twice**.

and on where it breaks:

> in the presence of cycles, the same evidence travels multiple times through loops of the graph, and
> is **mistaken for new evidence** … correcting for these loops of length 2 is no longer sufficient.

CBP's answer is not a bigger hand-drawn graph. It is two **fitted** scalars in the update (their
Eq. 4; standard BP is the special case (α,κ,β,γ)=(1,1,1,1)):

- **α_ij**, per undirected edge — *"decorrelates opposite messages"*: how much of the opposite message
  is re-admitted rather than excluded outright.
- **κ_i**, per variable node — *"fights the belief amplifications caused by messages being
  reverberated"*: an exponent on the whole product of incoming messages, i.e. a **damping of
  accumulated support learned from data** rather than declared by the modeller.

## What we already had, and why it is the α-only half

`mesh-operator-home`'s `_calibration` sidecar counts how many modality groups vote HOME. Its
independence partition is `PHONE = lan OR ts` — *"lan & ts are the same device"*. That is precisely
**one hand-drawn exclusion on one known length-2 loop**. `_asocial` (added 2026-08-18 from the
swarm-bias review) then discounts an axis that is constant-positive across a window in which the world
moved. Neither is κ. Both are **declarations about the graph**; nothing in the tool had ever *measured*
whether two axes it calls independent behave independently.

That is the sidecar's own founding complaint — *"agreement cannot separate a zealot from a second
witness"* — one level up, aimed at the partition instead of at the votes. The hand-coded Bose
exclusion was generalised into `_asocial`; the hand-coded *partition* never was.

## What measuring it actually found (live tape, `~/.mesh/op-home-axes.log`, n=1349)

Three results, two of them corrections to what I expected before measuring:

1. **`phone~ble` R = 0.012.** These are the only two axes probed *unconditionally* (817 co-positive
   records, 60.6% of all evals — the sidecar's dominant `corroborated 2/4` path). I went in expecting a
   double count and the tape falsified it: they are genuinely independent. The verdict was honest, and
   is now honest **by measurement** rather than by the author's confidence.

2. **You cannot measure an axis against the fused verdict.** `status` is a deterministic function of
   the very votes on the same line, so `I(status; ble | phone) = 0.124 bits` is a readout of the
   decision tree, not of the world. Redundancy here is **axis-vs-axis only**; `status` is skipped.

3. **A statistic over a conditionally probed tape measures the gate, not the world.** `att` and `cam`
   are probed *only* on the would-be-AWAY path (both phone axes dark), so `phone~att` can never be
   co-positive — and a naive reading of the live tape scores `phone~att` **R = 0.58, the single highest
   number on the file**, entirely from the probe gate. Folding on it would collapse the exact pair
   SIGNAL 4 exists to keep separate. A pair with no co-positive record is therefore **`n/a`, never 0**.

And one thing measuring surfaced that nobody was looking for: **`cam` has voted 1 exactly zero times in
1349 records.** Zero entropy, redundancy undefined against everything, and it has been silently padding
the `/4` denominator — a verdict advertising four modality groups while one of them has never once
spoken. That is now published as `MUTE axis`, because a mute axis and an absent axis are different
claims.

## The change

`scripts/mesh-operator-home` gains `_redundancy <tape> [min_n] [window] [thresh_pct]` →
`"<collapse-csv|-> <mute-csv|-> <n>/<min_n> <detail>"`, measuring pairwise
**R = I(a;b) / min(H(a),H(b))** straight off the axis tape, and `_calibration` gains a 7th argument
that folds a measured-redundant co-probed pair to **one witness** before counting support — the κ move,
with a threshold (`MESH_OP_AXES_REDUN_PCT`, default 70) instead of a partition. Coverage `n/min_n` is
published beside every judgement, so "no collapse" can never read as "checked and clean" on a thin tape.

Live output today:

```
HOME — phone on home WiFi (192.168.8.146)
  calibration: LONE source (phone) — verdict rests on one modality, no group to calibrate against
  calibration: pairwise redundancy phone~ble=1,phone~att=n/a,phone~cam=n/a,ble~att=n/a,ble~cam=n/a,att~cam=n/a over 288/24 records (n/a = never co-positive: att/cam are probed only when the phone axes are dark, so that pair measures the GATE, not shared evidence)
  calibration: MUTE axis cam — zero positive votes in 288/24 records; it is padding the /4 denominator, not corroborating anything
```

## Gates, seen red

7 new tape cases, all sandboxed (the fixtures never touch the durable tape). Five mutants driven from a
scratch copy, each confirmed red before restoring:

| mutant | result |
|---|---|
| `cop == 0` no longer renders `n/a` | RED — renders `phone~att=100` and **collapses** the gated pair, reproducing the exact failure the live tape predicted |
| `_calibration` ignores the measured collapse (κ removed) | RED — locked pair reads `corroborated 2/4` again |
| mute-axis detection removed | RED |
| threshold can never fire | RED |
| zero-entropy pair scored `0` instead of `n/a` | RED (only after case (m) was added — the first version of this gate was **unreachable**, since a zero-entropy axis is usually already caught by the co-positive rule; a constant-*positive* axis is the reachable path) |

Honest limit: Rule 1 (never measure an axis against the fused verdict) is enforced **by construction** —
`_redundancy` iterates a fixed axis list, so `status` cannot enter the detail even with the guard
removed. The `if (k == "status") continue` line is belt-and-braces and has **no gate**; it is documented
as such rather than dressed up with a test that cannot fail.

## Doctrine

**An independence partition is a claim about the world, and a claim about the world must be measured.**
The mesh already knows that agreement cannot separate a zealot from a second witness. The unnoticed
sibling: *a modality label cannot separate two organs from one*. BP's exclusion rule handles the loop
you drew; κ damps the ones you did not. When you cannot enumerate the paths, do not declare the
partition — measure the redundancy and damp the accumulation.

**And the measurement has its own gate:** a redundancy statistic over a conditionally probed tape
measures the probe gate. The highest correlation on our live tape is manufactured entirely by an `if`.

## Sources

- Bouttier, Jardri & Denève, *Circular Belief Propagation for Approximate Probabilistic Inference*, arXiv:2403.12106 [cs.AI], 17 Mar 2024 — <https://arxiv.org/abs/2403.12106>
- Jardri & Denève, *Circular inferences in schizophrenia*, Brain 136(11):3227, 2013 — <https://academic.oup.com/brain/article/136/11/3227/324497>
- Lao-Rodríguez, Cacciato-Salcedo & Malmierca, *The predictive processing embodied in brain conditions: the role of precision*, Front. Psychol. 17:1887747, 2026 — <https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1887747/full>
- Furutachi & Hofer, *Rethinking Predictive Processing*, Annual Review of Neuroscience 49, online 16 Apr 2026 — <https://www.annualreviews.org/content/journals/10.1146/annurev-neuro-102124-031410> (paywalled; read via abstract only — its thesis that prediction-error signals "may appear similar in their responses yet reflect fundamentally different underlying computations" is the same shape one level up, and is left unlanded here)
