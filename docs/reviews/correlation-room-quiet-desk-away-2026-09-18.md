# CORRELATION room_activity-QUIET × desk-AWAY — DISCARDED (redundant, not a joint pattern)

Claim (idea-queue, seed lift:room_activity:desk): when room_activity reads QUIET,
desk tends to read AWAY. Task text quoted lift 6.0 / 8 occasions; the live queue
(2026-09-18) now reads lift 2.05 hour-stratified (raw 2.4 CONFOUNDED), 27 distinct
occasions / 40 episodes of 1446, window 1568.0h — and invariance=UNSTABLE (clears
the 1.8 floor in 2 of 5 environments; env29 alone at 4.56 carries the margin).

Verdict: DISCARD — no fused sense, no reflex. One line why: both axes read the
same microphone (room_activity=QUIET is mic sound-energy; desk-presence fuses
audio=SILENT live-verified 2026-09-18), so the correlation is one sensor agreeing
with itself next to a time-of-day shadow (shadow alone scores 1.38 of 2.4), not a
JOINT pattern neither axis reaches alone.

Evidence (live, 2026-09-18, read-only):
- `mesh-desk-presence`: `LIKELY-AWAY ... [kbd=UNREACHABLE cam_motion=UNKNOWN
  fov=MODERATE cam=OK seat=NOSEAT audio=SILENT]` — audio is a named fusion input
  of the desk verdict, so desk=AWAY already contains the mic reading that
  room_activity=QUIET reports. Shared input = self-correlation by construction.
- `scripts/mesh-room-activity` header: audio axis is "sound energy in..." (mic);
  room_activity=QUIET is a mic-energy label, same organ.
- Idea-queue seed: hour-shadow with room_activity=QUIET's own hour histogram
  scores 1.38 against observed 2.4 — over half the lift is time-of-day profile
  (quiet room at night when nobody is at the desk), and the stratified 2.05 vs
  the 1.8 floor is the whole remaining margin.
- Invariance UNSTABLE: 2/5 environments clear 1.8 (env18 2.04, env29 4.56 on
  nxy=1/5x5); env17 1.50, env20 1.22, env36 1.56 do not. Environment-specific,
  MARKOV blanket only — not generalizable per the tool's own verdict.
- Usefulness: the underlying state "operator absent from desk" is already
  directly sensed (seat=NOSEAT, no logind session). Fusing QUIET+AWAY would mint
  a second name for what desk-presence already says, and wiring it as a reflex
  would let a muted mic vote twice.

Rejected alternative: fuse into an "away-and-quiet" occupancy verdict. Refused —
redundancy is the case for DELETING an axis, not minting a sense (senses charter);
a max()/worst-of fold would just equal one of its parts.
