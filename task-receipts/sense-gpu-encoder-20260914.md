# NVENC encoder utilization sense — 2026-09-14

Status: implemented and live-verified; publication withheld because the required `mesh-doctor`
gate did not complete cleanly.

`scripts/mesh-gpu-encoder` reads NVIDIA's `utilization.encoder` field for each GPU. This is the
hardware video-encoder engine's reported utilization, separate from general GPU utilization and the
already-present GPU fan reading. The tool is on-demand (`# orphan-ok`) until a consumer or sampling
cadence exists. Missing, malformed, or `N/A` values return exit 2; no value is substituted.

Evidence:

- `scripts/mesh-gpu-encoder --json` read a real live driver value: GPU 0 encoder utilization 0%.
- `scripts/mesh-gpu-encoder --test` passed fixture parsing, the `N/A`/exit-2 case, and a real driver
  read.
- `bash tests/test-mesh-gpu-encoder.sh` passed fixture parsing and unavailable-path checks.
- The TDD test was run before implementation and failed because the tool was absent.
- The source is executable (mode 755).

The required `mesh-doctor --quiet` run emitted existing failures for egress riding `tailscale0`
and the configured exit node, plus microphone and peer-SSH warnings. It was still in its remote probe
sweep after 6m43s and was stopped (exit 143); no final summary or orphan-check result was produced.
Therefore doctor cleanliness and absence of a new orphan WARN are **unverified**, and no `[sense]`
board line was posted.

Next action: once the existing doctor blockers are cleared, rerun `mesh-doctor --quiet`; if it exits
cleanly with no new orphan WARN, post `[sense]` with this artifact and the live NVENC reading.
