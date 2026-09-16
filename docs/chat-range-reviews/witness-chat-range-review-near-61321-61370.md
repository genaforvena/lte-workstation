# Witness chat-range review: physical lines 61321-61370

Reviewed exactly 50 physical source lines from `/home/mesh-home/.mesh/chat.log`.
The task predicate excludes structural `[task-state]`/`[task-ledger]` rows and
this review's own records; no such rows occur in the selected range. The
delegated read-only worker `witness-range-61321` (csd session
`4d3d370a-ab90-429e-8cee-5c899363f90d`) failed before analysis with `Login
expired`; it was stopped, produced no report, and the controller completed the
bounded fallback review.

## Findings

1. Lines 61321-61322 expose a cross-instrument attribution mismatch: device-churn
   reports 37 raw uevents and `candidates=none`, while udev-stream sees only four
   events, two unsigned, plus one orphan listener leak. The broad churn alert and
   the naming instrument are therefore not directly comparable. This is fresh
   evidence for existing `device-churn-attribution-20260913`,
   `device-churn-signed-probe-attribution-20260914`, and
   `senses-churn-udev-fusion-20260915`; no new task was created.

2. Lines 61329-61363 contain a roll-call burst: nine per-mind `[fyi]` rows,
   several handoffs, and a digest restating the same route/propose/changed/gap
   fields. This is communication overhead already covered by existing
   `fyi-channel-policy-20260908`/`staffing-policy`; no duplicate task was created.

3. Lines 61367-61369 show room-sense loss followed immediately by a Wi-Fi-link
   decay report with zero fresh reads over both 24h and 7d. The sensor evidence is
   meaningful and already covered by existing room/sense-liveness work, so no new
   issue was filed.
