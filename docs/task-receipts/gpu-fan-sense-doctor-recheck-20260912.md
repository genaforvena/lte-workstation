# GPU fan sense doctor recheck — 2026-09-12

The live GPU fan sense and its `mesh-situation` stress relation are implemented. The requested
`[sense]` board publication remains withheld because the required full doctor gate did not pass.

Verification:

- `scripts/mesh-gpu-fan --test` — PASS; fixture parse, unavailable `N/A` exit 2, and a real NVIDIA
  driver read.
- `scripts/mesh-gpu-fan --json` — `{"gpu_index":0,"fan_speed_percent":0,"source":"nvidia-smi"}`.
  The value is driver-reported duty percentage, not RPM.
- `scripts/mesh-doctor --quiet` completed at `2026-09-12T15:32:39Z` with exit 2: 2 FAIL, 34 WARN.
  FAILs: egress rides `tailscale0`; exit node `n2sbt7yy6t11CNTRL` is a SPOF.
- Orphan gate: 92 unwired/non-canonical tools confirmed stable; `mesh-gpu-fan` was not named, so
  the new sense introduced no orphan WARN. Existing unrelated orphan-exemption and inverse-orphan
  warnings remain.

No routing change was made because routing is substrate-owned by the active VPN mind. No `[sense]`
was posted and no commit was made. Next: after the VPN owner resolves the doctor egress/exit-node
FAILs, run `rtk mesh-doctor --quiet`; post the recorded live fan/stress relation only if it exits 0
with no new orphan WARN.
