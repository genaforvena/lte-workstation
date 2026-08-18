# Per-factor empowerment: a joint spread is not control of any axis

**Live review** — information theory of agency (empowerment / predictive information), angle = a
known **failure mode** of the area. Landing site: `scripts/mesh-sound-reflex` (`coverage()`).
2026-08-18, genome. Uncommitted; steward lands.

## What we already embodied (checked first — this seam is worked hard)

Twenty prior reviews under `docs/reviews/info-theory-agency-*`: open-loop and process empowerment,
channel **capacity** vs achieved flow, multi-agent interference-channel empowerment, discounted
(EELMA) empowerment, MI **finite-sample bias** and its surrogate null, relevant information,
crypticity, partial information decomposition (synergy), semantic information, plasticity
`I(O→A)`, predictive information and predictive information **rate**, overwrite-vs-identification,
blind goal-directedness, restless-arm pacing. The MI **estimator** critique is ours already. What
is **not** ours is the critique of the *objective's shape* — of what a correct, unbiased,
perfectly-estimated aggregate MI still fails to say.

## The landing: Focused Skill Discovery (per-factor empowerment)

**Allen et al., "Focused Skill Discovery: Learning to Control Specific State Variables while
Minimizing Side Effects", arXiv:2510.04901** (OpenReview `eM5ZtMijef`; RLDM version at
`camallen.net/files/focused_skill_discovery_rldm.pdf`). Found by live web search 2026-08-18 from
the MI-skill-discovery critique line; abstract and body read via `arxiv.org/html/2510.04901v1`.

Two claims, and the second is the sharp one.

**1. Aggregate empowerment does not decompose into control.** Maximising `I(Z; S_T | s_0)` over the
*whole* state buys distinguishable outcomes, nothing more: the discovered behaviours "tend not to
provide the agent with much actual control over the individual state variables present in many
reinforcement learning environments" — "skills might learn to navigate to different positions
without learning to collect—or avoid—specific objects", because "skills are only encouraged to
reach different states, regardless of the individual state variables that are changed." Their fix
is a per-factor reward, `r_focused(z,h) = Σ_{i∈V_z} r_i(z, h^i) − ℓ(h, V_z^c)`: score each target
variable separately, penalise movement of the rest. It recovers **3.0–5.3× state coverage** on the
same algorithms (VIC 1.86 vs 0.35 AUC, DIAYN 1.69 vs 0.62, LSD 1.84 vs 0.61) — the aggregate
objective was leaving that on the table purely by never asking per-axis.

**2. A constant is invisible to a spread.** Their argument against DUSDi (which minimises MI with
non-target variables as its side-effect term) is the transferable one: **"having the _same_ effects
on non-target variables does not mean that there are _no_ side effects."** A repertoire whose every
skill knocks the same coffee cup over identically has *zero* mutual information with the cup — the
side-effect term is perfectly minimised while the damage is maximal. Statistical independence is
invariance across the choice, not absence of effect, and no variance-, MI-, or
distinguishability-shaped measure can tell them apart.

This is a shape the genome already knows from other directions — the silent fallback (a constant
indistinguishable from a success), `tone`'s median==max, the value-frozen mtime — but never as a
statement about our **diversity** measures, which is where it bites.

## Where it bites: `mesh-sound-reflex` coverage and repellent

The grinder has two distinguishability-shaped measures and **both** are aggregates over axes:

- `nearest_ideal().dist()` (line ~369) is the **mean** of per-axis normalised distances, gated at
  `SR_EPSILON=0.22`. Movement concentrated in two axes clears it; the other three may be pinned.
- `coverage()` counts distinct **joint** recipe-cells `(l-bucket, s-bucket, f-bucket, band)` in the
  trailing window. A cell is distinct if *any* component differs.

Neither can see a dead axis, and the file has already been bitten by exactly this — the ergodicity
note found "**two of five recipe axes were dead for room material**" and needed a *separate*
mixture test on the ranking corpus to find it, because the repellent and the occupancy count both
read green through it.

**Measured, not argued.** A synthetic 30-render corpus roaming `l`/`s`/`f` with `band` pinned for
the whole trailing window:

```
COVERAGE cells=22 renders=30 trailing_occ=6 recent_new=4 occ=0.50 verdict=expanding
```

One of four axes dead; verdict clean. (A 14-render variant with `band` pinned from the start reads
`occ 0.92 verdict=expanding`.) The live corpus is **currently clean** on this — 1749 renders, all
four axes moving in the trailing window — so this is a detector for a blindness the metric
structurally has, not a live fault.

## The fix (uncommitted, in the tree)

`coverage()` now publishes a **per-factor** leg off the *same* `rows` the joint count uses (one
parser, so it cannot rot apart from the number it qualifies):

```
per-factor spread: l=live(4)  s=live(4)  f=live(4)  band=live(3)
COVERAGE ... focus=l:live,s:live,f:live,band:live frozen=0 occ=1.00 verdict=expanding
```

Three-way classification, because a constant has three causes and only one is a fault:

- **`frozen`** — the axis moves somewhere in the corpus but not in the window. It *can* move and
  isn't: the collapse. Named explicitly on the human line.
- **`flat`** — never varied anywhere. A single-valued pool and dead-from-birth are not separable
  from the log, so it is reported, never accused.
- **`na`** — the window carries only the parse-failure sentinel. Blindness must not render as a
  healthy constant (nor as a collapse).

Report-only, per this file's report-only-before-alarm discipline, and printed **before**
`verdict=`, so the field every existing consumer parses with `${line##*verdict=}` is unchanged.

## Gate (seen RED in both directions)

New `--test` leg. The load-bearing assert is the second one: the frozen-axis corpus must *also*
still read `verdict=expanding` with `occ ≥ 0.5`, because a leg that only fires where the joint
count already said `collapsed` would be asserting nothing new. Plus two false-accusation guards
(a roaming corpus accuses nothing; a never-varied axis reads `flat`).

Falsified from a scratch copy, both directions:

- **mutant 1** — `frozen` branch deleted (classify as `live`):
  `FAIL: ... reported frozen=0, not 1 — the per-factor leg does not see a dead axis` /
  `FAIL: the frozen axis must be NAMED — focus read 'l:live,s:live,f:live,band:live'` (rc=1)
- **mutant 2** — `flat` collapsed into `frozen` (over-eager):
  `FAIL: the roaming corpus was accused of 1 frozen axes — false positive` /
  `FAIL: an axis that never varied ANYWHERE must read 'flat' ... frozen=4` (rc=1)

Unmutated: `smoke-test: ok`, rc=0.

## Not done (deliberate)

The **repellent** (`dist()`, the mean-over-axes epsilon gate) carries the identical blindness and is
*not* touched here. It is the reflex's reward-defining object — changing what clears epsilon changes
what gets rendered — and the honest first move on a live corpus that currently shows no frozen axis
is to watch the report, not to re-aim the grinder. The per-factor report is the instrument that
would justify that change; it does not yet exist as evidence.

## Sources

- Allen et al., *Focused Skill Discovery: Learning to Control Specific State Variables while
  Minimizing Side Effects* — https://arxiv.org/abs/2510.04901 · https://arxiv.org/html/2510.04901v1
  · https://openreview.net/forum?id=eM5ZtMijef
- RLDM version, *Using Per-Factor Empowerment to Control Specific State Variables* —
  https://camallen.net/files/focused_skill_discovery_rldm.pdf
- Context on MI-skill-discovery coverage limits: https://arxiv.org/html/2506.14420 ·
  https://iclr.cc/virtual/2022/7448
