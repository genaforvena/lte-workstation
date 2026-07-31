# Deleuze & Guattari — double articulation (content plane vs expression plane) → `mesh-sensorium --articulation`

**Live literature review · cross-domain transfer to a distributed sensor mesh · 2026-07-31 · genome (mesh-home)**

## The concept we had not embodied

Every assemblage, for Deleuze & Guattari, is **doubly articulated** — a term they take from the
linguist Louis Hjelmslev. There are two articulations, each with its own *form* and *substance*:

- a first articulation on the **plane of content** — the "machinic assemblage of bodies": matter
  actually coupled and formed (in ATP's geological example, sediment being deposited);
- a second on the **plane of expression** — the "collective assemblage of enunciation": the regime
  of *signs* attributed to those bodies (the sedimentary rock's folding, the statement made *about* it).

The load-bearing claim — and the reason this is worth a metric — is that **the two articulations are
relatively independent and their relation is *not causal*.** They are held together only in *reciprocal
presupposition* ("there is a continual passage from one to the other" — but no guarantee). Nothing in
the form of the expression forces it to track the form of the content; a sign can keep being emitted
after the body it names has stopped producing, and a body can keep producing while its sign is dropped.

That is, almost word-for-word, the mesh's own **hollow-sense** failure class stated at the level of a
general principle: *the sign is not the read*. The mesh has fixed instances of it organ-by-organ
(state-touch, exit-2-organ-absent, real-read gates, "executable and loadable are different claims").
It did **not** have a cross-organ metric that reads the *two planes as two artifacts* and checks whether
they are still in reciprocal presupposition.

### Where I found it / citation

- **Deleuze & Guattari, *A Thousand Plateaus* (1980)** — "10,000 BC: The Geology of Morals" (double
  articulation; the form/substance of content vs expression) and the *tetravalence of the assemblage*
  (machinic assemblage of bodies ↔ collective assemblage of enunciation). Via **Hjelmslev, *Prolegomena
  to a Theory of Language***.
- Verified as current, live scholarship on the **Purdue Deleuze dictionary** (deleuze.cla.purdue.edu,
  "the double articulation characterizing a language system") and the assemblage encyclopedia entry
  (2025–26): both restate the *non-causal independence* of content and expression.
- **Live, continuously-published cross-domain transfer of double articulation into sensor/signal
  time-series:** Taniguchi et al., *"Nonparametric Bayesian Double Articulation Analyzer for Direct
  Language Acquisition from Continuous Speech Signals"* (arXiv:1506.06646; IEEE TASLP 24(9), 2016), and
  the Kyoto **Symbol Emergence Systems Group**'s ongoing work (2024–25,
  ses.ist.i.kyoto-u.ac.jp/publication; e.g. "Time-series Segmentation and Symbol Emergence", 2025).
  This confirms double articulation is an *active* concept in sensing research, not a period-piece.

  **Honest distinction (why I did not copy their mechanism):** Taniguchi's Double Articulation Analyzer
  operationalizes the **linguistic** (Martinet/Hjelmslev) reading — unsupervised *two-layer segmentation
  of a signal* (latent letters → latent words) via a sticky HDP-HMM + NPYLM. That is a heavy
  nonparametric-Bayesian pipeline, **not** a mesh-scale shell analyzer, and building it would be exactly
  the kind of over-claim the verification principle forbids. What I transfer is the **assemblage** reading
  — content-plane vs expression-plane *reciprocal presupposition* — which is a cheap `stat` read.

## Why it is distinct from what we already have

`mesh-sensorium` already carries four assemblage/RR axes, and one of them is close enough to require care:

| axis | plane(s) read | catches |
|---|---|---|
| `--balance` | `.state` cache (expression) only | depth / redundancy per percept-category |
| `--degeneracy` | `.state` cache only | whether that redundancy is structurally distinct (common-mode) |
| `--exteriority` | `.state` cache only | consumer fan-out (detachability) |
| `--impasse` | `.state` cache only, vs the clock | a live sign whose **value is `?`** (hollow-by-unresolved-value) |
| **`--articulation`** (new) | **LOG (content) *and* `.state` (expression), against each other** | a sign that fell out of reciprocal presupposition with a **live** content plane |

`--impasse` is the nearest neighbour, and it is genuinely different: it reads a **single plane** (the
`.state` cache) and fires only when the value renders as `?`. `--articulation` is the **first two-plane
check** in the organ. It catches exactly the quadrant `--impasse` cannot see: a sense that is *actively
writing content* (its reading LOG is fresh) whose **sign** (`.state`) has gone stale — the value there is
perfectly valid, **not `?`**, so `--impasse` is silent and `--balance` happily counts the stale sign as a
live stream. That is the mesh's own **driver-races-the-cache** failure (`mesh-mag`/`mesh-gyro` raced the
`-n 1` driver, 5 days stale, `--test` green) re-described as an articulation break: the body still
couples, but the sign the mesh acts on no longer presupposes it.

## The mechanism

For each **paired** sense — one that keeps *both* a current-value `.state` cache (**expression**) and an
append-only reading LOG (**content**) — age each artifact against the sense's `--cached` staleness limit
and classify:

- **ARTICULATED** — both planes fresh (sign presupposes live content).
- **MUTE** ⚠ — content LOG fresh, `.state` stale → *a live sense the sensorium/pane is blind to* (the fault).
- **SIGN-AHEAD** — `.state` fresh, LOG stale → **deliberately not faulted.**
- **DORMANT** — both quiet (a liveness / reflex-health concern, not articulation).
- **UNPAIRED** — only one plane present (reciprocal presupposition not assessable).

Posture: `DECOUPLED` (exit 3) if any MUTE, else `coupled` (exit 0), `NO PAIRS` (exit 2).

### The calibration boundary that makes it honest

The **SIGN-AHEAD** direction (fresh sign, stale content log) is the mesh's own **liveness-touch** shape:
`mtime = liveness`, `content = change-gated write` (CLAUDE.md; `mesh-state-touch`). Faulting it would
re-break precisely the false-STALE bug state-touch exists to prevent. So `--articulation` is
*asymmetric on purpose*: it faults only content-leads-a-stale-sign, never sign-leads-a-quiet-content.
The live read on this node vindicates the boundary — `ambient-clock` shows a **403h**-stale content log
under a fresh sign and is correctly read **SIGN-AHEAD, not MUTE**; without the exemption that one field
would have manufactured a permanent false decoupling.

## Live read (mesh-home, 2026-07-31)

```
  body-power       content=9m   expression=9m    ARTICULATED
  light            content=17m  expression=77s   ARTICULATED
  activity-tempo   content=48m  expression=8m    SIGN-AHEAD
  room-sense       content=3h   expression=4m    SIGN-AHEAD
  ambient-clock    content=403h expression=25s   SIGN-AHEAD
  pairs: 2 articulated · 0 MUTE · 3 sign-ahead · 0 dormant · 0 unpaired  (of 5)
  posture: coupled
```

## Verification

- **Read-only.** No verdict path touched; new flag only; reuses the `--cached` staleness limits.
- **RED-first `--test`** (3 fixtures under a throwaway `$HOME`, real `stat` on crafted mtimes): fresh-log
  / stale-state → **MUTE / DECOUPLED / exit 3**; both fresh → **coupled / exit 0**; fresh-state /
  stale-log → must **not** fault. A single hardcoded verdict passes at most one case.
- **Mutant proven RED:** replacing the expression-staleness check with `sf=1` (sign always fresh) makes
  MUTE unreachable → case 1 fails with `got rc=0: coupled`. Restored → green.

## Files

- `scripts/mesh-sensorium` — new `--articulation` flag + inline literature header + `--test` block
  (genome source; uncommitted, steward lands).
