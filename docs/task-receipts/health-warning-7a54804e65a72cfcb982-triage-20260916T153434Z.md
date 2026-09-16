# Health warning triage — 2026-09-16T15:34:34Z

Task: `health-warning/7a54804e65a72cfcb982/triage`
Owner: `health`

## Live evidence

- Required `mesh-dash --once check`: timed out with no payload; bounded retry `timeout -k 2s 8s` exited `124`.
- `mesh-load-gate --quiet-hours witness`: exited `1`.
- `/proc/loadavg`: `131.28 126.95 122.65 165/5700 1017758`.
- `/proc/meminfo`: `MemAvailable=10901024 kB`, `SwapTotal=1793332 kB`, `SwapFree=0 kB`.
- `mesh-supervise --status`: exited `0`; `snapshot`, `selfcare`, `dram-bw-sampler`, and `devcd-catch` reported `UP`.
- Owner-authored take was attempted as required:
  `MESH_TASK_ACTOR=health mesh-task take health-warning/7a54804e65a72cfcb982 triage`
  under `timeout -k 2s 30s`; it exited `124` without a ledger result.

## Typed block and retry edge

The exact-owner ledger operation is blocked by node resource pressure / ledger contention, not
by missing authorization. Retry after load and swap pressure normalize: run
`timeout 30s mesh-dash --once check`, require no `PROBE-WARNING: LOCAL LOAD HIGH`, then rerun
`mesh-load-gate --quiet-hours witness` and require exit `0`; only then retry the owner-authored
take and triage the warning.

