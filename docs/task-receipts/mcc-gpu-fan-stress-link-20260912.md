# MCC link: `mesh-gpu-fan` → `mesh-situation`

Status: implementation and live link verified; `[sense]` publication withheld because the required
`mesh-doctor` gate did not pass. No commit was made.

The situation fusion now reads `mesh-gpu-fan --json` live and publishes `gpu_fan_percent`,
`stress_fan_relation`, and overlap `stress_fan_coverage`. The relation is a context tuple of the live
`mesh-stress` level and NVIDIA driver fan duty; it does not alter posture. The fan producer is required
for machine/edge completeness: missing, malformed, or unreachable fan data renders UNKNOWN and exits
2. Its existing on-demand declaration now documents that `mesh-situation` owns the 15-minute cadence.

Evidence from 2026-09-12:

- `scripts/mesh-situation --test` passed after the change, including a synthetic 2/2 relation and an
  unreachable fan case that returned UNKNOWN, 1/2 overlap, and exit 2.
- `mesh-gpu-fan --test` passed its fixture, N/A exit-2, and real NVIDIA driver read (`fan_speed_percent=0`).
- Live `scripts/mesh-situation --json` returned `gpu_fan_percent="0"`,
  `stress_fan_relation="WARM-GPU-FAN-0%"`, `stress_fan_coverage="2/2"`,
  `axes_total=12`, and exit 0.
- `mesh-doctor` completed with exit 3: 3 FAIL and 33 WARN. The reported FAILs were the live egress
  route using `tailscale0`, an exit-node SPOF, and two recent `fyi-ledger.log` errors. Its orphan gate
  reported 92 stable existing orphans with no new-orphan delta; `mesh-gpu-fan` was absent from the
  doctor orphan and unbacked-exemption state files. Its tool smoke-test section reported all
  applicable checks passing.

Next action: after the existing doctor failures are resolved, rerun `mesh-doctor`; only if it exits 0,
post `[sense] mesh-gpu-fan <-> mesh-situation: live GPU fan duty × node-stress relation (2/2 overlap)`.
