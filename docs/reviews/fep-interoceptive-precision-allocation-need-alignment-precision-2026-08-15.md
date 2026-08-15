# FEP / active inference — interoceptive precision ALLOCATION: is the mesh's sampling budget need-aligned, and can it move?

**Date:** 2026-08-15 · **Window:** genome · **Landed:** `scripts/mesh-precision --attend` (report-only),
plus two fixes in `scripts/mesh-algedonic` the new mode surfaced. Uncommitted in the tree.

## The source (live literature, not the concept map)

St John Grimbly, Nicolas Kuske, Evert A. Boonstra, Bruce A. Bassett, Charel van Hoof, Rowan Hodson,
Benjamin Rosman, Ryan Smith, Mark Solms & Jonathan P. Shock, **"Interoceptive Attention as Dynamic
Homeostatic Prioritization in a Foraging Agent"**, **arXiv:2608.04232**, submitted **4 Aug 2026**
(found by sorting the arXiv API `all:"active inference"` feed by submission date — 5 papers exist in the
08-01…08-15 window that postdate our last sweep; read: abstract + the allocation/experiment sections of
the v1 HTML).

Verbatim, the mechanism:

> "at each step it reads its own body-state beliefs, identifies the most-needed channel, and reallocates
> a fixed budget of interoceptive precision toward it, so that the same precision-shaped likelihood feeds
> both belief update and planning"

with the rule and the budget constraint stated as

> m\*ₜ = arg maxₘ 𝔼q(sₘ)[needₘ] ,  needₘ(s) = (sₘₐₓ − s)/sₘₐₓ ,  Σₘ κₘ ≤ K,  κₘ ∈ [κ^floor, 1],
> K = 2.60, κ^floor = 0.05

and the three-arm experiment that **measures** it (this is the metric angle the task asked for):

> "this selective allocation more than doubles learning-phase survival at matched budget against a
> uniform-precision agent (0.414 vs 0.199 across 11 layouts, n=32 seeds each, paired cluster-bootstrap
> p ≤ 10⁻⁴)"
> "aiming precision at the least-needed channel does worse than spreading it evenly" (the anti-aligned
> control: identical budget and magnitudes, it "selects the *least*-needed channel")
> "denying the shaped likelihood to the planner alone removes about half of it"

So allocation is not a free axis: **at matched cost there are three distinguishable regimes — aligned,
uniform, anti-aligned — and two of them are worse than the third.**

## What we do NOT embody

Every precision mode in `scripts/mesh-precision` **measures** precision: `--num` its variance, `--bmr`/
`--bme` whether the data warrant a structure change, `--ckm` whether an observable context predicts the
noise, `--reachable` whether an actuator can move that context. **Nothing asks where the mesh SPENDS the
fixed budget that produces precision in the first place.** Grep over `scripts/` + `docs/` for
need-aligned / precision-allocation / attention-budget: zero hits; no `--attend` anywhere.

The mesh has the two objects the paper's rule needs, and has had them all along:

- the **need vector** — `mesh-algedonic`'s noisy-OR panel logs `axes=therm:0.0,hw:0.0,egress:0.0,stress:0.3,crit:?`
  on every 10-minute tick, each axis in [0,1] with 1 = maximal distress. That IS a needₘ, per channel,
  2463 samples deep, with an honest `?` for unknown.
- the **per-channel precision knob** — the SAMPLING CADENCE of the reflex that produces each axis
  ("a sense's coverage is its window over its cadence", CLAUDE.md). It is contended (this node runs three
  llama-servers, whisper and the grinder under PSI stall) and it is **set once at autowire time**.

Need moves; the budget does not. So the mesh is structurally the paper's **fixed-allocation** agent — and
whether that fixed allocation happens to be aligned, flat, or **anti**-aligned had never been measured.

## What landed: `mesh-precision --attend` (report-only)

Reads the need tape (`~/.mesh/algedonic.log`) and the budget (`~/.mesh/reflexes.cron`, axis→producer map
overridable with `--map`), and emits **two verdicts, never folded** (they answer different questions):

- **ALLOC** — cross-channel Spearman ρ(κᵢ, mean needᵢ) over eligible axes, **exact-permutation null** over
  the need labels → `ALIGNED` / `ANTI_ALIGNED` / `ALLOC_FLAT` / `ALLOC_UNSCORABLE(reason)`.
- **TRACK** — how many times the most-needed channel CHANGED, against whether the budget could have
  changed at all → `TRACK_STATIC` / `TRACK_NA` (the ranking never moved — a static budget is not evidence
  either way) / `TRACK_UNKNOWN` (rewired inside the window; historical cadences are **not** reconstructed).

**The transfer's seam, stated because it is load-bearing:** the paper's κ is a *likelihood* precision (how
sharply one observation is trusted); ours is a *sampling rate* (how often an observation exists at all).
Both are "how sharply this channel is estimated out of one fixed pot" and both are what the arg-max rule
allocates — but they are not the same quantity. The mode measures the allocation, never a survival
benefit: 0.414-vs-0.199 is the paper's number, not a prediction about this mesh.

### Three traps found while building it

1. **THE INSTRUMENT'S OWN CEILING — and it binds on the live data.** With *n* eligible channels the
   smallest two-sided p an exact permutation test can produce is (#perms attaining max|ρ|)/n!. At n=4 that
   is 2/24 = 0.083 > α=0.05, so **a PERFECT rank alignment still comes out p > α** — and with a tie in the
   budget (therm and stress both 12/h) the live floor is worse still, **0.167**. Reporting `ALLOC_FLAT`
   there would be the mode saying "not aligned" about data it cannot score. It refuses instead
   (`reason=power-ceiling`) and says what would fix it: one more channel with a *realized* budget (n=5 →
   0.017). Same shape as `--reachable`'s `periodic-null` refusal.
2. **A DECLARED BUDGET IS NOT A SPENT ONE.** An axis whose cron line exists but whose reading is UNKNOWN in
   most samples is excluded from the alignment and named with its coverage. An axis with **no** cron line
   is `UNWIRED` by name and carries `kappa=null`, never 0 — a fabricated allocation would drag ρ.
3. **THE PREFIX TRAP, live in this node's cron.** `mesh-therm-watch.bak.1784868137` is a *different* tool
   sitting in `reflexes.cron` right next to `mesh-therm-watch`; a substring match would have silently
   added its cadence to the therm axis's budget. Producer matching is word-boundary anchored and leg 9g
   pins it (mutant seen red: κ_e 12.0 → 72.0, and the mode still read `ALIGNED`).
   Also: the cron **file mtime is not usable provenance** — `mesh-reflexes`/`mesh-autowire` rewrite
   `reflexes.cron` on their own cadence (measured: its mtime equalled the tape's newest sample *to the
   second*). TRACK uses the per-line `# autowired YYYY-MM-DD` stamp and falls back to mtime only for an
   unstamped line, naming which evidence it used. A hand edit does not restamp — so the stamp is evidence,
   not proof, and the reason line says so.

### Gates

13 legs (9a–9m) inside `mesh-precision --test`, each driving the real path on injected `--log`/`--cron`
fixtures; the paper's three arms are pinned by name (9a ALIGNED with ρ=1 and p≤α asserted, not just the
label · 9b ANTI_ALIGNED · 9c uniform-budget). Suite runs in 2.9 s. **Six mutants seen red**, from a
scratch copy with the exec bit set:

| mutant | leg that caught it |
|---|---|
| producer match loses its word boundary | 9g (.bak sibling counted, κ 12→72, verdict flipped to ALIGNED) |
| power-ceiling refusal removed | 9d (n=4 perfect alignment read ALLOC_FLAT) |
| unrealized axis kept in the alignment set | 9e (10%-coverage axis eligible) |
| stamp evidence removed (mtime only) | 9i (fixture cron mtime is *now* → TRACK_UNKNOWN) |
| unmapped axis given κ=0.0 | 9m — **this one was green until 9m was written**: the first five mutants all passed it |
| unwired axis given κ=0.0 | 9f |

## Two fixes the mode surfaced in `scripts/mesh-algedonic` — they are ONE bug

`--attend`'s first live run reported the `crit` axis at **0% coverage over 2463 samples**: 2/h of budget
declared, nothing realized, ever.

1. **The tape name.** `pain_crit()` read `~/.mesh/criticality.log`; autowire's cron writes
   `~/.mesh/criticality.cron.log`. Nothing on this node creates the former, so the axis rendered UNKNOWN on
   **every** sample and the viability panel has been running `known=4/5` for the whole log. The identical
   split was already found and fixed *inside* `mesh-criticality` (its `csd_tape_path()`, "six code paths
   used the other one") — **the sweep never reached this reader** ([[a-format-fix-must-sweep-every-reader]]).
   The `--test` stayed green throughout because its fixture writes the name the reader wants
   ([[a-fixture-driven-gate-cannot-cover-the-live-path]]). Now resolves to the tape that EXISTS, autowire's
   name first, `MESH_ALGEDONIC_CRIT_TAPE` overrides.
2. **The second suppression tier — and without it the path fix would have been WORSE than the blindness.**
   `mesh-criticality` routes a SUPERCRITICAL three ways: ALARM (real runaway → board), HELD (meta-dominated
   chatter → suppressed), **TRACE** (density-only throughput, "explicitly NOT a runaway" → durable tier,
   kept off the board). `pain_crit()` respected HELD and had no arm for TRACE. Its own live oracle, in its
   own header: *"24 of 24 SUPERCRITICAL ticks on this node were ALARM-TRACED, ZERO took the ALARM route."*
   So turning the axis back on with only the HELD arm would have injected **crit:0.9** into the global
   viability panel for every excursion the producer had already decided is not one. Respecting a producer's
   gate means respecting **all** of its suppression tiers, not the first one someone happened to read.

Both gated in `mesh-algedonic --test` (3c drives the autowired tape name with the old name absent; 3d
pins a TRACED supercritical at 0.15/NOMINAL), both mutants seen red.

## LIVE reading (mesh-home, 2463 samples ≈ 17 d)

```
precision[attend]: ALLOC_UNSCORABLE / TRACK_STATIC
  stress  need 0.363  12.00/h  100% cov      <- most-needed, 26.1% of the budget
  egress  need 0.054  20.00/h   89% cov      <- richest,     43.5% of the budget
  hw      need 0.007   2.00/h   99% cov
  therm   need 0.000  12.00/h  100% cov
  rho=0.316 p=0.500 (p_min attainable 0.167 > alpha 0.050 — 4 channels cannot score their own allocation)
  reason=power-ceiling
  30 change(s) of the most-needed channel met an unchanged budget (every eligible axis's cron line
  stamped autowired <= 2026-07-14, before the window opened)
  unrealized(excluded)=crit:0% cov
```

Read carefully, three separate findings:

- **ALLOC is UNSCORABLE, not FLAT.** The honest answer is that with four channels — one of them tied with
  another on cadence — this mesh **cannot score its own allocation** at α=0.05. ρ=0.316 is descriptive
  only. The blocker is precisely the dead 5th channel: with `crit` realized, n=5 and the floor drops to
  0.017. The fix above is therefore not a side-quest — it is what makes the question answerable, and the
  next `--attend` run after `crit` starts resolving is the one that gets a verdict.
- **The allocation is at least not obviously need-shaped.** The most-needed axis (stress, mean 0.363, 46×
  the next) holds 26% of the budget while the least-needed-but-richest (egress, 0.054) holds 43%. Not a
  claim of anti-alignment — that is exactly what is unscorable — but it is the arrangement the paper's
  control arm warns about, and it is worth looking at directly.
- **TRACK_STATIC is unambiguous and needs no null.** The most-needed channel changed **30 times** over the
  window; the budget has not moved since 2026-07-14. Whatever the alignment turns out to be, it is a
  *fixed* one — the paper's dynamic prioritization has no counterpart here.

## Deferred as code (deliberately)

Making cadence need-responsive — the actual reallocation — is **not** landed and should not be landed off
this review. It edits `reflexes.cron`, i.e. the scheduler, on a node where the sampling budget is genuinely
contended; and the measurement that would justify it is currently UNSCORABLE by its own admission. The
order is: fix the dead channel (done, in the tree) → let `crit` accumulate → re-run `--attend` for a real
ALLOC verdict → only then discuss whether anything should move. Report-only until then; the mode weights
nothing, gates nothing, reallocates nothing.

## Files

- `scripts/mesh-precision` — new `--attend` mode + legs 9a–9m in `--test`; usage line extended.
- `scripts/mesh-algedonic` — `crit_tape()` resolver + the ALARM-TRACED suppression arm; legs 3c/3d.
