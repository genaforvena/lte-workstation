# LITERATURE review — Assembly Theory as a SELECTION-signature axis for autopoiesis (2026-07-31)

**Area:** complex adaptive systems / edge of chaos (Santa Fe lineage), entered from the angle of an
**operational mechanism that measures whether SELECTION is acting** — not a criticality statistic.
**Reviewer:** genome mind · live web search (WebSearch, 2026-07-31) + read of the primary literature
**Verdict:** LAND — one un-embodied concept, one shipped (uncommitted) read-only axis with a red-then-green gate.

---

## The idea, and where it is being published now

> **Assembly Theory (AT)** — Sharma, Czégel, Lachmann, Kempes, Walker & Cronin,
> *"Assembly theory explains and quantifies selection and evolution"*, **Nature 622:321 (2023)**
> (preprint arXiv:2206.02279). Formalised further in Kempes, Lachmann, Iannaccone, Fricke, Chowdhury,
> Walker & Cronin, *"Assembly theory and its relationship with computational complexity"*,
> **npj Complexity 2:6 (2025)**, doi:10.1038/s44260-025-00049-9.

AT quantifies how much **selection** a *population* of objects evidences, from two measurements per object:

- **assembly index** `a_i` — the minimum number of joining steps to build the object by reusing
  already-constructed sub-parts;
- **copy number** `n_i` — how many instances are observed.

The **Assembly equation**: `A = Σ_i e^{a_i} (n_i − 1) / N_T`.

The move that makes AT distinct from every complexity/diversity measure: a complex object (high `a_i`)
is trivial to produce *once* by chance, but producing it **in abundance** (high `n_i`) requires a
memory / copying / selecting history. **Complex-AND-abundant is the fingerprint of a selecting process**,
and neither term alone suffices — the `(n_i − 1)` factor zeroes a one-off; `e^{a_i}` discounts an
abundant-but-trivial object.

### The live controversy (honored, because this is a *live* review)

AT's claim to measure something Shannon/LZ cannot is **contested**: Abrahão et al.,
*"Assembly Theory Reduced to Shannon Entropy and Rendered Redundant by Naive Statistical Algorithms"*
(arXiv:2408.15108, 2024), and the computational-complexity reading (arXiv:2406.12176 / npj Complexity
2025) argue the assembly index is compression-adjacent. This is exactly why the shipped axis does **not**
collapse to a frequency count and does **not** gate on `A`'s raw magnitude — see below.

## Why it is genuinely un-embodied

`grep -riE 'assembly.index|assembly.theor' scripts/ docs/` → **0 hits** (verified 2026-07-31).
The mesh's compression-complexity `C_s` (`mesh-criticality --compress`) is *per-object* Kolmogorov-proxy
on the **board event series**; it never couples an assembly index with a **copy number across a
population**, which is the whole of AT's selection claim. Ergodicity (mesh-chaos ruin barrier,
pooled-corpus AUC), branching-ratio SOC (mesh-criticality, ~20 sidecars), swarm/stigmergy (mesh-forage),
and causal-emergence (Rosas-PID in mesh-situation — *discarded* for lack of a micro state to coarse-grain)
are all already deep. Assembly Theory is a different corner: **is a selecting history operating on what
the mesh produces?**

## The gap it closes in a real organ — `scripts/mesh-vitality`

`mesh-vitality` is the autopoiesis vital-signs reflex. Its existing axes reward **quantity**
(`commit_velocity`), **soundness** (`verify_fails`), and **breadth** (`action_occupancy`,
`ecology_potential`). None measures whether production carries the **fingerprint of selection**.

The confound is subtle and named one function up: `action_occupancy()` (marginal edit entropy) reads
**maximal** for a stream that emits a fresh, structurally-distinct one-off object every commit — and by
this file's own POSIWID caveat that certifies "undifferentiated novelty with zero compounding" as peak
health. **AT inverts exactly that case**: pure one-off novelty has `n_i = 1` everywhere ⇒ `A = 0`, because
no selecting history is reusing complex work. So the new axis is the complement occupancy is blind to —
not "is production broad?" but "does what is produced show complex work-motifs *recurring* — a compounding
repertoire?" A loop can produce, produce soundly, produce broadly, and still **not select**.

### Shipped (uncommitted) — read-only `assembly_signature()`

- **Corpus** = commit **subjects** over `ASSEMBLY_WIN` (default 14 days) — the mesh's own produced record
  of self-modification. **Objects** = recurring token n-grams; `a_i` = join steps = gram-length − 1;
  `n_i` = occurrences. `A = Σ_i e^{a_i}(n_i − 1)/N_T` (cap on gram length bounds `e^{a_i}`).
- **Label turns on the DEPTH of recurrence** — the exact place AT parts from Shannon — never on `A`'s
  magnitude (no hardcoded cutoff; avoids the median-is-max trap):
  - `SELECTED` — a **deep** motif (`a_i ≥ ASSEMBLY_DEPTH`) recurs (`n_i ≥ ASSEMBLY_COPY`): complex
    work-objects in abundance ⇒ a selecting/compounding history *is* operating.
  - `NOVELTY-CHURN` — recurrence exists but **only among shallow** (single-token) motifs: reuse is
    Shannon-level only, complex work is all one-off (the critique's null pole, made explicit).
  - `ONE-OFF` — nothing recurs (`max n_i = 1`): pure novelty, `A = 0`, no selection signature.
- **Report-only**: appended to the trace-tier metrics wall (`report=`), never touches the
  `[vitality-low]` edge trigger or the exit code. Same posture as `heaps_beta`/`omega_cycle`.
- **RED-first `--test`**: three synthetic git-subject corpora (deep-motif → SELECTED; single-token reuse
  → NOVELTY-CHURN; all-distinct → ONE-OFF). Neutering the `deep_recurs` gate flips the CHURN/SELECTED
  discriminator → RED (verified: `deep_recurs=False` → "SELECTED fixture → NOVELTY-CHURN", then restored
  green). This exercises the classifier, not just "does it emit a label".

**Live at landing (real repo):** `assembly=SELECTED(A=471.7, depth=5, copies=208, "mesh…fix")` — the
mesh-land landing routine is a genuine deep-motif-in-abundance: the autopoietic loop has *selected* a
complex, compounding self-landing routine (as opposed to emitting undifferentiated novelty). Honest
positive.

## Unwired next step

The per-window `A` trajectory over the commit tape (does the selection signature *rise* as the mesh
matures, or flatten toward NOVELTY-CHURN when the loop degenerates into churn?) — the twin of the
edge-optimality / dynrange tape-joins on `mesh-criticality`. Also candidate: run the same axis over the
**produced-sound recipe corpus** (`room-music-params.log`) — but note the sound lane is *designed* for
anti-copy diversity (repulsion-from-recent), so low copy number there is intended, not a fault.

## Sources

- [Assembly theory explains and quantifies selection and evolution (arXiv:2206.02279)](https://arxiv.org/abs/2206.02279)
- [Assembly theory and its relationship with computational complexity — npj Complexity 2025](https://www.nature.com/articles/s44260-025-00049-9)
- [Assembly Theory Reduced to Shannon Entropy… (arXiv:2408.15108)](https://arxiv.org/pdf/2408.15108)
- [Assembly Theory and its Relationship with Computational Complexity (arXiv:2406.12176)](https://arxiv.org/abs/2406.12176)
