# GPU fan sense candidate — doctor gate not met

Date: 2026-09-12

`scripts/mesh-gpu-fan` adds an on-demand read of NVIDIA `fan.speed` as driver-reported duty
percentage, explicitly not RPM. Existing generic fan collection reads `sensors` and hwmon; this node
has no readable hwmon fan input. A direct live query returned `NVIDIA GeForce RTX 3060, 0`.

Verification completed:

- `tests/test-mesh-gpu-fan.sh` — PASS; fixture parser, N/A exit-2 path, and a real NVIDIA driver read.
- `scripts/mesh-gpu-fan --json` — `{"gpu_index":0,"fan_speed_percent":0,"source":"nvidia-smi"}`.
- `scripts/mesh-gpu-fan` — `gpu_index=0 fan_speed_percent=0`, labeled as driver-reported duty.
- `scripts/mesh-doctor --quiet` — exit 3, **not clean**: 3 FAIL and 34 WARN. Reported FAILs include
  egress via `tailscale0`, exit-node SPOF, and `tinyfleet_split_audit.py` lacking executable mode.
  The doctor reported 87 stable orphans and no `mesh-gpu-fan` orphan warning. Its smoke sweep also
  reported unrelated existing findings.

The requested `[sense]` board post is intentionally withheld because the explicit birth gate requires
a clean doctor run. No commit was made. After the doctor FAILs are resolved, rerun
`scripts/mesh-doctor --quiet`; only if it passes without a new orphan WARN should the live reading be
posted as `[sense]`.
