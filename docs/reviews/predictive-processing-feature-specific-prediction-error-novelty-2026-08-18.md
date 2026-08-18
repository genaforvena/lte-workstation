# Live literature review — predictive processing & the Bayesian brain

**Area:** predictive processing / Bayesian brain · **Angle:** a RECENT result (2023–2026) — what is new right now
**Date:** 2026-08-18 · **Channel:** genome · **Organ:** `scripts/mesh-novelty` (new report-only mode `--features`)
**Status:** uncommitted in tree, steward lands

---

## The concept we did not embody

**Feature-specific prediction error — surprise has a LEVEL, and one scalar cannot carry two.**

The field's live result: a prediction error is not a magnitude on one axis. *Which* feature was
violated is an axis of its own, and the level that reports the error is **not** the level that
computed it.

> **"A stimulus may be both predicted and surprising, depending on the specific features."**
> — Richter, Uran, Vinck & de Lange (2025)

Sources, all read this session:

| Paper | Where | What it establishes |
|---|---|---|
| **Richter D, Uran C, Vinck M, de Lange FP — "Feature-specific predictive processing: What's in a prediction error?"** | *Imaging Neuroscience* (MIT Press), **2025-12-18**, [doi:10.1162/IMAG.a.1061](https://doi.org/10.1162/IMAG.a.1061) · open at [PMC12715616](https://pmc.ncbi.nlm.nih.gov/articles/PMC12715616/) | The live review. Prediction errors *even in V1* track **high-level** (object-identity) surprise and **not** low-level (orientation/contrast) surprise — inverting the area's own tuning. Cites: **Richter et al. 2024** (fMRI — "all visual areas from early occipital to higher-order ventral regions, including V1, were upregulated as a function of high-level, but not low-level, surprise"); **Richter et al. 2025** (EEG — that modulation lands **<200 ms** post-onset, parieto-occipital); **Heilbron & de Lange 2025** (mouse V1, strongest in **superficial layers**); **Uran et al. 2022** (macaque — in ONE area the two levels ride **different observables**: firing rate ← high-level predictability, narrow-band **gamma 30–80 Hz** ← low-level). Their idiom for why the high level is the behaviourally relevant one *and* the easier to predict: **"rain vs individual drops of rain."** Four candidate mechanisms listed; **dendritic HPC** (basal = feedforward error, apical = high-level mismatch) is the one that explains the rate/gamma split. |
| **Westerberg JA et al. — "Hierarchical interactions between sensory cortices defy predictive coding"** | *Trends Cogn Sci* **2026;30(2):110-123**, [doi:10.1016/j.tics.2025.09.018](https://doi.org/10.1016/j.tics.2025.09.018) · [PubMed 41120233](https://pubmed.ncbi.nlm.nih.gov/41120233/) | The same month's dissent, landing on the same operational point from the opposite direction: feedback **enhances** the predicted representation rather than suppressing it, and repetition effects are feedforward adaptation. Umbrella alternative: BELIEF. |
| **Gabhart, Xiong & Bastos — "Predictive coding: a more cognitive process than we thought?"** | *Trends Cogn Sci* 2025, [PMC12821738](https://pmc.ncbi.nlm.nih.gov/articles/PMC12821738/) | Read and **set aside as already embodied** — local vs global oddball is `mesh-novelty --levels` (2026-07-27). |

Both live papers converge on one operational sentence: **the magnitude of a response does not name
which feature was violated.**

**Prior coverage checked** (none of it is this): Bayesian surprise vs Shannon (07-28) · Bayesian
model reduction (07-28) · circular inference (07-28) · conformal coverage (08-04) · model recovery
(08-04) · genuine-MMN matched control (08-03) · local–global two-timescale (07-27) · corollary
discharge (08-14) · omission / learned WHEN (08-15) · metacognitive type-2 sensitivity (08-17) ·
EFE ambiguity (08-17) · interoceptive precision allocation (08-15). Every one of them scores
**bits on one alphabet**. None asks *which feature*.

---

## The measured bite on this node

`scripts/mesh-novelty` is the mesh's surprise organ and its wake gate ("wake on HIGH novelty, stay
silent on routine"). Every mode in it — marginal, `--conditional`, `--bayesian`, `--levels`,
`--territory`, `--progress`, `--tempering`, `--when`, `--control` — draws its events from **one**
function:

```python
def event_type(line):
    """Coarse event signature: the bracket tag, else a generic class."""
```

That is a single feature, and specifically a **LOW** one: the surface form of the token. Decomposing
the same board into three levels, each scored against its **own** baseline (`~/.mesh/chat.log`,
3000 lines, 2026-08-18):

| level | what it is | alphabet | H |
|---|---|---|---|
| `form` | the literal marker as typed — **what `event_type()` sees** | 101 | 4.62 b |
| `actor` | the emitting window/organ | 87 | 5.19 b |
| `role` | the board grammar `mesh-promises` already parses (`task\|taking\|done\|verify\|fyi`, + `sense` for every organ marker outside it) — the **coarse** level | 6 | 1.60 b |

```
pairwise r over the last 600 events:   r(form,role) = -0.41   r(actor,role) = +0.02   r(form,actor) = +0.49
top decile K=60, a LOW gate vs a HIGH gate:
    overlap                                                        1 / 60
    form-top sitting at the role axis FLOOR (surface-only)        59 / 60
    role-top sitting below the median form-surprise (invisible)   33 / 60
  form-top: [criticality-signal-lost] [note3-light-raw] [dispatch-noack] [health-ok] [criticality-recovered]
  role-top: done/genome  done/land  task/discover  task/health  done/senses
```

The two axes are not merely non-redundant on this board — they are **anti-correlated**, and
structurally so. The board holds exactly two populations: frequent coordination words (low
form-surprise, high role-surprise) and rare one-off organ markers (the reverse). So the gate that
decides whether to wake a paid mind picks the second population almost exclusively. Its own default
output says so without being asked:

```
🔭 mesh-novelty — recent window mean marginal surprise: 3.31 bits (routine)
── most surprising recent events ──
   7.3b [ambient-clock]  … NIGHT-QUIET
   6.5b [media-scene]    … scene=QUIET
   5.3b [genome-strand]  … phaedra: DIVERGED
   4.8b [note]           … access change: phone: BLIND
```

Three of those four are an organ saying a routine thing in a rare word. Meanwhile a `[taking]` with
no matching task, or a `[done]` from a window that rarely closes — the claim grammar, exactly where
`mesh-promises` finds leaked promises — sits at 0.66 on the axis the gate reads. **The mesh wakes on
drops of rain.**

This is the same shape as the doctrine's *"check what your ranker SELECTS FOR, not just that it
ranks"*, one level up: there the top tail of a score inverted the intent; here the whole **axis** is
the wrong feature, and no amount of re-ranking on it recovers the other one.

---

## The fix (report-only, in tree)

`scripts/mesh-novelty --features` (+ `--json`). Decomposes each recent event into `form / actor /
role`, scores each against its own baseline, and reports **where the levels disagree** — per-event
dominance and spread, the pairwise correlations, and the low-gate-vs-high-gate top-decile
disagreement above.

```
novelty-features (Richter/Uran/Vinck/de Lange, Imaging Neuroscience 2025-12-18 …; report-only):
  levels (each with its OWN baseline over 2960 lines): form 101 types H=4.62b · actor 87 types H=5.19b · role 6 types H=1.60b
  do the levels agree? r(form~actor)=+0.49 · r(form~role)=-0.41 · r(actor~role)=+0.02   (over the last 600 events)
  a LOW gate vs a HIGH gate, top decile K=60: overlap 1/60 · 59/60 of the form-top sit at the role axis FLOOR …
  most level-divergent of the last 40:
    [task                  ] job    form  0.99 actor  1.03 role  2.82  → ROLE-dominant (spread 1.83)
    [done                  ] sound  form  0.66 actor  1.13 role  1.86  → ROLE-dominant (spread 1.21)
```

**Normalization, stated in the tool itself because it is otherwise a trick.** For a marker inside the
grammar, `form` and `role` are the *same event*, so the raw bits are near-identical (`done` = 3.03 b
as a form, 2.98 b as a role — they differ only by each level's smoothing denominator). Each level is
divided by **its own** baseline entropy, so a dominance verdict names a **level**, not more bits.
Self-calibrating against the live corpus, never an assumed 0..1.

**What it does NOT do.** It adds no gate: `mean_bits`, `--threshold` and `--edge` are untouched, and
`analyse()` pays nothing unless the flag is passed. Whether the wake gate should move to the `role`
axis is a behavioural change to a spend signal and is the steward's/operator's call — the instrument
comes first. Honest n/a: under `MESH_NOVELTY_FEAT_MIN` (60) baseline lines it prints `n/a` and exits
**2**, never a "the levels agree".

**Gates (`--test`, F1–F7), seen RED then green.** F1 a never-seen marker from the commonest role is
FORM-dominant · F2 a common marker doing a rare act is ROLE-dominant · **F3 the mutation gate**:
`[done]`'s *raw* surprisal is HIGHER on `form` than on `role` — the opposite of the verdict — so F2
can only pass because each level is divided by its own entropy · F4 the levels are measurably
non-redundant (r < 0 on the fixture) · F5 the two gates pick different events · F6 an unremarkable
event is flat on every level (the axis is not always-on) · F7 too little board renders `None`.

Three mutants run from a scratch copy, each red on the leg that owns it:

| mutant | result |
|---|---|
| drop `/H` in `nb()` (no per-level normalization) | **F2, F3 RED** — dominance inverts to `form` |
| `role = form.lower()` (collapse the levels) | **F1, F2, F3, F4, F5, F6 RED** — r = 1.0 |
| `len(ev) < 0` (n/a can never fire) | **F7 RED** |

---

## What is still open (not claimed)

- The paper's sharpest structural claim — **one area, two observables, two levels** (V1 firing rate ←
  high-level, gamma ← low-level; the dendritic-HPC account) — has an obvious mesh reading: a single
  organ should publish its low- and high-level surprise on **separate channels** rather than folding
  them. `--features` measures the two; it does not yet split any organ's emission.
- `role` is derived from the board grammar `mesh-promises` parses. That is a documented, load-bearing
  schema rather than a fresh hand-roster — but it is still a list of names, and *a sweeper is only as
  good as the names it knows*. A marker outside it reads as `sense` by default, which is right today
  and would silently mis-file a new grammar word.
- Every figure here is **today's answer**: `chat.log` is a sliding window, so the alphabets, entropies
  and correlations turn over. The CLAIM is the gate; re-derive the numbers, never quote them.
