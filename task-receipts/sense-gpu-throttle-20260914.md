# GPU clock-reason sense — 2026-09-14

Added the on-demand `scripts/mesh-gpu-throttle` reader for the RTX 3060's
`nvidia-smi` `clocks_throttle_reasons.active` bitmask. The existing GPU readers cover activity,
display, fan duty, power, temperature, clocks, and power limiting; none queried this driver reason
mask. The driver help describes it as the active clock-event-reason bitmask. The reader preserves
that raw mask and does not infer a cause from temperature or clock rate. It writes no state and
returns exit 2 if the driver value is absent or malformed.

The new source is executable and declares `# orphan-ok: on-demand ...`; this is a manual live read,
not a scheduled reflex, so no cadence or state artifact is declared. `tests/test-mesh-gpu-throttle.sh`
checks active and zero masks, unavailable and `N/A` exit-2 paths, and invokes the source's `--test`.
The `--test` checks a fixture and then requires a real NVIDIA driver read.

## Verification

- Test-first red: `rtk bash tests/test-mesh-gpu-throttle.sh` exited 127 before the source existed.
- Green: `rtk bash -n scripts/mesh-gpu-throttle tests/test-mesh-gpu-throttle.sh` and
  `rtk bash tests/test-mesh-gpu-throttle.sh` passed.
- The self-test completed a real driver read at `2026-09-14T07:16:56Z` with
  `gpu_index=0 active_mask=0x0000000000000000 active=false`; the standalone JSON read at the same
  second returned the same value. An earlier real read at `07:10:58Z` returned mask `0x1`, showing
  the sampled driver state can change.
- Source mode is `-rwxrwxr-x`.
- `rtk scripts/mesh-doctor --quiet` found the existing egress-on-`tailscale0` and selected-exit-node
  failures, plus existing microphone, peer-SSH, funnel-bypass, and absence-as-negative warnings. The
  full concurrent smoke sweep had no completion summary after five minutes and was stopped with
  exit 130. The orphan census was therefore not reached; a clean doctor PASS and no-new-orphan-WARN
  result are **not established**.
- No `[sense]` board post and no commit were made.

Next action: the routing/exit-node substrate owner resolves the two doctor FAILs; then run
`rtk scripts/mesh-doctor --quiet` to a complete summary. Post
`[sense] mesh-gpu-throttle: nvidia-smi active clock-reason mask ...` only after it exits 0 and the
completed orphan census contains no new orphan WARN.
