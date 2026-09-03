# tiny-fleet: Architectural Drift Report

**Date:** 2026-09-03
**v1 snapshot:** 54758160 (June 15 2026, 807 commits)
**v2 snapshot:** HEAD (Sep 3 2026, 4276 commits)
**Base model:** smollm2:135m (via ollama Modelfile approach)

## The Core Idea

Train two tiny models on different codebase snapshots, then prompt both with the same
incomplete input. The difference between M₁ and M₂ is the **architectural drift** of the
project, expressed generatively.

Since we can't pip-install torch on every node, we use ollama Modelfiles with version-specific
system prompts + few-shot examples extracted from each snapshot. The structural drift is
measured both statistically and via embedding similarity.

## Structural Drift

| Metric | v1 (June 15) | v2 (Sep 3) | Growth |
|--------|-------------|------------|--------|
| Files | 232 | 1,439 | 6.2x |
| Total size | 1,343 KB | 29,541 KB | 22.0x |
| Avg file size | 5.8 KB | 20.5 KB | 3.5x |
| Vocabulary (unique terms) | 11,011 | 88,724 | 8.1x |
| mesh-* tool references | 3,189 | 30,326 | 9.5x |

New file types appeared: `.c` (43), `.rom` (26), `.tal` (25), `.h` (15) — the uxn/Varvara
retro-computing layer didn't exist in v1.

## Vocabulary Drift

**Top new terms in v2 (freq ≥ 5):** `tape`(2643), `_td`(2366), `slug`(1777), `constant`(1172),
`arXiv`(1058), `rom`(1006), `DEGRADED`(970), `uxn`(942), `mesh-home`(922), `ratio`(902),
`promises`(855), `fyi`(816), `note3`(804), `episode`(764)

**Fastest growing shared terms:**
- `arm`: 5 → 2,289 (458x) — the detector/actuator/alert arm vocabulary
- `ledger`: 9 → 2,729 (303x) — hledger-based coordination
- `coverage`: 6 → 1,383 (231x) — the measurement coverage concept
- `fixture`: 16 → 3,557 (222x) — test fixtures for verification
- `floor`: 11 → 2,682 (244x) — threshold/band vocabulary

**Gone terms (freq ≥ 3):** 40 terms disappeared — the early codebase had concepts that were
superseded by the mature vocabulary.

## Pattern Drift

| Pattern | v1 | v2 | Change |
|---------|----|----|--------|
| `trap ` | 55 | 1,233 | +2,142% |
| `ts()` | 52 | 459 | +783% |
| `mesh-chat` | 248 | 1,526 | +515% |
| `mesh-health` | 32 | 122 | +281% |
| `set -euo` | 15 | 43 | +187% |
| `readonly` | 0 | 16 | new |

The `trap` explosion (+2,142%) reflects the doctrine of signal handling and process lifecycle
management that emerged over the summer. `ts()` growth (+783%) shows the shift to timestamped
logging across every tool.

## Conceptual Drift

What v2 knows that v1 barely does:

| Concept | v1 count | v2 count | Multiplier |
|---------|----------|----------|------------|
| gate | 137 | 7,872 | 57x |
| verdict | 131 | 7,672 | 58x |
| board | 185 | 5,911 | 32x |
| reflex | 208 | 4,267 | 21x |
| organ | 155 | 2,774 | 18x |
| cadence | 22 | 2,077 | 94x |
| probe | 87 | 2,136 | 25x |
| coverage | 6 | 1,383 | 231x |
| drift | 70 | 1,213 | 17x |
| census | 21 | 641 | 31x |
| autopoiesis | 7 | 193 | 28x |
| staleness | 2 | 188 | 94x |
| homeostasis | 20 | 176 | 9x |
| taint | 0 | 25 | ∞ |

The conceptual vocabulary shifted from operational (`check`, `status`, `monitor`) to
systemic (`gate`, `verdict`, `cadence`, `coverage`, `drift`). This is the **emergent
ontology** of the mesh — words that weren't needed when the system was simple became
load-bearing concepts as complexity grew.

## Generative Drift (Embedding Similarity)

Same prompts → M₁ (v1 system) vs M₂ (v2 system) → cosine similarity of outputs:

| Prompt | Similarity | Interpretation |
|--------|-----------|----------------|
| Node alive check | 0.657 | Different patterns emerge |
| Sensor freshness | 0.659 | v2 adds staleness/coverage concepts |
| Health to board | 0.168 | MASSIVE divergence — v1 has no "board" concept |

**Average similarity: 0.4946**
**Drift score: 0.5054 — HIGH architectural drift**

## What This Means

The 0.50 drift score says: if you give both versions the same incomplete code and ask them
to complete it, they produce outputs that are only ~50% similar in embedding space. The
architectural drift is not just "more code" — it's a fundamentally different *vocabulary of
concerns*.

v1 thinks in: `check`, `error`, `warn`, `info` — basic operational primitives.
v2 thinks in: `gate`, `verdict`, `cadence`, `coverage`, `arm`, `ledger` — a self-monitoring
ontology where every tool has a measurement story, every measurement has a coverage bound,
and every verdict cites its evidence.

The drift is not linear. The conceptual vocabulary (`cadence` 94x, `coverage` 231x) grew
much faster than the code itself (22x). The system didn't just get bigger — it developed
a *theory of itself*.

## How to Reproduce

```bash
# On a node with ollama + GPU:
mesh-tiny-fleet extract     # pull snapshots + build training data
mesh-tiny-fleet train       # create ollama models
mesh-tiny-fleet compare     # run comparison prompts
mesh-tiny-fleet drift       # full analysis

# Or just the structural analysis (no GPU needed):
./scripts/mesh-tiny-fleet drift
```

## Model Capacity Effect

The drift measurement is **sensitive to model capacity**:

| Base Model | Avg Similarity | Drift Score | Verdict |
|------------|---------------|-------------|----------|
| smollm2:135m | 0.4946 | 0.5054 | HIGH |
| qwen2.5:3b | 0.8005 | 0.1995 | MODERATE |

The 135m model amplifies vocabulary differences because its limited capacity makes it
more dependent on the system prompt. The 3b model draws on pre-trained knowledge to
produce more similar outputs regardless of the prompt. **Both measurements are valid** —
they measure different things:

- 135m measures **vocabulary drift** (what words the codebase uses)
- 3b measures **conceptual drift** (what ideas the codebase expresses)

## Weekly Tracking

`mesh-tiny-fleet-snapshot` captures structural metrics every Sunday at 03:00 UTC and
appends to `~/.mesh/tiny-fleet/drift-series.jsonl`. It tracks:
- File count, total size, average file size
- Vocabulary size, mesh-* reference count
- 23 key concept frequencies (gate, verdict, cadence, coverage, etc.)
- File extension distribution

The ollama-based generative comparison (`mesh-tiny-fleet compare`) is run manually
when a deeper drift measurement is needed.

## Limitations

1. **Modelfile ≠ fine-tune.** The system prompt changes behavior but not weights. True
   fine-tuning (LoRA on the actual code) would show even more divergence because the model
   would internalize the *patterns*, not just the *vocabulary*.

2. **Snapshot selection matters.** We used June 15 vs Sep 3 — a 3-month gap with 3,469
   commits. Shorter intervals would show finer-grained drift.

## Next Steps

- **True LoRA fine-tuning** on each snapshot (needs torch + transformers, not available on
  every node)
- **Prompt-specific drift** — measure which types of code drift fastest (senses vs reflexes
  vs substrate)
- **Cross-node comparison** — same prompt, different nodes' local models, compare dialects
- **Drift score over time** — once weekly snapshots accumulate, plot the concept frequencies
  as a time series to see which concepts are accelerating
