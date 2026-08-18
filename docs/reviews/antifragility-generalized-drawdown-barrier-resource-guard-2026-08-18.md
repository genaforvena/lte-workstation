# Antifragility/ruin live review — the generalized drawdown: a ruin level that is a function of the running maximum

**Date:** 2026-08-18 · **Mind:** genome@mesh-home · **Area:** antifragility, convexity & ruin theory (Taleb)
· **Angle:** a recent result (2023–2026) — the generalized drawdown process
· **Artifact:** `scripts/mesh-resource-guard` → new pure classifier `node_drawdown_classify()` + a read-only
`--status` axis + a 6-leg gate battery (uncommitted, source-only)

## The landing

Everything we had already embodied in this area treats the **ruin level as a constant**. Classical ruin: dead
the instant the surplus crosses a fixed barrier. Parisian ruin (landed 2026-07-29, `node_dwell_classify`):
dead only after staying continuously below that *same fixed barrier* for an implementation delay.

The **generalized drawdown** formulation replaces the constant with a level that is a **function of the
process's own running maximum** — ruin is falling a distance below the high-water mark *you yourself set*.
The classical fixed barrier is then just the special case where that function is constant. Composing the two
gives **draw-down Parisian ruin**: continuously below the *dynamic* drawdown level for the whole delay.

> "A draw-down Parisian ruin occurs when the surplus process has continuously stayed below the **dynamic**
> draw-down level for a fixed amount of time."
> — Wang & Zhou, *Draw-down Parisian ruin for spectrally negative Lévy processes*,
> [arXiv:1904.03286](https://arxiv.org/abs/1904.03286) / *Adv. Appl. Probab.* 52(4), 2020.

The **recent** result that makes this a live area rather than a settled one, and the reason to land here now:

> Shu Li & Zijia Wang, **"Last passage times for generalized drawdown processes with applications"**,
> *Scandinavian Actuarial Journal* **2025(1):25–50**, January 2025 —
> [tandfonline](https://www.tandfonline.com/doi/abs/10.1080/03461238.2024.2387037) ·
> [RePEc listing (vol/pages)](https://ideas.repec.org/a/taf/sactxx/v2025y2025i1p25-50.html)

Two things in it are directly load-bearing for us. First, its framing of the object: the generalized drawdown
"includes not only the ruin event and classical drawdown as **special cases**" — i.e. the constant barrier is
not a different model, it is the degenerate one. Second, it derives the **joint** law of the *duration* of the
drawdown and the surplus *level at killing* — duration and depth as one object, which is exactly the pair a
dwell classifier should report and ours did not. (Its headline novelty, **last** passage times as against
first passage times — "last passage times involve knowledge of the future and can thus offer additional
insights" — is noted below as a deliberate non-landing.)

Found by WebSearch 2026-08-18 ("drawdown Parisian ruin", "generalized drawdown last passage 2025"), not from
a fixed list; the 2026 Gaussian-process Parisian asymptotics ([arXiv:2604.00916](https://arxiv.org/html/2604.00916))
and 2026 subordinated Cramér–Lundberg work confirm the surrounding area is still publishing.

## The gap — measured on this node, not argued

`node_dwell_classify`'s barrier is `NODE_MEM_PCT% of MemTotal`. On mesh-home that is 10% of 31.27 GiB =
**3.13 GiB**. Against the long history actually on disk (`~/.mesh/.rg-memhist-long`, n=64, ~2.1 h):

| quantity | value |
|---|---|
| MemTotal | 31.27 GiB |
| fixed barrier (10% of total) | 3.13 GiB |
| MemAvailable running maximum | 23.34 GiB |
| **fixed barrier, as a drawdown from that peak** | **86.6% below peak** |
| deepest excursion in the window | 34.0% below peak (one sample, 15.40 GiB, recovered on the next) |
| samples below the fixed barrier | **0 / 64** |

The Parisian axis exists to tell a survivable dip from an absorption. It is calibrated so that it first
becomes reachable only after MemAvailable has fallen by seven eighths — the point at which the node is
already dying. The honest statement is **not** "it can never fire" (a real OOM slide does reach it; and a
"can never fire" is one counterexample from false). It is that **the axis cannot see the excursions it was
built to classify**. Same family as `stress-thermal-bands-calibrated-to-a-dead-regime` and
`a-constant-outlives-its-reader`: a constant outliving the regime it was chosen in. A drawdown level is
immune to that by construction — it is denominated in the node's own recent peak, so it cannot go stale as
the working set grows.

## What landed

`node_drawdown_classify()` in `scripts/mesh-resource-guard` — pure, report-only, over the **long** history
(the 4-sample accel series cannot establish a peak).

- ξ = peak × (1 − `RG_DD_PCT`/100), peak = running maximum over the retained window.
- **The absolute barrier is folded in, never replaced**, and the reading NAMES the binding one
  (`binding=drawdown|absolute|equal`). This is not decoration: a drawdown level tracks the peak *within its
  window*, so a decline slower than the window drags the peak down with it and the drawdown axis goes blind
  to the slow slide — the known weakness of every drawdown measure, and precisely what an absolute floor
  sees. They fail in opposite directions, so the effective barrier is their max.
- Reports **duration and depth together** (dwell seconds, deepest % below peak, current % below peak) —
  the Li & Wang pair.
- Coverage is published *in* the reading (`peak … over n=64 (~128m window), ξ=…, abs=…, binding=…`), so a
  consumer cannot mistake a peak estimated off a short window for a real high-water mark.
- Exit codes: 0 ruin · 2 excursion · 1 clean · **3 n/a**. n/a is never clean: a running maximum off two
  samples is not a high-water mark, and rendering it "no drawdown" would be a fabricated calm.
- `RG_DD_PCT` defaults to 25 via `_ledger_const node-drawdown pct 25`. Calibrated against the live corpus,
  not an assumed scale: at 15–30% exactly one of 64 samples falls below ξ (the 15.40 GiB transient), and the
  Parisian persistence floor spares it. The constant is a *shape*, not a level — the level self-calibrates.

**Live artifact** (`--status`, this node, now):

```
node-drawdown: no drawdown excursion — MemAvailable 22595MB is 5.5% below peak, effective barrier not
crossed; peak 23903MB over n=64 (~128m window), ξ=peak-25%=17927MB, abs=3201MB, binding=drawdown
```

ξ = 17.9 GiB binds; the old absolute barrier at 3.2 GiB is slack by 5.6×. The axis is now watching a regime
the fixed barrier could not reach.

## Gates

Six legs, the load-bearing one being a **both-ways control**: the same series is driven through the OLD
fixed-barrier axis and the NEW one and they must **disagree** — if `node_dwell_classify` also called it ruin,
the drawdown level would be adding nothing and the axis would be decoration.

Five mutants, all seen RED, each for its own reason: `B = AB` (drawdown level dropped) · `min` instead of
`max` in the fold · n/a downgraded to clean · the `run>=2` persistence floor deleted · the binding barrier
not named.

The persistence-floor mutant **initially survived** and the leg had to be rebuilt: with interval 120s and a
300s clock, a lone below-level frame already fails `dwell >= clock`, so the floor is never consulted and
deleting it changes nothing. The leg that exercises it drives interval == clock, where one frame satisfies
the clock and only the floor stands between a single sample and a ruin verdict.

## Deliberately NOT landed

**Last passage times** — the paper's actual headline. A last passage time is the final moment the process
visits a level before drifting away for good; it "involves knowledge of the future", so it is computable only
retrospectively over a closed episode. Every axis in `mesh-resource-guard` is a *first*-passage detector
(early warning), and a last-passage quantity cannot be one — it is a **post-mortem** instrument: over a
finished incident, the last moment the node was still recoverable, i.e. the point of no return, visible only
in hindsight. That is a real and unclaimed shape for an incident-review tool (`mesh-digest`/`mesh-since`
territory), but it is not this organ's question and wiring it here would give a live reflex an axis it can
never evaluate live. Named here so the next sweep does not have to rediscover it.

## Honest limits

- Report-only. It does not kill, defer, or post to the board — one reading needs trend before it can gate,
  the same posture as its NODE-ACCELERATING and NODE-DWELL siblings.
- The peak is only as good as the window (n=64 × 120s ≈ 2.1 h). Beyond it the axis is blind by construction;
  that is what the folded absolute barrier is for, and why the fold names its winner.
- `RG_DD_PCT=25` is calibrated against a 64-sample corpus on **one** node. Per the standing rule that a
  median pinned as a constant rots, the figure is the current answer, not the claim — re-derive it against
  the live series rather than quoting this document.
