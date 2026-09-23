# CORRELATION desk-DEGRADED × ambient-MODERATE — DISCARDED (blindness + base rate, 2026-09-23)

Claim (idea-queue row 1130): when desk reads DEGRADED, ambient tends to read MODERATE
(lift 2.5, 8 occasions / 11 episodes of 567, window 794.2h, collapsed).

Verdict: DISCARD — no fused sense, no reflex. One line why: DEGRADED is a
sensor-blindness verdict (68/70 rows carry UNKNOWN/STALE axes) next to MODERATE, a 35%
base-rate label firing in every hour — blindness beside background noise, not a joint
pattern, and the desk tape is undated so the episode claim is not rebuildable.

Evidence (live, 2026-09-23, read-only):

- `scripts/mesh-correlate --dry` rc=0: no DEGRADED×MODERATE line; `--list` likewise
  empty. The pair does not surface on the current tape; the queued seed is stale.
- Prior verdicts agree twice, independently: 2026-09-08 audit (support came from a
  2026-08-15–17 historical regime, 15/20 rows clustered; MODERATE common 1128/4776;
  DEGRADED×QUIET counter-examples 5/20 break the reading) and 2026-09-18 review
  (DEGRADED = "mixed/unclear" evidence-unavailable label per tool header; MODERATE
  6118/17541 = 34.9% across all 24 hours, weak discriminator; joint timing not
  rebuildable from undated desk-state.log; fusing blindness + noise would mint phantom
  presence — refused per senses charter).
- Usefulness: the remedy for a blind desk axis (re-probe the axis) already exists;
  ambient MODERATE adds no decision.

No tool edited. Receipt left uncommitted for steward landing.
