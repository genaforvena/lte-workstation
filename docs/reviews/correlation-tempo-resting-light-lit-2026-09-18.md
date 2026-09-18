# CORRELATION tempo-RESTING × light-LIT — DISCARDED (definitional, not a joint pattern)

Claim (idea-queue): when tempo reads RESTING, light tends to read LIT. Task text
quoted lift 1.86 / 9 episodes, re-measured inside light=LIT's 07:00-17:00 band
(full-window 1.8 CONFOUNDED); 8 distinct occasions / 10 episodes of 203, window
876.2h, autocorrelation-collapsed, <1h-apart episodes one occasion.

Verdict: DISCARD — no fused sense, no reflex. One line why: RESTING vs SILENT
IS the light split by construction (wifi=STILL + light=LIT → RESTING,
wifi=STILL + light=DARK → SILENT, scripts/mesh-activity-tempo lines 506-511),
so "RESTING implies LIT" is the verdict reciting its own defining input, not a
JOINT pattern neither axis reaches alone.

Evidence (live, 2026-09-18, read-only):
- `scripts/mesh-activity-tempo` header: `RESTING = tamper=quiet + wifi=STILL +
  light=LIT → lit room, no motion` vs `SILENT = ... + light=DARK → room at rest`
  (lines 21-22, 40-41); code lines 506-511 implement exactly that fork.
- Live tape `~/.mesh/activity-tempo.log`: 185 RESTING rows carry the light input
  IN the row (`light=LIT` 49 / `light=DARK` 71 / `light=UNKNOWN` 65) — the axis
  is a named fusion input of the verdict, same shape as the desk-audio sibling
  (correlation-room-quiet-desk-away-2026-09-18, discarded same day).
- The 71 RESTING-with-DARK rows are the cam=STILL fallback arm (line 523-527:
  camera live + no motion → RESTING regardless of light) and the 65 UNKNOWN rows
  the wifi-STILL-no-context arm (line 512-515) — i.e. even the correlation's own
  exceptions are other arms of the same verdict function, not independent data.
- Base-rate mismatch underneath the lift: light.log reads LIT 94/1191 rows
  (7.9%) on its own cadence vs tempo's 20-min cadence — a lift across two
  different denominators, and the 07:00-17:00 re-measurement keeps only the
  daylight hours when LIT is definitionally available.
- Usefulness: the underlying state "room still and lit" is already directly
  published as the RESTING verdict itself. Fusing RESTING+LIT would mint a
  second name for what tempo already says, and wiring it as a reflex would let
  the light axis vote twice (once inside tempo, once beside it).

Rejected alternative: fuse into a "quiet-and-lit" occupancy verdict. Refused —
redundancy is the case for DELETING an axis, not minting a sense (senses
charter); the pair reaches no state neither axis reaches alone, since one axis
is literally computed from the other.
