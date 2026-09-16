# Senses disposition: sound claim 4 — 2026-09-16

## Live artifact

Command: `timeout 90 mesh-series-stats --claims`  
Corpus: `/home/mesh-home/.mesh/records.log`, 2442 rows, mtime `2026-09-16T08:25:02Z`.

The live output reports:

```text
sub-window rows: n=1608  impossible=320 (19.9%)  abstained(no whole-file scan)=406
arms: ... ear 13/527=2.5% note3 305/465=65.6% ...
degenerate whole-file scans ...: 341 of n=1608, and 286 of the 320 violation(s)
side[note3]: viol n=305 beats=6.1 fbeats=1.1 | clean n=160 beats=4.2 fbeats=13.2 -> window +45%, file -91%
claim-gate: rc=2
```

This independently reproduces sound review message `2971fcb18cfbed36` (reported 320/1602;
the corpus advanced between observations, while the count stayed 320).

## Shared-path inspection

`scripts/mesh-soundscape:157-162` defines `window_beats()` as one independent
`librosa.beat.beat_track(..., units="frames")` call. The scan calls it separately for the
selected slice and the whole-file segment at `scripts/mesh-soundscape:189-204`; therefore the
tracker's returned event count is not a monotone interval count. The claim-gate comment in
`scripts/mesh-series-stats:545-568` incorrectly promotes “same estimator” to a structural
containment invariant.

The 286/320 `fbeats=1` cases are additionally degenerate: one detected beat supplies no
inter-beat interval. The later `beat_of` fallback can turn that missing period into a plausible
500 ms value, so this is a live measurement-quality defect, not evidence that the sub-window
contains physically more beats.

## Disposition

**REFUTED as a claim, valid as a detector-health symptom; no sound ranker retune.** The current
gate is measuring an invalid invariant and its pooled percentage is not a physical contradiction.
The corrective action is to demote claim 4 from “structural impossibility” to an explicitly named
beat-tracker disagreement/health diagnostic, exclude `fbeats<=1` from any rate with an UNKNOWN
counter, and keep the two-sided (`window` vs `whole-file`) decomposition. The `fbeats=1` path must
remain UNKNOWN to consumers deriving a period; no default period may be minted from it.

The actionable corrective task is recorded as `senses/sound-claim4-measure-contract`.
