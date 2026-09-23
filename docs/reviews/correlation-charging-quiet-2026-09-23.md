# CORRELATION body_power-CHARGING × ambient-QUIET — DISCARDED (clock hole, 2026-09-23)

Claim (idea-queue row 1396): when body_power reads CHARGING, ambient tends to read QUIET
(lift 2.26, 20 episodes, era-restricted; 8 occasions / 20 episodes of 212, window 877.2h).

Verdict: DISCARD — no fused sense, no reflex. One line why: CHARGING piles into the 06–09
and 18–22 high-QUIET shoulders while ambient's own producer renames deep-night quiet to
NIGHT-QUIET (P(QUIET|00–05) = 0 by construction), so the lift is the clock's hole, not a
joint pattern — hour-stratified 1.37 < 1.8 floor.

Evidence (live, 2026-09-23, read-only):

- `scripts/mesh-correlate --dry` rc=0: the CHARGING×QUIET pair does not surface at all on
  the current tape — 18 DROPPED rows, no CHARGING×QUIET line in --dry or --list. The queued
  seed is stale; the live tape's own gates already refuse it.
- Prior full verdict (docs/correlation-investigation-body-power-charging-ambient-quiet-spurious-2026-08-20.md):
  hour-matched shadow scores 1.62 of the 2.22 crude lift; stratified 1.37 < 1.8 floor;
  mechanism in producer source (`scripts/mesh-ambient-clock:1019` QUIET→NIGHT-QUIET rename
  23:00–05:00); discriminating control (FULL 2.59 / DISCHARGING 1.57 / LOW 0.00) rules out
  "phone readable" as the driver. That verdict additionally built the hour-shadow gate
  (red-then-green: `tape-hourhole.tsv` episode-lift 2.0 → stratified 1.00, drops loudly).
- Usefulness: the underlying state "phone on charger in a quiet room morning/evening" is
  already directly readable from each axis; fusing them would mint a second name for a
  clock coincidence, and a reflex on it would fire on the household schedule, not a signal.

No tool edited: the hour-shadow gate that kills this shape already exists and the live
re-test confirms the refusal. Receipt left uncommitted for steward landing.
