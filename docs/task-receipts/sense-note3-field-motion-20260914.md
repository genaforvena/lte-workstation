# Note 3 magnetic field × rotation instrument — 2026-09-14

Added `scripts/mesh-note3-field-motion`, an on-demand paired reader for the Note 3's calibrated
AK09911C magnetic field (HAL type 2) and MPU6500 gyroscope (type 4). The joint sample puts field
vector and angular rate together so later observations can separate field changes during phone
rotation from changes in the magnetic environment. It publishes raw evidence only; no disturbance
label is assigned without a time-aligned corpus. Missing, malformed, stale, or over-skewed inputs
return exit 2. The tool writes no state and declares `# orphan-ok:` because it is on-demand.

`tests/test-mesh-note3-field-motion.sh` passed at 03:06Z. Its `--test` exercises valid/missing/stale
fixtures and requires a real paired HAL read. A separate live `--json` read is saved in
`docs/task-receipts/sense-note3-field-motion-live-20260914.json`:

```json
{"magnetic_field_uT":{"x":0.78,"y":30.48,"z":46.32,"magnitude":55.45431633335677},"angular_velocity_rad_s":{"x":0.00213053,"y":0.00319579,"z":0.0098537,"magnitude":0.01057580424814113},"coverage":"1/1 paired sample","pair_skew_ms":0.0,"pair_age_ms":27.902,"hal_ticks_ns":{"magnetometer":143426502098160,"gyroscope":143426502098160},"source":"Note 3 sensorcat HAL types 2+4"}
```

The first 3-second live probe returned the gyro but no magnetometer event. Source inspection showed
the HAL client emits only sensors that actually delivered an event; a 5-second pair read delivered
both. The instrument therefore uses a 6-second acquisition window, and the required test plus later
standalone read both passed with paired ticks.

## Doctor gate — unresolved

`scripts/mesh-doctor --quiet` started at 03:06:04Z and reported existing hard failures: egress via
`tailscale0` and selected exit node `n2sbt7yy6t11CNTRL`. It also reported the existing default-mic
warning, untimed `mesh-load-audit` peer SSH, six `mesh-song-verify` funnel bypasses, and five
absence-as-negative sites. After 5:21 the smoke sweep was still running a large parallel test tree;
it was interrupted without a final summary. No orphan warning appeared in the emitted output before
interruption, but this is NOT a complete doctor PASS and does not certify a clean orphan census.
Routing was left to its substrate owner. Per the mint gate, no `[sense]` board post was made.

## Next action

The routing/substrate owner resolves the egress and exit-node FAILs; then run `scripts/mesh-doctor
--quiet` to completion. If it exits 0 and has no new orphan WARN, refresh the live reader and post
that paired artifact as `[sense]`.
