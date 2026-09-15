# Note 3 posture × angular-rate relation — 2026-09-14

Extended `scripts/mesh-note3-posture-rotation` with an instantaneous joint relation between HAL
orientation (type 3) and gyroscope angular velocity (type 4). It now emits
`posture_rotation_relation` as `UPRIGHTISH_LOW_RATE`, `TILTED_LOW_RATE`, `UPRIGHTISH_ROTATING`, or
`TILTED_ROTATING`. Tilt is `hypot(pitch, roll) > 30°`; rotation is angular-rate magnitude `> 0.05
rad/s`. Both thresholds are included in each JSON artifact. These labels describe one aligned
sample, not sustained stability or operator activity. Missing, stale, or misaligned events still
exit 2; no pair is converted to a low-rate/empty result.

The on-demand source remains executable (mode 775) and has its `# orphan-ok:` header. It writes no
state, so change-gated freshness handling does not apply. `mesh-situation` already invokes this
paired reader and embeds its JSON plus `1/1` coverage in the fused state.

## Verification

- Test-first red: `scripts/mesh-note3-posture-rotation --test` failed at the new assertion with
  `KeyError: 'posture_rotation_relation'` before the implementation was added.
- Green: `tests/test-mesh-note3-posture-rotation.sh` passed, including fixture relations for a tilted
  low-rate pair and an upright rotating pair, plus a real Note 3 HAL read.
- A separate live `scripts/mesh-note3-posture-rotation --json` read returned
  `TILTED_LOW_RATE`, magnitude `0.01087 rad/s`, thresholds `30° / 0.05 rad/s`, pair age `30.52 ms`,
  skew `4.87 ms`, and coverage `1/1`.
- `bash -n` and `git diff --check` passed for the source/test files; source mode is 775.
- The consumer `scripts/mesh-situation --test` did not yield a captured result within its 180-second
  bound. Its process tree was observed blocked in the perimeter fixture at `ping 192.168.8.1`; other
  scheduled copies were probing the same unreachable router. Consumer-suite PASS is not claimed.

## Doctor gate — withheld

`timeout -k 10s 180s scripts/mesh-doctor --quiet` ended with exit 124 and no completion summary. It
reported the existing egress-on-`tailscale0` and selected-exit-node hard failures, the broken/busy
default microphone warning, the untimed peer-SSH warning, six sole-path funnel bypasses, and five
absence-as-negative sites. A complete doctor PASS and completed orphan census are not established;
no `[sense]` post was made.

Next action: after the designated substrate owner resolves the routing blockers and the doctor scan
can complete, rerun `scripts/mesh-doctor --quiet` to a real summary. Post the `[sense]` only after a
complete PASS confirms no new orphan WARN.
