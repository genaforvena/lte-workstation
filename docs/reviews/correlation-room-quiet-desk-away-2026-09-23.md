# CORRELATION room_activity-QUIET × desk-AWAY — DISCARDED (live gate drop, 2026-09-23)

Claim (idea-queue row 1252, seed lift:room_activity:desk): when room_activity reads QUIET,
desk tends to read AWAY (lift 6.0, 8 occasions / 16 episodes of 787, window 832.2h).

Verdict: DISCARD — no fused sense, no reflex. One line why: the tool's own hour-shadow gate
drops this exact pair on the live tape (stratified lift 1.71 < 1.8 floor; time-of-day profile,
not structure), confirming three prior discards (2026-08-18, 2026-09-08, 2026-09-18) — both
axes share the same microphone and the night regime, so the correlation is one sensor agreeing
with itself, not a joint pattern.

Evidence (live, 2026-09-23, read-only):

```
2026-09-23T03:52:46Z mesh-correlate: hour-shadow: DROPPED room_activity=QUIET <-> desk=AWAY
(lift 2.09, 40 episodes) — a shadow with room_activity=QUIET's exact hour-of-day histogram
and NO relation to desk already scores 1.42 of the observed 2.43 (n=255); hour-stratified
lift is 1.71 < 1.8 — time-of-day profile, not structure
```

- `scripts/mesh-correlate --dry` rc=0: "no correlation/prediction meets thresholds
  (need more data — honest empty, not a failure)". The candidate never reaches the queue
  on current data; the queued row is a stale seed.
- Prior art agrees independently: 2026-09-18 review (shared-mic self-correlation + 1.38/2.4
  shadow + UNSTABLE invariance 2/5 envs), 2026-09-08 audit (37 episodes, stratified 2.32 vs
  shadow 1.52, env-carried), 2026-08-18 (two finder defects exposed).
- No tool edited: the hour-shadow/occasion gates that kill this pair already exist and fired.
  No fused sense (would mint a second name for what desk-presence already says) and no reflex
  (would let a muted mic vote twice). Receipt left uncommitted for steward landing.
