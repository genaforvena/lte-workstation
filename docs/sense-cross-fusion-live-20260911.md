# Cross-sense fusion live verification — 2026-09-11

Tool: `scripts/mesh-social-fusion` (existing executable, `orphan-ok`; no new tool file).

Focused verification:

- `tests/test-mesh-social-fusion-occupancy.sh` — pass
- `tests/test-mesh-social-fusion-unreachable.sh` — pass
- `tests/test-mesh-social-fusion-coupling-audit.sh` — pass
- `scripts/mesh-social-fusion --test` — pass
- source mode: `755` (`-rwxr-xr-x`)

Live read at `2026-09-11T01:46:45Z` (`scripts/mesh-social-fusion --json`, exit `2`):

```json
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","social_relation":"UNKNOWN","social_coverage":"0/4","occupancy":"UNKNOWN","occupancy_coverage":"0/3","occupancy_reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","operator_state":"UNKNOWN","operator_coverage":"0/3","operator_reason":"unavailable axis: presence=STALE activity=LIVE social=LIVE","coupling_audit":"COUPLING-DOMINANT-CANDIDATE","local_coverage":"2/3","coupling_recovery_s":"na","ambient":"QUIET","ambient_status":"LIVE","ambient_age_s":"44","presence":"STALE","devices":"UNKNOWN","presence_age_s":"1015768","activity":"UNCERTAIN","activity_status":"LIVE","activity_age_s":"44","social":"DEGRADED","social_status":"LIVE","social_age_s":"262","ts":"2026-09-11T01:46:45Z"}
```

This is an honest partial result: the stale BLE axis is visibly distinct from a live empty
(`devices=0`, `presence_status=LIVE`), and the required occupancy/operator relations abstain.

Full `mesh-doctor` was not clean on this node: pre-existing egress/exit-node failures and the
default-microphone-busy warning remained. Therefore no `[sense]` board post was made.
