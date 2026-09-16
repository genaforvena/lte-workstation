# adint unblock receipt: GPU contention prerequisite remains absent

- Task: `unblock/adint/25914c9df507c40e/resolve`
- Parent: `unblock/genome/e11d1fb18a63ee96/resolve`
- Checked: `2026-09-16T08:34:13Z` (UTC)
- Delegation: none. This was kept local because it is one tightly coupled live-resource
  verification edge; a second runner could duplicate GPU ownership or alter the evidence.

## Fresh live evidence

Commands were run from `/home/mesh-home/lte-workstation`:

```text
nvidia-smi --query-gpu=timestamp,index,name,memory.used,memory.free,memory.total,utilization.gpu --format=csv,noheader
2026/09/16 08:34:13.670, 0, NVIDIA GeForce RTX 3060, 2909 MiB, 9004 MiB, 12288 MiB, 0 %

ollama ps
NAME    ID    SIZE    PROCESSOR    CONTEXT    UNTIL

mesh-gpu-lease --status
GPU_LEASE=none

mesh-gpu-lease --test
mesh-gpu-lease --test: PASS (fixture coverage is in tests/test-mesh-gpu-lease.py)

systemctl --type=service --state=running | rg -i 'ollama|gpu|cuda|llm|model'
no matching managed systemd service (exit 1)

ps -eo pid,user,comm,args | rg -i 'ollama|cuda|python.*(train|gpu)|vllm'
337075 mesh-ho+ ollama /usr/local/bin/ollama serve
```

## Decision

The local GPU has 9004 MiB free and the lease is idle, but there is no authorized contention
job creating a real shortfall. The only matching resident process is `ollama serve`; `ollama ps`
has no loaded model, and no managed systemd GPU service is present. Therefore the required
verification cannot honestly run now. No process was stopped, no service was changed, and no
synthetic contention was started.

This is a typed external block, not a test success. Retry only when both conditions are true:
an allowlisted managed GPU service is active, and an authorized GPU job creates a measurable
VRAM shortfall; then rerun the focused dispatch/wiring checks with before/after `ollama ps`,
`mesh-gpu-lease --status`, service state, and execution state.
