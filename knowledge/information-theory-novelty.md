# Field → application: information theory → a novelty/surprise signal

**Field:** Information theory (Shannon, 1948 — about as well-studied as fields get).
**Core idea applied:** the *self-information* of an event is `I(x) = -log2 P(x)`.
A rare or never-seen event carries many bits; a routine one carries few. Attention
should follow *information*, not *volume*.

## The gap it fills

The mesh emits hundreds of routine lines a day — `[done]`, `[taking]`,
`[git-lock]` — and a handful of rare ones — `[health-fail]`, `[incident]`,
`[gap]`, a first-seen device, a never-before tag. With no measure, signal drowns
in noise: an absent operator faces 200 lines, and a cheap reflex can't tell
"wake an expensive mind" from "nothing happened."

## The tool

`mesh-novelty` learns the BASELINE distribution of event types from the board's
history (add-1 / Laplace smoothing so a never-seen type gets the maximum
surprise), then scores a RECENT window:
- per-event surprisal in bits under the baseline,
- an aggregate novelty score (mean bits of the window),
- the specific high-surprise events + first-seen entities (device MACs).

On real data it ranks `[health-fail] Redmi` (7.2 b) and a `CRITICAL [check]`
above the routine `[done]` flood (~1 b) — pure information content, no heuristics.

## Two payoffs (both real)

1. **Legibility.** `mesh-digest` now LEADS with the highest-bit events, so after
   an absence the operator sees what was genuinely NEW before the routine volume.
2. **Spend.** `mesh-novelty --threshold B` is a cheap reflex that can gate
   expensive minds: feed a mind only when the window is genuinely novel
   (≥ B bits) or a new device appears; stay silent on routine. Attention —
   and token cost — follows information.

## Honest limits

- Event "type" is currently the bracket tag + a coarse class. Finer signatures
  (author-role, content n-grams) would sharpen it; tags are a strong, cheap start.
- Baseline is the whole board history; a sliding/decaying baseline would adapt
  to regime change (a busy sprint shifts what's "routine").
- It measures surprise, not importance — a rare-but-trivial event scores high.
  It's a *spotlight*, not a judge; a mind still decides if the surprise matters.

Related: [[channel-stream-architecture]] (reflex→text→conditional mind-feed —
novelty is the ideal gate), [[quiet-is-not-done]].
