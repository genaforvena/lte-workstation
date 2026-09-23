# CORRELATION tempo-SILENT × ambient-MODERATE — DISCARDED (regime shift, 2026-09-23)

Claim (idea-queue row 1186): when tempo reads SILENT, ambient tends to read MODERATE
(lift 3.8, 8 occasions / 8 episodes of 171, window 815.7h, collapsed).

Verdict: DISCARD — no fused sense, no reflex. One line why: SILENT was unreachable
until the light path began producing DARK, so the full-window denominator treated a
short late regime as 34 days of exposure — inside its own era the episode lift is 1.00.

Evidence (live, 2026-09-23, read-only):

- `scripts/mesh-correlate --dry` rc=0: no SILENT×MODERATE line; `--list` likewise
  empty. The pair does not surface on the current tape; the queued seed is stale.
- Prior full verdict (docs/correlation-investigation-tempo-silent-ambient-moderate-spurious-2026-09-08.md):
  producer artifact records the exact queued statistic and its correction (era lift
  1.00; P(MODERATE|readable tempo)=0.972 vs 0.963 when SILENT, lift 0.99); live
  re-audit (4776 rows) shows overlaps concentrated in the 2026-08-15–19 regime with
  phone-unreachable/body-unknown/camera-blind rows while the ambient-clock label stays
  MODERATE — shared availability + short instrument regime, not causation. Label trap:
  this `ambient` column is the BLE-appliance clock, not the microphone; fusing it with
  the activity classifier would amplify the shared-organ confound.
- Regime gate exists precisely for this shape (short-token exposure correction); the
  historical source artifact records its rejection of the original statistic.

No tool edited. Receipt left uncommitted for steward landing.
