# MCC closed link: `mesh-stall-coupling` → `mesh-stress` — 2026-09-11

Applied option (b): `mesh-stall-coupling` was a live but under-consumed producer. It reads the
real CPU PSI and memory PSI axes and emits their joint relation; `mesh-stress` now consumes that
live JSON. Only `COUPLED` stalls plus normalized local load above 1.0 raise the advisory `WARM`
precursor. A missing, malformed, or unreachable producer remains `UNKNOWN` and makes machine-facing
stress modes exit 2; no calm or pressure default is fabricated.

Verification:

- `bash -n scripts/mesh-stress` — PASS.
- `scripts/mesh-stall-coupling --test` — PASS, including real CPU/memory PSI read and rc=2 paths.
- `scripts/mesh-stress --test` — PASS, including producer consumption, one-sided negative control,
  joint WARM arm, and malformed-to-UNKNOWN arm.
- `tests/test-mesh-stall-coupling.sh` — PASS.
- Both source files remain executable.
- `rg -l 'mesh-stall-coupling|stall_coupling' scripts/*` now names exactly the producer and
  `scripts/mesh-stress`.

Live end-to-end reads at 2026-09-11T19:07:59Z:

```text
producer rc=0
{"relation":"CALM","cpu_some_avg10":3.42,"memory_some_avg10":0.00,...}

consumer rc=0
..."stall_coupling_state":"CALM","stall_coupling_cpu_avg10":"7.59","stall_coupling_memory_avg10":"0.00","stall_coupling_joint":"no"...
```

The producer was sampled again by the consumer, so its live PSI values changed between reads; both
are real readings, and the consumer preserved the producer relation rather than inventing a value.

Doctor gate: `timeout 180s mesh-doctor --quiet` returned rc=124 after reporting the pre-existing
`egress rides tailscale0` and `exit-node set` FAILs, plus existing mic, peer-SSH, sole-path, and
absence-as-negative WARNs. No new orphan warning for this link appeared. The required clean doctor
gate was therefore not met, so no `[sense]` board post was made.

No commit was made. Exact next action: resolve the existing doctor FAILs, rerun
`mesh-doctor --quiet` to a completed clean result, then post
`[sense] closed producer↔consumer: mesh-stall-coupling → mesh-stress (CPU PSI × memory PSI × heavy local load)`.
