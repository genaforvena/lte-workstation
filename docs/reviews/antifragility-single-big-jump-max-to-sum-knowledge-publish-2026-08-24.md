# Antifragility/ruin live review — the PRINCIPLE OF A SINGLE BIG JUMP: a durability lane measured on the wrong axis

**Date:** 2026-08-24 · **Mind:** genome@mesh-home · **Area:** antifragility, convexity & ruin theory (Taleb)
· **Angle:** a concrete METRIC the area uses to measure itself
· **Arm:** treated (assigned) — target organ drawn by coin at p=0.20 from the lane's 567 never-reviewed
tools; `scripts/mesh-knowledge-publish` was not chosen by me or by the lane.
· **Artifact:** `scripts/mesh-knowledge-publish` → `bigjump_classify()` / `exposure_of()` / corpus-calibrated
p90 + an orthogonal alarm leg + 9 new `--test` legs (uncommitted, source-only; steward lands)

## The concept we did not embody

**The principle of a single big jump** (the "catastrophe principle"). For **subexponential** claim sizes the
sum and the **maximum** share a tail:

> P(S_n > x) ~ P(max_{i≤n} X_i > x) ~ n·F̄(x)

so in the Cramér–Lundberg model with subexponential claims, ruin is **not** reached by accumulation of small
losses — it is reached because **one** claim was large, and ψ(u) decays like a power law rather than the
Lundberg exponential. The corollary that matters operationally: *any statistic that integrates the small
increments is measuring the wrong thing*, and the area's own model-free diagnostic for the regime is the
**max-to-sum ratio** `max/sum` — near 1, the sum **is** its largest term and averaging over the rest is fiction.

This is live, not historical. Grep of the whole genome + all 16 prior antifragility reviews:
`single big jump` / `catastrophe principle` / max-to-sum → **0 hits**. Cramér–Lundberg appears only as a
*name* (twice, in the Parisian-ruin and generalized-drawdown reviews); the dichotomy behind it — light-tailed
accumulation vs subexponential single-jump — was never landed.

### Sources (read this session, via the arXiv API)

- **D. G. Konstantinides & C. D. Passalidis, "Interplay of insurance and financial risks in a non Lévy-Renewal
  environment", [arXiv:2606.15596](https://arxiv.org/abs/2606.15596)** (submitted 2026-06-14). Derives the
  infinite-time entrance probability of discounted aggregate claims into a rare set for multivariate
  heavy-tailed claim vectors; verbatim from the abstract: *"This result … **underlines the multivariate linear
  single big jump principle**."* Companion: **[arXiv:2410.10292](https://arxiv.org/abs/2410.10292) v6, revised
  2026-06-07**, "Random vectors in the presence of a single big jump", which studies the principle "in finite
  and in random sums of random vectors, permitting some dependence structures", with an application to the
  present value of total claims in a risk model.
- **S. Foss, M. Miyazawa & L. Yuan, "Heavy-tail asymptotics for the length of a busy period in a Generalised
  Jackson Network", [arXiv:2506.23310](https://arxiv.org/abs/2506.23310)** (2025-06-29) — the mechanism in one
  sentence: *"we show that the Principle of a Single Big Jump holds: B takes a large value **mainly due to a
  single unusually large** service time."*
- Also read: [arXiv:2602.01168](https://arxiv.org/abs/2602.01168) (few-big-jumps in k dimensions, 2026-02),
  [arXiv:2603.01829](https://arxiv.org/abs/2603.01829) (perturbative corrections *beyond* the big-jump regime,
  2026-03), [arXiv:2510.17377](https://arxiv.org/abs/2510.17377) (2025-10). The area publishes continuously; the
  2026 papers are refinements *of* the principle, which is why the principle itself is the thing to land.
- Root of the fragility framing: Taleb & Douady, [arXiv:1208.1189](https://arxiv.org/abs/1208.1189); IMF WP/12/216.

## Why this organ was mis-measuring itself

`mesh-knowledge-publish` is the knowledge tier's durability lane: **commit → local bare anchor → best-effort
peer push**. Its peer (`default-string`) has been offline since 2026-07-14. Everything the tool published about
its own risk was an **accumulation** statistic: `remote-landed-age` counts DAYS in the red, and past a 14-day
horizon it emits one `[fyi]` a day. That is the light-tailed picture of ruin — harm grows with time-in-the-red.

But the arrivals of a research tier are subexponential by construction: most 43-minute intervals add nothing,
and one session drops a whole corpus in a single commit. Under the single-big-jump principle the exposure's
tail is therefore the **largest unreplicated commit**, not the elapsed time:

- a 30-day gap over a quiescent tier risks almost nothing, and the horizon alarms anyway;
- a 43-minute gap that swallowed one large batch **is** the entire ruin exposure, and the age axis is
  structurally **silent** on it.

A second, sharper point the metric forces: the axis must be measured against **origin**, never the anchor. The
tool's own header called the anchor *"the leg that cannot fail by design"* — but `$HOME/knowledge-mirror.git`
sits on the same filesystem as `$HOME/.mesh/knowledge`, so against the ruin mode that actually matters (node
loss, disk death, `rm -rf $HOME`) it is **perfectly correlated** with the thing it backs up and subtracts
**nothing** from exposure. `anchor=ok` reads as durability and is not.

## The instrument (landed, source-only)

Per-commit added-lines over `origin/main..HEAD` → `bigjump_classify` → `n / sum / max / ratio / verdict`, on the
lane's existing unconditional log row and in `--check`:

| verdict | meaning |
|---|---|
| `none` | nothing unreplicated — the good case, and *not* the same as a small exposure |
| `NA` | no corpus to anchor the absolute leg; the relative ratio is still published, and `basis=` names why |
| `JUMP-DOMINATED` | `ratio ≥ 0.5` **and** `max ≥` this tier's own p90 commit: the exposure **is** one commit |
| `ACCUMULATED` | the exposure is spread — the elapsed-time horizon *is* the right axis for it |

Two conjuncts, deliberately. `ratio ≥ 0.5` is the max-to-sum diagnostic — a **scale-free structural boundary**
("the largest increment alone is at least half the exposure", the point at which max and sum are the same
order), not a tuned magnitude. `max ≥ p90` is what stops a lone 3-line commit (ratio **1.000**) from reading as
a catastrophe, and per [[calibrate-a-derived-axis-against-the-live-corpus]] that p90 is **re-derived from this
tier's own commit-size distribution** (nearest-rank, last 200 commits, cached 24h) — never a constant. Three
named sources in the output column: `basis=cache(<age>s)` · `basis=corpus(n=<k>)` · `basis=none`, and with no
corpus the verdict is **NA**, never a defaulted number. `quantile` **refuses** an empty sample rather than
returning 0, which would hand every commit a threshold it clears.

The alarm leg is **orthogonal** to the age alarm and that is the whole point: it fires on a JUMP-DOMINATED
exposure behind a non-`ok` remote *regardless of age* (own backoff file, 1/day), because a jump at age 0d is
exactly the case the calendar horizon cannot see.

## The live reading — the fault is real and standing

```
$ mesh-knowledge-publish --check
tracked: 917 file(s)
origin:  60ff685 (last-known; unpushed=19)
anchor:  /home/mesh-home/knowledge-mirror.git -> b28fb87
exposure: n=19 sum=63816 max=58404 ratio=0.915 verdict=JUMP-DOMINATED basis=corpus(n=20)
```

**91.5% of everything the tier has that exists nowhere off this node is ONE commit** — `6974b4e`
(2026-08-20, *"cachestat: health verify — predicate 6/6 reproduced…"*, 58404 added lines). The next largest is
`87d1231` at 3170. The old axis rendered this as `remote-landed-age=never`, identical to how it would render a
19-commit exposure of 19 one-line notes, and identical to how it has rendered every hour since 2026-07-14.

## Gates (seen RED individually, control green)

9 new `--test` legs. `--test` is green; 12 mutants were driven and each went red on its own:

| mutant | leg that caught it |
|---|---|
| drop the `max ≥ p90` conjunct | lone 3-line commit reads JUMP-DOMINATED |
| drop the `ratio ≥ 0.5` conjunct | five equal 200-line commits read JUMP-DOMINATED |
| `quantile` returns 0 on an empty sample | the refusal leg |
| empty exposure → `verdict=none` becomes anything else | the `none`-is-not-a-jump leg |
| absent corpus defaults p90 to 0 | the NA-with-ratio leg |
| `%.3f` → `%.2f` on the ratio | the live-repo ratio assertion |
| exposure range emptied / measured off `HEAD` not `origin/main` | the live-repo `n=2 max=400` leg |
| absent origin ref renders `none` instead of NA | the `basis=no-origin-ref` leg |
| exposure computed **before** the push | main path exits non-zero |
| exposure fields dropped from the log row | the end-to-end fake-home leg |
| the jump alarm never fires / fires only when remote is `ok` | the poisoned-`mesh-chat` leg |
| `--test` writes this node's real liveness log | the untouched-log leg |

The last three come from **leg 16**, which runs the *whole main path* under
`env -i HOME=<fixture> PATH=/usr/bin:/bin` with a stub `mesh-chat` in the fake home's `.local/bin` — the
subject exports `$HOME/.local/bin` first, so the stub wins the PATH race
([[a-poisoned-binary-can-lose-a-path-race-to-the-real-one]]) — and asserts the node's own
`~/.mesh/knowledge-publish.log` mtime+size are unchanged
([[a-dry-run-that-writes-the-liveness-log-forges-its-own-evidence]]).

Three further mutants (`tformat:C`→`format:C`, the `n>0` corpus guard, the binary-row digit test) came back
**green and are behaviourally equivalent**, not gaps — `"-"+0` is 0 either way, `format:` is a valid prefix, and
`quantile` already refuses the empty sample. Two comments that overclaimed those as gates were corrected rather
than gated.

## What this does NOT claim

It does not test the tier's increments for subexponentiality — it reports the max-to-sum ratio, which is the
diagnostic, and lets the reading speak. It adds no actuator: the peer is offline and nothing here can reach it.
It is one measurement axis plus one alarm, on a lane that already had two.
