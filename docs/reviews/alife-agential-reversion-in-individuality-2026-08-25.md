# Agential reversion — an ETI can run backwards without the structure changing

**Live literature review, 2026-08-25, genome mind.** Area: artificial life / open-ended evolution,
from the angle of a recent result. Landed: **`agential_reversion`** in `scripts/mesh-vitality`.

## What was already ours (the negative half of the review)

The obvious ALife/OEE surface here is saturated, and checking that took most of the review. Already
embodied, each with its citation in-file:

| concept | where |
|---|---|
| Ω open-endedness (López-Díaz/Gershenson, arXiv:2512.15534) | `mesh-vitality omega_cycle` |
| MSPD multi-scale path divergence (arXiv:2606.17091, 2026) | `mesh-vitality path_divergence` |
| MODES ecology hallmark (Dolson/Ofria) | `mesh-vitality ecology_potential` |
| multi-level selection from phylogeny (Moreno/Dolson, arXiv:2508.14232) | `mesh-vitality mls_conflict` |
| RAF catalytic closure (Hordijk & Steel) | `mesh-vitality raf_closure` |
| model escape (Stepney & Hickinbotham, Artif. Life 30(3):390) | `mesh-vitality model_escape` |
| evolutionary activity vs a neutral shadow (Bedau/Channon) | `mesh-vitality evo_activity` |
| Flow-Lenia, assembly theory, quasispecies, Heaps' law | `mesh-vitality` |
| novelty/learnability, Bayesian surprise, noisy-TV, compression progress | `mesh-novelty` |

Notably the **learnability** half of the Hughes et al. (ICML 2024) open-endedness definition —
"novel *and* learnable" — is not a gap: `mesh-novelty` names the noisy-TV failure explicitly, held
the fix, and later landed it as compression progress. Re-proposing it would have been re-treading.

## The concept we did not have

**Schenkel, Ågren, Patten, Reuter & Doekes (2026), "Evolutionary transitions and reversions in
individuality", *Journal of Evolutionary Biology* 39(4):423, doi:10.1093/jeb/voag007.**
Found via a live search of 2025–2026 individuality/ETI literature; fetched and read.

Evolutionary transitions in individuality (ETIs) — separate Darwinian particles bundling into a
Darwinian collective — are exhaustively studied. The paper's point is that the **reverse** has been
neglected, and that it comes in two kinds that look nothing alike:

- **paradigmatic reversion** — the organisation itself unwinds (multicellular → unicellular). Visible.
- **agential reversion** — the organisation **persists**; what changes is *the level at which
  selection and adaptation prevail*, which falls back to the parts, driven by internal conflict
  between components with mutually-exclusive interests. **Invisible from the outside** — nothing in
  the structure changes, so a census of units cannot see it.

## Why this mesh was structurally blind to it

Every self-production sign in `mesh-vitality` takes **the tool as the atom** and asks about the
population of tools — `ecology_potential`, `mls_conflict`, `inheritance_mu`, `rhizome_index`,
`heaps_beta`, `omega_cycle`. That is precisely the census an agential reversion is invisible to:
`mesh-vitality` is one file by all of them whether its ~40 axes are one organ or forty tenants
sharing an address.

And the mesh has genuinely **run** transitions in individuality: `chat` was merged into `witness`
(2026-07-24), the `shell` window was folded into the mind channels (2026-06-17), `mesh-clear`
absorbed the judgement `mesh-mind-compact` used to make. Nothing asked whether any of those fusions
is still a unit.

## What landed

`agential_reversion()` in `scripts/mesh-vitality`, report-only (never touches the `[vitality-low]`
edge or the exit code).

Over `AR_WIN_D`=90 days, for each candidate collective (≥ `AR_SIZE`=400 lines now), take its
**modification** commits (`--diff-filter=M`; a file's creation is one contiguous insert and would
read as maximally local — the opposite of true) and merge hunks sitting within `AR_GAP`=50 lines of
each other. A commit still spanning ≥2 **separated** regions is a *collective-level* change: it had
to coordinate parts that are not neighbours — here, the block **and** the render line **and** the
smoke test. A commit confined to one region is *particle-level*.

**I** = share of commits that are collective-level. The sign is **I(late half) − I(early half)**,
per file, oldest-first. `REVERTING` when some qualifying file has fallen by ≥ `AR_DELTA`=0.20 while
persisting; otherwise `INTEGRATED`; `INSUFFICIENT` when nothing qualifies.

### The dormancy gate — found by looking at the first live hit

The first live reading named `mesh-converse` (d=−0.26, I 0.38→0.11). Reading the file's history
killed the verdict: its last modification was **67 days before the measurement**. A dormant file
falls exactly the same way — its late commits are stray one-region touch-ups from fleet-wide sweeps
— but the paper's agential reversion is a body that persists **and is still being adapted**, only at
a lower level. `AR_RECENT_D`=30 now excludes it, counted as `dormant=` rather than judged. Without
that gate the axis would have shipped with a false positive as its headline.

### Declared limits, none of them small

1. Hunk **count** is confounded by edit **size**; `AR_GAP` blunts that and does not remove it.
2. A file whose spine is simply **finished** — only leaves changing — falls the same way as internal
   conflict, and this measure **cannot separate them**. A hit is a lead for a human, never a verdict.
3. **Paradigmatic** reversions (a tool split back apart) are **out of scope** — detecting them needs
   rename/copy tracking across the split, and pretending otherwise would let the loud kind hide
   inside a sign built for the quiet one.
4. Internal **conflict**, the paper's actual driver, is not observed at all — only its predicted
   co-edit shadow.

### Gate

`mesh-vitality --test` green. `agential_reversion --selftest` has five arms: **REVERTING** and
**INTEGRATED** are the *same* fixture with its halves swapped (git log is newest-first, so a flipped
time axis inverts every verdict); **gap-merge** uses commits that all have two hunks, 10 lines apart
recently and 890 apart earlier, so a raw hunk count returns INTEGRATED and only region-merging
reaches REVERTING; **thin** requires a 3-commit half to self-exclude; **dormant** is arm 1 dated past
`AR_RECENT_D`. Both the live path and the selftest call **one** analyzer (`_ar_py`) — a selftest
running its own copy of the predicate would test a different program than the one that reports.

Four mutants driven RED from a scratch copy: flipped time axis (3 arms red), hunk-count instead of
region separation (1), floor removed (1), dormancy gate removed (1).

### Live reading at landing

```
agential-reversion=INTEGRATED(worst=mesh-job-apply,d=-0.08;q=61,thin=137,dormant=22)
```

61 files qualified as collectives; 137 self-excluded below 8 commits a half; 22 dormant. No file has
fallen far enough to read as reverting — the genome's collectives are still being changed as wholes.
