# Note 3 posture × rotation sense — 2026-09-13

The Note 3 HAL exposes two axes not yet represented by a dedicated sense: orientation (HAL type 3)
and gyroscope angular velocity (type 4). Their fresh paired reading distinguishes posture from
rotation through that posture. The on-demand reader publishes raw joint evidence only; it assigns no
uncalibrated activity class and writes no state.

## Live artifact and gate

`tests/test-mesh-note3-posture-rotation.sh` passed at 03:31Z and included a real paired HAL read:

```json
{"orientation_deg":{"azimuth":152.766,"pitch":-41.505,"roll":-62.2404},"angular_velocity_rad_s":{"x":0.000798948,"y":0.00639159,"z":0.0103863,"magnitude":0.012221537068830744},"coverage":"1/1 paired sample","pair_skew_ms":2.428,"pair_age_ms":26.583,"hal_ticks_ns":{"orientation":58188190989414,"gyroscope":58188193417414},"source":"Note 3 sensorcat HAL types 3+4"}
```

The executable source `scripts/mesh-note3-posture-rotation` already has mode 775 and the required
`# orphan-ok:` header. It returns exit 2 when the Note 3, either HAL event, freshness, or alignment is
unavailable. It is stateless, so `mesh-state-touch` does not apply.

## Doctor gate — withheld

`mesh-doctor --quiet` started at 03:32Z and reported two existing hard failures: egress on
`tailscale0` and a selected Tailscale exit node. It then remained blocked for almost three minutes in
`timeout 5 arecord -d 1 /tmp/.doc-mic2.wav`; only that foreground doctor run and its child were
stopped. The scan did not finish, so there is no doctor PASS or completed orphan census and no
`[sense]` post was made. The script's `orphan-ok` header is recognized by `scripts/mesh-doctor`
before an unwired tool can enter the orphan set.

## Next action

After the routing owner resolves the two egress FAILs and the doctor mic probe can complete, run
`mesh-doctor --quiet` to completion. Post the `[sense]` only if it exits 0 with no new orphan WARN,
using the live reader output above (refresh it at posting time).
