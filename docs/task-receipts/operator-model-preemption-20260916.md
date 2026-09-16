# Model-preemption audit — 2026-09-16

## Scope

Owner step: `operator-model-preemption-20260916/audit-model-preemption`.

## Measured contention edge

The task dispatcher allocates a mind, but no dispatch path currently owns or coordinates
resident Ollama models. `scripts/mesh-dispatch` and `scripts/mesh-mind-control` decide worker
availability/routing; `scripts/mesh-task` records resource policy text, but neither stops a
model. Model consumers and long-lived services are separate: the live user units
`ollama.service` and `mesh-room-gigaam.service` are active, while `mesh-voice-clone.service`
was transitioning. At 2026-09-16T05:06Z, `ollama ps` showed `qwen3-vl:4b-instruct` and
`all-minilm:latest` resident on GPU; `nvidia-smi` showed 5,470 MiB free of 12,288 MiB.

Models reappear because `ollama.service` is `Restart=always` and model consumers reload them
on demand; stopping an individual model is not a durable coordination contract. The existing
safe boundary is the already-deployed `mesh-gpu-lease`: it snapshots the active allowlist,
stops only `mesh-voice-clone.service`, `mesh-room-gigaam.service`, and `ollama.service`,
measures free VRAM, and restores the exact prior active set on release/expiry or failed acquire.

## Safe contract for the implementation step

At the dispatch edge that launches a GPU-bound mesh consumer, require a declared minimum-free-
VRAM threshold and call `mesh-heavy-run` with `MESH_HEAVY_GPU_PREEMPT=1`. A failed lease is a
typed retry/queue edge; it must not stop an unowned process, kill an ambiguous Ollama model, or
present a permanent operator block. The implementation must preserve protected active consumers,
restore prior service state, and add a mutation-red regression plus a real `ollama ps` check.

## Verification and delegation

Personally inspected the source hooks, live units, `ollama ps`, and GPU read above. The delegated
`genome-model-preemption-audit` worker performed a read-only search but stopped without a
separate inspectable report; its output was not used as proof.
