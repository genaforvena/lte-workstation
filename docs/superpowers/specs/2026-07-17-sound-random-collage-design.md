# Sound reflex: random collage from ambient — design

**Date:** 2026-07-17
**Tool:** `scripts/mesh-sound-reflex` (`tick()` only)
**Board slug:** `sound/random-cut-select-from-ambient` · owner `mesh-sound-reflex/sound`
**Doctrine:** memory `sound-mixes-random-from-ambient` (operator «Одобряю sound»)

## Operator intent (verbatim, two TG messages same day)

1. «sound должен делать миксы не из того, что есть, а из записей случайных, которые меш делает…
   не чужие, а случайно нарезанные и выбранные из того, что меш слышит» — mixes come from the
   mesh's OWN ambient recordings (room mic), **randomly cut and randomly selected**, not foreign
   tracks, not by best-score.
2. «кашель и тишину молоть тоже интересно» — grinding **cough and silence is wanted too**. Drop
   the grindability floor; near-silence and transients are valid, selectable material.

## What changes

Replace the score-argmax selection at `mesh-sound-reflex` `tick()` (~line 447, the
`# Rank by score ONLY … a stronger record led this block` block) with a **block collage** built
from random selection + random cuts. Remove the density/beats *picker gate*; the only remaining
entry gate is a **validity guard**.

Unchanged: fresh-block anchoring / `consume`, the `drop` privileged lane, novelty gate,
`grind_cap`, detached grind, `mesh-room-music` as the sole grind owner, `mesh-soundscape` as the
sole measure tract.

## Flow (new `tick()` selection section)

1. Fresh block, `drop` privilege, empty-block decline — **unchanged**.
2. **Pool** `P` = every record in the fresh block (excluding `drop`) whose source file passes the
   **validity guard**. No density filter, no beats filter.
   - Validity guard: `ffprobe` reports an audio stream with `format.duration > 0`, and the file is
     non-trivial (size floor, e.g. > 1 KB, to reject 0-byte / header-only). A valid near-silent wav
     **passes** (operator wants silence). A corrupt / 0-byte / evicted file **fails** →
     `skip:invalid-source` (or `skip:evicted-before-grind` when the file is simply gone).
3. `P` empty (every source invalid/evicted) → decline out loud (each block row → `skip:invalid-source`
   / `skip:evicted-before-grind`), `consume`, return.
4. **Collage draw** (single pass, no floor retry loop):
   - `K = rand(1 .. min(|P|, SR_COLLAGE_MAX))`.
   - Random subset of `P` of size `K` (the **seed** = one of them, carries the ledger grind verdict).
   - Each selected record → random cut: `len = rand(SR_CUT_MIN .. SR_CUT_MAX)` clamped to source
     duration; random offset in `[0, dur-len]`; `ffmpeg -ss <off> -t <len> -ac 2 -ar 44100` → scratch
     wav.
   - Concat the cuts in **random order** (`ffmpeg -f concat`) → `feed.wav` in a `mktemp -d` scratch.
   - If concat yields no audio (all cuts failed to decode) → decline block (`skip:invalid-source`),
     clean scratch, `consume`, return.
5. **Re-measure the feed for AXES ONLY** (`mesh-soundscape --measure feed.wav`). This is *not* a gate
   — it supplies `dyn/act/rich/move/cent/beats/win` for the recipe so the grind stays coupled to the
   real material (the "not trivial / not boring" half of the doctrine). `MEASURE none` (near-silence)
   is **not** a rejection: fall back to the derive defaults / measured-median axes and `beat_of`'s
   500 ms fallback, and grind anyway.
6. **Derive** the recipe from the feed's measured (or fallback) axes + `beat_ms`. Novelty gate
   unchanged. Remove the `MIN_BEATS` beatless pre-skip on this path — a beatless feed is allowed to
   reach the grinder.
7. **Grind** `feed.wav` detached, `grind_cap` sized by feed duration; the bg job removes the scratch
   dir when done. Provenance: `MESH_RMC_META="src=collage/<seed> parts=<h1,h2,…> cuts=<off:len,…>"`.
8. **Verdicts** (every fresh row settles — anchor honesty preserved):
   - seed → `grinding` → `ground:<mp3>` / `skip:degenerate` / `skip:grind-timeout(...)` (existing bg
     outcomes).
   - other selected → `blended:<seed>` (used, not declined).
   - valid-but-not-selected → `skip:not-selected(random collage)`.
   - invalid / evicted source → `skip:invalid-source` / `skip:evicted-before-grind`.
9. `consume(last)`.

## Why no floor / no retry loop

The floor existed to keep the beat-driven automixer off transients. The operator now *wants* those
ground, so the picker imposes no floor. A silent or transient feed that grinds to nothing usable is
caught **downstream, honestly**, by `mesh-room-music`'s existing `valid_track` gate →
`skip:degenerate` — a grinder outcome, never a pre-filter. Whether ground silence is *audible* is the
grinder's job (its gain-normalisation can lift room hiss into granular texture); the picker only makes
silence **selectable and fed**. Because there is no floor to satisfy, the draw is a single pass — no
re-draw loop.

## New tunables (header, documented)

- `SR_COLLAGE_MAX` (default 4) — max records per collage.
- `SR_CUT_MIN` / `SR_CUT_MAX` (default 4 / 12 s) — random cut window bounds, clamped to source dur.

`SR_MIN_DENSITY` / `SR_MIN_BEATS` are **retired from this path**. Keep them read-only (a node may
export them in `~/.mesh/nodes`) so their meaning doesn't silently change, and leave the historical
cough-guard reasoning in the header marked as HISTORY for this lane — do not re-add the floor.

## `--test` — the gate flips (every assertion drives real behaviour)

Under the existing sandboxed-ledger / `LOCK` isolation (never touches the live ledger, never writes
the liveness log). Fixtures built with `ffmpeg lavfi` (deterministic; no RNG inside an assertion).

1. **Validity guard, silence INCLUDED (the inverted cough-guard test):** a valid near-silent wav
   (`anullsrc` / very low sine) → assert it is a **selectable** pool member (can be drawn + fed). A
   0-byte / corrupt file → assert **excluded** (`skip:invalid-source`, grinder never invoked).
   **Break the validity guard so it rejects silence → this test must go red.**
2. **Random selection, not score:** 20 draws over a synthetic block where the argmax-score record is
   not the only member → assert ≥ 2 distinct seeds appear. (Uniform over ≥ 2 items ⇒ P(all-same) ≈
   2⁻¹⁹ — robust, not a flaky majority-of-3; see memory `a-stochastic-gates-threshold-is-a-statistic`.)
3. **Random cut:** 20 cuts → ≥ 2 distinct `(off, len)`.
4. **Collage:** with `|P| ≥ 2`, at least some draws produce `K ≥ 2` and the feed concatenates > 1
   cut; assert contributors settle `blended:<seed>`, not `not-selected`.
5. **Recipe from feed:** assert the derived axes track the feed's `--measure` line (or the documented
   fallback when `MEASURE none`), not a stale ledger row.

Discipline: **watch each gate go red before restoring** (a gate not seen failing is not a gate).
Run mutants from a scratch copy; restamp any live artifact a fixture child forges.

## Honest limitations (documented, not papered over)

- A block with one valid record ⇒ the "random subset" is that one record; only the *cut* is random.
  Real cross-record randomness accrues across blocks over the day, which is how the ear feeds it.
- Near-silent feeds frequently grind hollow ⇒ `skip:degenerate`. The operator will *hear* ground
  silence only when the grinder makes something audible of it; if he later wants that reliable, it is
  a separate grinder/recipe change (gain, granular params), not a picker change.
- `drop` (operator `~/.mesh/inbox`) stays privileged and whole-file; note a full-length drop can
  balloon to a 40–50 min granular render — send a trimmed slice (tracked separately in the memory).
