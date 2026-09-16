# Amendment: TinyFleet S06 capacity admission — 2026-09-15

Supersedes the scheduling wording in
`health-warning-cb9de072194908524114-triage-20260915.md`; the live measurement
and consumer inventory are unchanged.

## Reservation mechanism

The frozen S06 launch path is `scripts/mesh-study-launch`. It invokes:

```text
MESH_HEAVY_GPU_MIN_FREE_MB=2048
MESH_HEAVY_GPU_PREEMPT=1
MESH_HEAVY_GPU_LEASE_TTL=2700
mesh-heavy-run 10240 -- env ... run_study_matrix.py \
  --registration runs/fleet-study-v1/registration.json \
  --run-root runs/fleet-study-v1 \
  --gpu-min-free-mb 2048 --gpu-wait-s 60 --gpu-poll-s 15
```

`mesh-heavy-run` is the reservation/admission owner. Its bounded
`mesh-gpu-lease` may pause only the allowlisted mesh-managed GPU services,
records restoration state before any pause, and restores them on release/TTL;
it does not stop arbitrary workloads. If the declared headroom cannot be
reached, the run remains queued/retryable after restoration. This is an
autonomous capacity decision; no human memory-freeing action is required.

## Safe runnable predicate

For each attempt, immediately before reservation, S06 is runnable exactly when
all of the following hold:

```text
registration.json exists and is the frozen input;
study runner is executable;
mesh-heavy-run is available;
fresh nvidia-smi memory.free probe succeeds with one numeric free_mib;
free_mib >= 2048;
mesh-heavy-run admits the 10240-MiB RAM / 2048-MiB GPU reservation;
the matrix runner's repeated live probe remains free_mib >= 2048.
```

If the probe is failed, missing, non-numeric, or `< 2048 MiB`, or if the
reservation/runner returns its retryable capacity result, defer and retry via
the durable heavy-work queue. Do not convert that state into a study failure.
At the observed `2320 MiB`, the threshold is formally runnable with only
`272 MiB` slack; it is capacity-admitted but fragile, not merely “nonzero”.
