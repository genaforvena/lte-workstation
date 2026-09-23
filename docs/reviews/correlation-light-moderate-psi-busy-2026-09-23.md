# CORRELATION light-MODERATE × psi-BUSY — DISCARDED (regime shift, 2026-09-23)

Claim (idea-queue row 1619): when light reads MODERATE, psi tends to read BUSY (lift
2.80, 11 episodes, hour-stratified vs shadow 0.82; 8 occasions / 11 episodes of 388,
window 1002.7h; invariance UNSTABLE 0/3 envs: 0.64 / 1.25 / 1.20).

Verdict: DISCARD — no fused sense, no reflex. One line why: BUSY barely existed before
the 2026-08-15 regime boundary (11/234 readings) while all 22 co-occurrences sit in the
recent tail — inside the regime where BUSY is actually present the lift is 1.29, and 0/3
environments clear the floor.

Evidence (live, 2026-09-23, read-only):

- `scripts/mesh-correlate --dry` rc=0: no MODERATE×BUSY line; `--list` likewise empty.
  The pair does not surface on the current tape; the queued seed is stale.
- Prior full verdict (docs/correlation-investigation-light-moderate-psi-busy-spurious-2026-09-06.md):
  regime-restricted lift 1.29 < 1.8 floor; env17 0.64 / env20 1.25 / env21 1.20 (0/3);
  earlier regime (2418 rows, 69% of window, 50 MODERATE rows) had zero co-occurrences.
  Hour-matching cannot fix a rate change across the window; no light/load physical
  mechanism exists (psi = kernel pressure thresholds; support tracks when BUSY became
  common, not illumination). Regime-onset correction in `scripts/mesh-correlate`
  (REGIME_GATE=1, verified live above) is the standing general defense.
- Usefulness: nothing to fuse — the "coupling" is a window-regime artifact, and the
  correlation seed stays withheld per the tool's own UNSTABLE verdict.

No tool edited. Receipt left uncommitted for steward landing.
