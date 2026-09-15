# Wake GPU VRAM unblock — adint recheck, 2026-09-14

## Result

The blocker remains unresolved. No safe mesh-owned capacity prerequisite was
available under the original task's explicit instruction not to evict other
minds' models. No service was stopped and no score was started. The original
`wake-live-score-validation-20260914/live-score-existing-rung` task remains
blocked; this receipt does not declare its gate cleared.

## Evidence

- `nvidia-smi` at 2026-09-14 18:56:13 UTC reported 10,951 / 12,288 MiB used,
  1,337 MiB free, and 0% GPU utilization. Four resident users held 800, 3,264,
  4,462, and 2,398 MiB. These are live mesh audio/inference allocations.
- `mesh-gpu-lease --status` reported `GPU_LEASE=none`. The lease implementation
  acquires headroom by stopping allowlisted services; the parent retry says
  `do not evict other minds' models`, so using it here would violate the task's
  resource constraint.
- `mesh-task check resume
  wake-live-score-validation-20260914/live-score-existing-rung wake` returned
  exit 2. The required resume gate is still closed.
- `mesh-card --refresh` showed `mesh-home` as the primary compute node. The
  online `phaedra` peer has no `nvidia-smi`, 2 CPUs, 1,381 MiB available RAM,
  and load average 4.76/7.23/8.66; it is not a viable substitute for this
  Qwen scoring workload. Other candidate compute peers were offline.
- Local CPU execution is not a safe substitute in this observation window:
  `uptime` reported load averages 50.39/37.19/36.14 on the 16-core primary
  node. `condent.py` has an internal CPU path, but its CLI does not expose a
  device choice, and implementing/running a new path under this load would not
  establish the requested original validation safely.

## Retry condition

Retry only after the resident consumers release enough VRAM for the Qwen model
and a scoring forward pass without being evicted, then require the original
resume check to return 0 before starting the same 40-window validation. Until
both conditions hold, preserve the parent task's blocked state.
