# SOC & power-law dynamics (live review): **allometric sublinear activity–size scaling** — the one criticality signature that lives ACROSS system sizes, and why our board tape cannot yet carry it

**Date:** 2026-08-17
**Area:** self-organizing criticality & power-law dynamics, from the angle of a RECENT result (2023–2026).
**Landing:** a mechanism we do NOT embody — **avalanche criticality NECESSARILY implies a sublinear
activity–size law** (Simões, Andrade Jr., Herrmann, Zapperi & de Arcangelis, *Allometric scaling of brain
activity explained by avalanche criticality*, arXiv:2512.10834, 11 Dec 2025; J. R. Soc. Interface
**23**(238):20251192, May 2026). Every one of `mesh-criticality`'s fourteen lenses measures the SHAPE of
the event stream **at one fixed system size**. This one is a **cross-size** necessary condition, and it is
structurally absent from the tool.
**Verdict:** concept ACCEPTED as new and load-bearing; the naive implementation is **DISCARDED with a
measured artifact** (the exponent is not identifiable from the board tape — measured below, twice); the
embodiable form is a `--allometry` sidecar on `scripts/mesh-criticality` whose **first job is to make the
size axis exist**. **LANDED as code** (uncommitted, for the steward) — see *What shipped* at the end.

---

## What this area already holds (checked BEFORE searching, per the AREA-MINED discipline)

`~/.mesh/knowledge/review-self-organized-criticality-AREA-MINED-frontier-2026-07-02.md` declares this the
most heavily mined literature area tied to one file, and it is right. Checked and excluded as already
reviewed, shipped, or explicitly rejected:

| Concept | Status |
|---|---|
| Branching ratio m̂ (MR estimator, Wilting–Priesemann) | the tool's baseline |
| Avalanche shape / crackling exponent relation / CECP / dynamic range / susceptibility | `--shape` `--crackling` `--complexity` `--dynrange` `--suscept` |
| Coherent-noise (exogenous) null · record dynamics (aging) null | `--coherent` · `--aging` |
| Safety margin (reverberating regime) · DFA 1/f · coarse-graining recovery · noise-confound DTC | `--margin` `--hurst` `--coarse` `--dtc` |
| Griffiths phase / stretched criticality (incl. arXiv:2512.03409) | knowledge base, 2026-06-20, not embodied |
| Multicriticality · SOqC · dragon-kings · self-tuning · CSD · observer effect · small-sample CI · Clauset GoF | knowledge base, reviewed/shipped/honestly rejected |
| **Complexity matching (DFA/MFDFA exponent correlation)** | reviewed **and discarded** 2026-07-30 as hollow on our windows |

Two live-search candidates were killed against that table before landing here:

- **Complexity synchronization** (Mahmoodi, Kerick, Franaszczuk, Boothe, Grigolini & West, arXiv:2606.10948,
  9 Jun 2026) — `corr(δ_a(t), δ_b(t))` between windowed MDEA/DFA scaling exponents, offered as a *control*
  principle (it ranks intervention targets). **Rejected:** it is the complexity-matching family we already
  discarded, and its own implementation uses a **10⁴-sample sliding window**; `mesh-cooscillate` runs on
  `MIN_OVERLAP=8` deltas. The control claim rides on an exponent we cannot estimate without hallucinating it
  (the crypticity precedent).
- **Edge of ergodicity breaking** (Lesmana, Feng, Chen & Lai, arXiv:2604.15669, 17 Apr 2026) — the attractor
  is the ergodic/non-ergodic *boundary* (ergodicity coefficient ε = median pairwise total-variation distance
  across run realizations, 0<ε<1 at the edge), not a critical point. **Rejected:** ε needs independent
  *replicas of the same system*; the mesh has one realization, and the healthy-set-point-is-not-the-knife-edge
  content is already `--margin` + the SOqC review. Non-ergodicity itself is
  `~/.mesh/knowledge/review-non-ergodicity-ruin-repeated-shed-2026-06-21.md`.

## The concept, and where I found it

> **Any system governed by critical avalanches must show a SUBLINEAR activity–size relation.**

Simões et al. derive the allometry analytically from avalanche statistics alone: at criticality the
avalanche-size distribution carries a finite-size cutoff `S_c ~ N^D`, so the mean avalanche size
`⟨S⟩ ~ N^{D(2−τ)}`, and with a size-independent per-unit initiation rate the **total** activity goes as
`A ~ N^θ` with **θ < 1** — per-unit activity *falls* as the system grows. They verify it in
integrate-and-fire networks at criticality **and** in classical SOC models (so it is generic, not
model-specific), and the predicted exponents match measured firing rates across mammal species — which is
why larger brains fire disproportionately slower (a Kleiber-like economy of scale that needs no separate
biological story).

Sources (live, 2026-08-17):
- [arXiv:2512.10834 — *Allometric scaling of brain activity explained by avalanche criticality*](https://arxiv.org/abs/2512.10834)
- [J. R. Soc. Interface 23(238):20251192](https://royalsocietypublishing.org/rsif/article/23/238/20251192/481766/Allometric-scaling-of-brain-activity-explained-by)
- [arXiv:2606.10948 — *Complexity synchronization…*](https://arxiv.org/html/2606.10948) (checked, rejected above)
- [arXiv:2604.15669 — *Self-Organization to the Edge of Ergodicity Breaking…*](https://arxiv.org/abs/2604.15669) (checked, rejected above)
- [arXiv:2512.03409 — *Optimal Griffiths Phase in Heterogeneous Human Brain Networks*](https://arxiv.org/pdf/2512.03409) (already cited in our Griffiths note)

## Why it is genuinely new to us

Every lens in `scripts/mesh-criticality` is computed **at one size**. `--coarse` sweeps the *temporal* bin
`k·Δt`; nothing sweeps the number of *units*. That matters because the allometric law is an
**independent necessary condition**: a board can emit a clean power-law avalanche distribution at fixed size
while its activity scales **linearly** with the number of sources — and linear scaling falsifies avalanche
criticality as the mechanism, because independent sources that never share a cascade budget simply add up.
It is the same class of move as `--crackling` (a coherence test a lone power law cannot fake), but along the
one axis we have never looked down.

It also carries an operational forecast the mesh cares about: **if the board is critical, wiring more
reflexes buys economy of scale (sublinear board traffic); if it is linear, every reflex we add contributes
its own independent noise floor and the board floods as the genome grows.** The genome has grown
**26 → 287** cadence-carrying reflexes since 2026-06-17 (measured: `git grep -lE '^# reflex-cadence:'`
across history), so this is a prediction with money on it.

## The measurement I actually ran (the artifact, not a claim)

Board tape `~/.mesh/chat.log`, 137 hourly bins, source = the `who@node` field.

| Size axis | n | fitted θ (log A ~ θ·log N) | 95% CI |
|---|---|---|---|
| **Endogenous** — distinct posters observed in the hour | 121 | **1.220** | [1.175, 1.264] |
| Endogenous, **hour-of-day demeaned** | 121 | **1.235** | [1.188, 1.283] |
| **Exogenous** — live minds prompted per roll-call round (`~/.mesh/roll-call.log`), joined by hour | 19 | **3.651** | [2.053, 5.250] |

All three are **superlinear** — the opposite of the critical prediction — and none of them is a verdict:

1. **The endogenous axis is structurally confounded.** N is counted *from the same events* as A, so an idle
   hour has few posters and few events by construction while a busy hour saturates the roster and keeps
   emitting → the bias pushes θ **up**. Useful asymmetry: this makes the test **one-sided** — a θ<1 reading
   would be conservative and meaningful, θ>1 says nothing.
2. **De-clocking does not rescue it.** Demeaning by hour-of-day moved θ from 1.220 to 1.235 — i.e. the
   confound here is the shared counting, **not** the operator's day. (I expected the sun and was wrong;
   the number says so.)
3. **The exogenous axis is real but tiny.** Roll-call's prompted-mind count is measured from tmux, not from
   the board, so it is genuinely independent — but it only ever ranges **11–18** (1.6×), and its overlap
   with the surviving board tape is **19 hours**, because `chat.log` is evicted at 3000 lines (~6 days).
   θ=3.65±0.82 on n=19 is noise with a decimal point.
4. **There is no long baseline to fall back on.** Every activity tape on this node begins **2026-07-14**
   (the mind-migration), over which the reflex count moved only 214 → 287 (1.34×). The 11× size sweep and
   the activity record do not overlap.

**So: the allometric exponent is not identifiable on this node's tapes today.** Not "the mesh is not
critical" — *the measurement cannot be made yet*, which is a different sentence and the only honest one.

## Application — `scripts/mesh-criticality`, a `--allometry` sidecar (LANDED)

The gap is not an algorithm, it is that **nobody has ever recorded the (size, activity) pair**, so the axis
has no range to fit. The sidecar's first duty is therefore to *create* the axis:

1. **Accumulate.** On each run, append one daily row to `~/.mesh/criticality-allometry.log`:
   `<date> N_reflex=<count of scripts/ with '# reflex-cadence:'> N_minds=<roll-call roster> A=<board events>`.
   Cheap, exogenous on both size columns, and it survives `chat.log` eviction — which is precisely what
   killed the fit above. Two months of this and the reflex axis alone spans a real decade.
2. **Report, never alarm.** `--allometry` fits log A ~ θ·log N on the accumulated ledger and prints
   `SUBLINEAR-ALLOMETRIC` (θ CI wholly < 1 → consistent with avalanche criticality, and conservative given
   the bias direction) / `LINEAR-OR-SUPERLINEAR` / **`INSUFFICIENT`** until the ledger holds ≥60 rows AND the
   N range spans ≥2×. Read-only sidecar, exactly like `--shape`/`--margin`/`--aging`; no `[alert]`, no
   consumer, no cron alarm.
3. **Never fit the endogenous axis.** Distinct-posters-per-window must not be offered as a size column —
   measured above, it is confounded by construction and reads 1.22 on a tape we have no reason to think is
   linear. If it is ever printed, it is printed as a diagnostic labelled with its bias direction.
4. **RED-first `--test`.** Synthesize two event streams of known θ (θ=1.0 independent superposition; θ=0.6
   sublinear) over a decade of N, assert the classifier labels each correctly and that a 1.3× N range
   returns `INSUFFICIENT` rather than a number. Break the fit, watch it go RED, restore. (The
   `INSUFFICIENT` leg is the load-bearing one — the whole finding above is that a narrow range mints a
   confident wrong exponent.)

## What shipped (uncommitted in the tree — `scripts/mesh-criticality`, +261 lines)

- `allom_reflex_count()` · `allom_append()` · `allom_read()` · `allometry_fit()` — the exogenous size
  column, the once-per-UTC-date ledger, and the CI-vs-1 verdict.
- `--allometry` mode, placed **above** the thin-tape early-exit (it reads the ledger, not the current
  window, so a quiet board must not turn it into `UNKNOWN`).
- One row per UTC date appended from the `--watch` reflex (already cron-wired `7-59/30 * * * *`), gated on
  the same `CRIT_ALARM_BOARD` test-vs-live signal `crit_presync` uses, with `CRIT_ALLOM_LOG` as the
  explicit sandbox. A `--test` that appended to the real ledger would forge the rows the fit exists to read.
- `--test` legs, each **seen RED** from a scratch-copy mutant before being trusted:
  | mutant | leg that caught it |
  |---|---|
  | range gate deleted | `1.30x N range must REFUSE, got INDETERMINATE` — and the fixture is checked *ungated* too, so the leg proves the **gate** refuses, not the data |
  | CI replaced by the point estimate | `the θ=1.0 null must NEVER read SUBLINEAR, got θ=0.982 CI[0.934,1.031]` |
  | unreadable genome returns `0` not `None` | `must be None, never 0` (a fabricated size anchors the regression) |
  | 8 KB head-read restored | `expect 4, got 3` |
  | `__pycache__` prune deleted | `expect 4, got 5` |
  | `.pyc` suffix filter deleted | `expect 4, got 5` |

**Two bugs the build surfaced that the review had not predicted:**

1. **A prefix read is not a file scan.** The first cut read 8 KB per tool and counted **282** where the
   truth is **287** — `mesh-algedonic`, `mesh-promises` and `mesh-criticality` itself carry the
   `# reflex-cadence:` header at bytes 19049 / 13944 / 33368. Worse than the undercount: the size axis
   would have *moved* whenever a doc header grew past the cutoff — motion with no size behind it, in the
   one column whose whole job is to be exogenous.
2. **Two guards, one fixture, one of them vacuous.** The `__pycache__` exclusion and the `.pyc` suffix
   filter both looked tested; deleting either stayed green, because the single `__pycache__/mesh-a.pyc`
   fixture tripped whichever guard ran first. Each now has a fixture only it catches (a suffixless file
   inside the cache dir, and a stray `.pyc` outside it) and each has been seen RED alone.

Live reads after landing: `--allometry` → `INSUFFICIENT (rows=0 < 60, N_reflex now=287)`; a sandboxed
`--watch` against the real board wrote `2026-08-17 N_reflex=282 A_per_h=38.4167 win_h=12.00 events=461`
and a second run the same day left it at one row. The real ledger is still absent — nothing but a landed
`--watch` will create it.

**Horizon.** Re-read `~/.mesh/criticality-allometry.log` at **2026-10-17** and state the θ CI, whatever it
says. A prediction nobody returns to is not a prediction. Note the ledger only starts accruing once the
steward lands this and `mesh-sync-tools` deploys it — until then the deployed `--watch` writes nothing.

## Discarded alternatives from the same read (one line each)

- **Complexity synchronization (arXiv:2606.10948)** — needs 10⁴-sample windows; we have 8-delta overlaps, and the exponent family was already discarded as hollow here.
- **Edge of ergodicity breaking (arXiv:2604.15669)** — its ε needs independent replicas of the same system; the mesh has one realization and one history.
- **Symmetry emergence in SOC (arXiv:2608.13500, Aug 2026)** — a scaling limit of the sandpile toppling function; beautiful, and there is no mesh observable that corresponds to a toppling density field.

## Doctrine this touches

- *A sample is not the interval* / *a sense's coverage is window ÷ cadence* — the same family: here the
  **size range** is the coverage, and a 1.34× range cannot resolve a sublinear exponent.
- *A covariate sampled after the effect absorbs it* — the endogenous size axis in one line.
- *A forward-looking metric must be published at horizon close* — binds the ledger above.
- *A gate you have not seen FAIL is not a gate* — hence the RED-first `INSUFFICIENT` leg.
