# Unblock receipt: live model-preemption verification

- Task: `unblock/genome/e11d1fb18a63ee96/resolve`
- Parent: `operator-model-preemption-20260916/verify-live-dispatch-wiring`
- Checked: `2026-09-16T07:26:29Z` (UTC)

## Current evidence

The safe live predicates are unchanged:

```
systemctl is-active ollama.service mesh-room-gigaam.service mesh-voice-clone.service
inactive
inactive
inactive
systemctl is-enabled ...
masked
not-found
not-found
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader
NVIDIA GeForce RTX 3060, 12288 MiB, 8028 MiB
ollama ps
qwen3-vl:4b-instruct  100% GPU  (expires in about 4 minutes)
all-minilm:latest     100% GPU  (expires in about 3 minutes)
mesh-gpu-lease --status
GPU_LEASE=none
```

Repository and installed wiring were already verified in
`docs/task-receipts/operator-model-preemption-verification-20260916.md`, including the
focused lease, heavy-run, and study-launch tests and matching SHA-256 values.

## Disposition

No mesh-internal code or scheduler prerequisite is missing. Resident Ollama models do not change
the service predicate: all managed service units remain inactive, and no lease or contention
event is active. Activating or unmasking a managed
service, and launching an authorized GPU contention job, would change external runtime state and
is not justified by the current evidence. The exact irreducible atom is:

> An authorized operator/runtime owner must make one managed GPU service active and authorize a
> real GPU-bound contention job that produces a shortfall.

When that atom exists, rerun the four focused checks plus `ollama ps`,
`mesh-gpu-lease --status`, and before/after service/model/execution state; append the real
preemption and unblock result to the parent verification receipt.

## Delegation

`genome-e11d1-audit` was launched as a read-only audit of the same blocker. Its report is a lead
only; this receipt is based on the commands above and the parent receipt inspected locally.
