# ALife / OEE live review — compression PROGRESS (a derivative), not surprise (a level)

**Date:** 2026-07-31 · **Area:** artificial life & open-ended evolution · **Angle:** a foundational
idea the mesh applied too loosely (and named as a HELD gap, but never embodied).
**Tool touched:** `scripts/mesh-novelty` (new `--progress` axis; report-only). Uncommitted for the steward.

## The concept

**Interestingness = future compression progress, not novelty and not surprise.** This is Schmidhuber's
curiosity/creativity theory, freshly re-operationalized in **Herrmann & Schmidhuber, "Interestingness as
an Inductive Heuristic for Future Compression Progress", arXiv:2605.14831 (2026)** — found via web search
(the 2026 OEE literature front, alongside jennyzzt/awesome-open-ended). The paper's move:

- Interestingness is a **relational, prospective** property between an object and a learner's current
  state — *how much can I still learn from it* — grounded in **MDL** (model complexity + residual code).
- It is **NOT** count-based novelty and **NOT** prediction error: those fixate on **irreducible
  randomness** — the **Noisy-TV problem**. TV static is endlessly "surprising" yet unlearnable.
- The fresh mechanism is **stagnation length** `t − m̂`: symbols since the last compression breakthrough.
  The paper proves progress-probability decays `~2^-(t−m̂)`, so *the most promising object is the one that
  exhibited the most recent progress.*

## Why this is a "too loose" read, not virgin territory

`scripts/mesh-novelty` **already names this exact gap** — the `NOISY-TV / REDUCIBLE vs IRREDUCIBLE
SURPRISE` block at `:425-459` (Schmidhuber 1991; Burda et al. ICML 2019; Mavor-Parker et al. ICML 2022;
arXiv:2509.25438 2025). Every axis in the file — `surprisal`, `--conditional`, `--bayesian`, `--levels`,
`--territory` — scores a **LEVEL** of surprise in the recent window. None asks whether that surprise is
**falling** (learnable/epistemic) or **pinned high** (irreducible/aleatoric). So a churny board — a
flapping sensor minting a first-seen device MAC every scan — reads HIGH novelty every window and would
**wake expensive minds on noise forever** (use-case-2, the SPEND path). The block **HELD** the fix for
one reason: *"estimating learnability needs a multi-window history this single-pass call does not keep."*

The 2026 paper **dissolves that objection**: compression progress is the **derivative of amortized code
length over the FULL symbol sequence** — already available in one read. No persisted multi-window state.

## What was applied too loosely, concretely

`--bayesian` (Itti & Baldi) was the mesh's best answer to "attention should follow belief-update, not
improbability" — and it **habituates KNOWN-rare types**. But it is **fooled by all-NEW-type noise**: every
first-seen symbol moves the belief maximally, so a flapping sensor reads `MODEL-MOVING` and pays the wake.
The `--test` asserts this directly: on a 100-distinct-first-seen-type board, `mean_bits ≥ 4.0` AND
`--bayesian` reads MODEL-MOVING (both trip a wake) **while `--progress` reads NOISE** (skip). Surprise ≠
interestingness, demonstrated in-suite.

## The application (embodied)

`mesh-novelty --progress` (`--json`), report-only, opt-in — same discipline as the other instrument axes
(does NOT touch `mean_bits` or the wake gate; the behavioral wake-gating the held block reserves for the
steward stays the steward's — this lands the **measurement** it was blocked on).

- **Symbol stream** = the board's own event-type tokens (`event_type` per line), FULL history.
- **Code length** via `zlib` (stands in for MDL, per the paper's framing), header subtracted as an
  additive artifact. `L(k) = code_bits(prefix k)/k` = amortized bits/symbol.
- **Breakthrough** = a prefix checkpoint whose `L` dropped by ≥ `PROGRESS_EPS` (0.02 b/sym) vs the prior;
  **stagnation length** = symbols since the last breakthrough (`T` if none).
- **Verdict:** `LEARNING` (tail Δ ≥ eps — code length still dropping, learnable structure emerging) ·
  `NOISE` (stagnated AND `ρ = out/in bytes ≥ 0.7` — incompressible, the Noisy-TV) · `MASTERED` (stagnated
  but compressible — structure already absorbed). Env knobs: `MESH_NOVELTY_PROGRESS_{EPS,NSEG,RHO,MIN}`.

**Live board (this node, 2026-07-31):** `[LEARNING] 4.62 b/sym, tail Δ+0.05 b, ρ=0.578, stagnation 0 of
~3000` — the mesh's event vocabulary is still becoming more compressible (fresh breakthrough at the tail),
the open-ended zone: neither noise nor mastery.

## Distinctness (not a rename of a sibling)

- vs `--bayesian`: habituates known-rare, **fooled by all-new-type noise** (each moves the belief); this
  reads incompressibility → NOISE regardless of per-symbol novelty.
- vs `--diversity`: marginal SHAPE (order-blind). This reads the SEQUENCE.
- vs `mesh-vitality omega_cycle`: also order-sensitive, but over the **genome** commit stream (limit-cycle
  vs wandering); this is over the **board** event stream (compressibility derivative). Different substrate,
  different question.

## Verification (RED-first, seen fail then restored)

- `--test` legs: `LEARNING`/`NOISE`/`MASTERED` on three synthetic streams; the `Lcurve` proves the
  mechanism (LEARNING fixture holds flat at 8.0 b/sym through 40 noise symbols, then drops 8.0→3.6 exactly
  when a period-3 pattern begins). Thesis leg: noise board reads HIGH surprise + MODEL-MOVING but NOISE.
- Mutations seen RED then restored: `learning = False` → LEARNING fixture fails; `rho >= HI` → `rho < HI`
  (NOISE↔MASTERED inverted) → both fail; `eps=99` inline knob → LEARNING vanishes (derivative gate is
  load-bearing). All green after restore: `smoke-test: ok`.

## Sources

- Herrmann & Schmidhuber, *Interestingness as an Inductive Heuristic for Future Compression Progress*,
  arXiv:2605.14831 (2026).
- Schmidhuber 1991 (curiosity/boredom); Burda et al., *Large-Scale Study of Curiosity-Driven Learning*,
  ICML 2019; Mavor-Parker et al., ICML 2022; *Beyond Noisy-TVs*, arXiv:2509.25438 (2025) — all already
  cited in the file's own `:425-459` held block.
- Context: jennyzzt/awesome-open-ended; Hughes et al., *Open-Endedness is Essential for ASI*,
  arXiv:2406.04268 (the novel-AND-learnable definition the mesh already embodies in `mesh-vitality`).
