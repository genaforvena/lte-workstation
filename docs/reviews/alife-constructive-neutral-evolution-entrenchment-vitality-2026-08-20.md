# Artificial life & open-ended evolution → CONSTRUCTIVE NEUTRAL EVOLUTION as the null for our own complexity growth (2026-08-20)

**Angle (from the idea-queue draw):** a known **CRITIQUE / failure mode** of the area.
**Landed:** `cne_load()` in `scripts/mesh-vitality` — a per-construct-class **entrenchment index** against a
corpus control arm. Uncommitted in the tree; steward lands.

## The critique (named + cited)

**Constructive Neutral Evolution (CNE)** is the standing objection to every "complexity increased, therefore
the system is open-ended" claim. Its three-step ratchet (Stoltzfus 1999): a component with **excess capacity**
already *buffers* a variant → a damaging change is therefore **neutral when it arrives** (it is **masked**) →
it fixes by **drift** → and the buffer is now **presupposed** by the variant, so it can never be removed.
No step was selected *for*. Complexity rose anyway.

- Stoltzfus, A. (1999). "On the possibility of constructive neutral evolution." *J Mol Evol* 49:169–181.
- Gray, Lukeš, Archibald, Keeling & Doolittle (2011). "**Irremediable Complexity?**" *Science* 330:920–921 —
  names the product: not an adaptation but a "runaway bureaucracy" / Rube Goldberg machine, and —
  the load-bearing word — **irremediable**: unremovable, because removal now breaks the dependents that grew
  up presupposing it. https://www.science.org/doi/10.1126/science.1198594
- Muñoz-Gómez, Bilolikar, Wideman & Geiler-Samerotte (2021). "Constructive Neutral Evolution 20 Years Later."
  *J Mol Evol* 89:172–182. https://pubmed.ncbi.nlm.nih.gov/33604782/
- **LIVE, and inside this field** (found by WebSearch 2026-08-20, not from a fixed list):
  - Catherall-Ostler & Dixit (2025). "**The Constructive Neutral Evolution of Behaviour**." *Ecology and
    Evolution* 15(7):e71736 — CNE carried from molecules to **behaviour**; their framing is that only natural
    selection is *ordinarily* thought to raise behavioural complexity, and CNE is the second driver.
    https://onlinelibrary.wiley.com/doi/10.1002/ece3.71736
  - Walsh, A. (2026). "**Neutrally Evolving Interlocking Complexity in the Quandary Den**." arXiv:2604.18361
    (Apr 2026) — an ALife model whose complexity rises **under unchanged informational demand**, by exactly
    two mechanisms: *subfunctionalization* and **masking** (harmful interactions accumulate and are
    *suppressed by regulation* rather than removed). https://arxiv.org/abs/2604.18361

## Why this is somewhere we have not been

Zero hits for `constructive neutral|irremediable|entrench|Stoltzfus|Doolittle` across all 255 files in
`docs/reviews/` and all of `scripts/`. The adjacent things we DO have are different nulls:

- `evo_activity` (Bedau/Channon **neutral shadow**) — a demography-matched null for **which components get
  used**. CNE asks about the **removal rate of a construct class**: different null, different population.
- `assembly_signature` — motif reuse in **commit subjects**; never reads the diff.
- `phylum_coherence` — trait **spread across tools**; not persistence-through-editing.
- `mls_conflict` — newborn **tool** fate. `cne_load` never looks at a tool boundary; it is a line-class statistic.

And CNE's mechanism is not exotic here — **masking is this mesh's own named deleterious class**: CLAUDE.md's
"the SILENT FALLBACK" (`cmd 2>/dev/null || echo <default>` turns a total failure into a plausible constant)
is a textbook CNE buffer. That made the obvious hypothesis "our masks are ratcheting", and it is **wrong** —
see below. That inversion is the finding.

## The gap it closes in `mesh-vitality`

Every complexity-rising sign in that file — `assembly_signature`, `phylum_coherence`, `heaps_beta`,
`renewal_trend`, `tool_count` — reads a **rise** and calls it vitality, and **not one can tell an adaptation
from a bureaucracy**. The POSIWID block at the head of the same file already named the symptom on 2026-06-21
("weight `commit_velocity` by behavior-changing delta") and **HELD** the fix for one stated reason:
*"behavior-changing" could not be defined without punishing the deliberate instrument-first / knowledge-tier
discipline, and "must be validated against real git history before it changes the verdict."*

CNE supplies the missing discriminator, and it is **not the add rate at all** — it is the **removal
asymmetry**. Knowledge-tier prose that is doing work gets **revised**: removed and rewritten at some rate.
Bureaucratic accumulation is the class that, once written, is never touched again.

## What was measured (live genome, 1000 commits touching `scripts/`, 2026-08-20)

The measurement **needs a control arm**, because in an overwhelmingly additive corpus every class grows.
Corpus baseline removal ratio = all removed / all added = **0.064** (+146814 / −9421 — 15.6 lines added per
line removed). Entrenchment index = (class removal ratio) / baseline:

| class   | +added | −removed | rem. ratio | **entrench** | share of adds |
|---------|-------:|---------:|-----------:|-------------:|--------------:|
| funcdef |    799 |       24 |     0.0300 |     **0.47** |         0.005 |
| comment |  47600 |     1803 |     0.0379 |     **0.59** |     **0.324** |
| code    |  87620 |     6173 |     0.0705 |         1.10 |         0.597 |
| envknob |   2294 |      192 |     0.0837 |         1.30 |         0.016 |
| mask    |   4273 |      606 |     0.1418 |     **2.21** |         0.029 |
| gate    |   4228 |      623 |     0.1474 |     **2.30** |         0.029 |

Two results, and the first one **inverts the naive alarm**:

1. **Masks are the most purified class in the genome, not the ratcheting one.** The raw count says masking
   constructs accumulated **+3730 net** over 1000 commits — an alarming number that is a pure artifact of
   reading a count with no control. Against the baseline, `mask` (2.21) and `gate` (2.30) are removed at
   **~2.2× the corpus rate**. The silent-fallback doctrine is *working*: the class it hunts is the one the
   mesh actually un-writes. (Same shape as *a-knockout-drill-with-no-control-arm* and *an-exclusion-count-is-
   a-bias-term*: the alarming raw number and the corrected one point opposite ways.)
2. **The entrenched class is prose.** `comment` = **32.4% of every line added to `scripts/`**, removed at
   **0.59×** the baseline rate. The genome's complexity growth is concentrated in the one class it almost
   never removes. That is the CNE signature stated precisely, and it is exactly the regime the 2026-06-21
   POSIWID hold suspected but could not measure. `funcdef` is more entrenched still (0.47) but holds 0.5% of
   the growth — which is what the share filter is for: an entrenched class that carries no growth is not a
   bureaucracy, it is a stable core.

## The change (uncommitted — `scripts/mesh-vitality`)

`cne_load()` — over the last `MESH_VIT_CNE_WIN_N` (1000) commits touching `scripts/`, classify every added
and removed diff line (`comment · mask · gate · envknob · funcdef · code`), compute the corpus baseline
removal ratio (**the control arm**) and a per-class entrenchment index, and label the class that both
**dominates the growth** (≥ `CNE_SHARE`=0.25 of all adds) and is **entrenched** (index < `CNE_ENTRENCH`=0.80):

- `CNE-SHAPED(<cls>:entrench,share,base,n)` — the growth is carried by the least-removed class.
- `PURIFIED(...)` — the growth class is removed at or above baseline.
- `DIFFUSE(...)` — no single class holds ≥25% of the growth.
- `INSUFFICIENT(commits=..|adds=..)`; `n/a` when the baseline is 0 (no removals at all → every index is 0/0,
  a fabricated verdict) or python3/git are absent.

Live reading right now: `CNE-SHAPED(comment:entrench=0.59,share=0.32,base=0.064,n=146814)`.

**Report-only, and a LEAD, never a verdict** — same posture as `nfds`/`mls_conflict`/`ecology`. It does not
touch `commit_velocity` or the verdict, which is the caution the 06-21 hold asked for; it supplies the
git-history validation that hold demanded. And the index cannot separate *unremovable* from *nobody needed
to*: a low index also fits a class that is simply stable and correct. It answers one question no other sign
in the file asks — **where is the growth that never gets un-written?**

## Gate seen RED, then green

`cne_load --selftest` drives the **real** `classify`/`score` code on two synthetic diff fixtures whose only
difference is the removal side (cne-shaped vs proportionally-purified). Broken deliberately by making
`classify()` return `'code'` for a comment line: both fixtures collapsed to `PURIFIED(code)` → `selftest:
FAIL`, rc=1. Restored → `selftest: PASS`, rc=0. Full `mesh-vitality --test` green with the axis wired
(`cne_load=CNE-SHAPED(...)/selftest: PASS`).

## The self-implicating footnote

This review is itself ~120 lines of prose plus a ~65-line comment header in the very class it just flagged as
the genome's entrenched growth. That is not a reason to skip it — it is the reason the axis had to be
report-only and the reason the index is a lead. The honest next question, which this does **not** answer:
does the entrenched prose get *read*? CNE's own answer is that an unread buffer is exactly what irremediable
complexity looks like from the inside.
