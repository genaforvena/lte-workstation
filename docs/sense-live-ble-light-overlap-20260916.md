# Live BLE × webcam-light overlap — 2026-09-16

## Measurement

This is an observation artifact, not a persisted perception state. The two axes were sampled on
`mesh-home` during one bounded window:

```text
presence command: timeout 30s mesh-presence --fresh --json
presence start:   2026-09-16T10:13:59Z
presence record:  2026-09-16T10:14:08Z
presence rc:      0
presence:         status=ok count=9 known=10 personal_presence=ACTIVE_NEAR familiarity=FAMILIAR
                  proximity=NEAR:3,ROOM:6 attribution=personal:5,appliance:2,ambiguous:2

light command:    timeout 60s mesh-light --test
light start:      2026-09-16T10:14:17Z
light rc:         0
light live line:  DIM mean=84.0 median=40.0 stddev=85.1 p10=23 p90=241 spread=218 scene=localized
uvc artifact:     ~/.mesh/uvc-metadata/latest.bin, 2992 bytes, mtime 2026-09-16 10:14:58Z
light state read: ~/.mesh/.light-state -> DIM|source=webcam|scene=localized|spread_luma=228|frame_age_s=0
```

The BLE record and the webcam record overlap within the 18-second command-start window (and the
fresh UVC artifact is inside the light probe). Both organs returned real reads, so this is not a
partial/unknown result. The measured joint pattern is:

```text
JOINT_OBSERVED: ACTIVE_NEAR (BLE) + DIM/localized (webcam)
```

This measurement does not promote the pair to a new semantic verdict: it establishes one live,
heterogeneous joint observation while keeping each axis' own label and coverage visible. It does
not claim that dim light causes presence or that presence explains the scene.

## Gate evidence

`mesh-presence --fresh --json` returned a fresh structured scan with nine devices and rc=0.
`mesh-light --test` returned rc=0 and explicitly reported a live webcam artifact, including frame
statistics and scene quality. The UVC artifact was non-empty and fresh. An unavailable organ would
have been recorded as `UNKNOWN/PARTIAL`; neither occurred in this window.

## Delegation record

A read-only sensor-surface audit was delegated to `senses-sensor-audit`. I inspected its completed
transcript with `read-turn --full`; it identified `scripts/mesh-arrivals`' missing real BLE assertion
and cited `scripts/mesh-arrivals`, `~/.mesh/reflexes.cron`, and the stale/fresh arrivals artifacts.
That report was advisory only and did not alter this measurement or claim the task.
