# Cross-sense fusion live verification — 2026-09-10T21:01Z

Existing tool: `scripts/mesh-social-fusion` (executable, `orphan-ok`; no new tool file or
wiring change was needed).

Focused verification passed:

- `tests/test-mesh-social-fusion-occupancy.sh`
- `tests/test-mesh-social-fusion-unreachable.sh`
- `tests/test-mesh-social-fusion-coupling-audit.sh`
- `scripts/mesh-social-fusion --test`
- `mesh-autowire --test`
- `mesh-doctor --test`

Fresh real read:

```text
rc=2
{"verdict":"UNCERTAIN","reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","relation":"UNKNOWN","coverage":"0/3","social_relation":"UNKNOWN","social_coverage":"0/4","occupancy":"UNKNOWN","occupancy_coverage":"0/3","occupancy_reason":"unavailable axis: ambient=LIVE presence=STALE activity=LIVE","operator_state":"UNKNOWN","operator_coverage":"0/3","operator_reason":"unavailable axis: presence=STALE activity=LIVE social=LIVE","coupling_audit":"COUPLING-DOMINANT-CANDIDATE","local_coverage":"2/3","coupling_recovery_s":"na","ambient":"QUIET","ambient_status":"LIVE","ambient_age_s":"72","presence":"STALE","devices":"UNKNOWN","presence_age_s":"998637","activity":"UNCERTAIN","activity_status":"LIVE","activity_age_s":"313","social":"DEGRADED","social_status":"LIVE","social_age_s":"231","ts":"2026-09-10T21:01:13Z"}
```

This proves the derived relations are not a single-axis fold and that stale/unreachable BLE is
visible and cannot mint `EMPTY` or an all-clear. The focused empty fixture separately proves a live
`count=0` presence read derives `occupancy=EMPTY`.

Full `mesh-doctor` was run with a 180-second bound and exited `124` before completing its tool-parse
sweep. Completed output showed pre-existing node failures for egress over `tailscale0` and the
configured exit node, plus an untimed peer-SSH warning for `mesh-load-audit`; no new orphan warning
was reported. Because the required full doctor PASS was not achieved, no `[sense]` board post was
made.
