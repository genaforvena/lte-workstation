# CORRELATION desk-DEGRADED × ambient-MODERATE — DISCARDED (spurious/unactionable)

Claim (idea-queue): when desk reads DEGRADED, ambient tends to read MODERATE
(lift 2.5, 8 occasions / 11 episodes of 567, window 794.2h, collapsed).

Verdict: DISCARD — no fused sense, no reflex. One line why: DEGRADED is a
sensor-blindness verdict (68/70 rows carry UNKNOWN/STALE axes), MODERATE is a
35%-base-rate label at all hours, n=8 occasions cannot carry a new sense, and
the desk tape is undated so the episode claim is not rebuildable from source.

Evidence (live corpus, 2026-09-18, read-only):
- `~/.mesh/desk-state.log`: 6351 dated `[desk-state]` rows; 70 DEGRADED (all
  `DEGRADED:signals`). Axis census over the 70: body=UNKNOWN 42, tamper=UNKNOWN
  40, cam=STALE 62 — 68/70 carry at least one blind axis. Per the tool's own
  header, DEGRADED = "both axes available but mixed/unclear": it names
  unavailable evidence, not an occupancy state.
- `~/.mesh/ambient-db-tape.tsv`: 17541 rows / 1567h. Labels:
  QUIET 6645, MODERATE 6118 (34.9%), LOUD 2728, SILENCE 2044, UNREACHABLE 6.
  MODERATE fires in every hour 0–23 (126–360/h) — a weak discriminator; any
  common condition will "co-occur" with it.
- Joint timing is NOT rebuildable: desk-state.log rows carry no timestamps, so
  "11 episodes / 8 occasions" cannot be re-derived from the two named tapes;
  the claim's provenance is unverifiable from source.
- Usefulness: the remedy for a blind desk axis already exists (re-probe the
  axis); ambient MODERATE adds no decision. Not a JOINT pattern neither axis
  reaches alone (senses charter) — it is one axis's blindness next to the
  room's commonest mid-level label.

Rejected alternative: fuse "desk-blind + room-noisy" into a presence verdict.
Refused — presence must come from positive evidence (typing, recognized face,
corroborated motion); blindness + background noise is exactly how a phantom
"someone is here" gets minted.
