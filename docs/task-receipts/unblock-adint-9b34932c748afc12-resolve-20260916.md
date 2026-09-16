# Unblock receipt — `unblock/adint/9b34932c748afc12/resolve`

Recorded: 2026-09-16T10:13:30Z
Owner: `adint`
Parent: `unblock/genome/cbb5cbc230380598/resolve`

## Fresh verification

The four mesh-owned wiring gates passed:

```text
python3 tests/test-mesh-gpu-lease.py       PASS
scripts/mesh-gpu-lease --test              PASS
MESH_DIR=<temporary> scripts/mesh-heavy-run --test  PASS
bash tests/test-mesh-study-launch.sh       PASS
```

Live resource evidence:

```text
RTX 3060: 12288 MiB total, 9012 MiB used, 2901 MiB free, 0% GPU
GPU_LEASE=none
ollama.service inactive
mesh-room-gigaam.service inactive
mesh-voice-clone.service inactive
```

`ollama ps` showed `qwen3-vl:4b-instruct` at 100% GPU. Existing `mesh-heavy-run`
drain/test processes were present, but no already-authorized GPU-bound contention job
produced a real VRAM shortfall while the managed services were active. No service,
model, lease, or external process was stopped or reconfigured.

## Disposition and retry edge

This is a typed `external-event` block. The parent acceptance condition needs an
already-authorized GPU-bound job to create a genuine shortfall while the managed services
are active. Do not manufacture contention or stop services to create the event. When that
event exists, rerun the four gates above plus `ollama ps`, `mesh-gpu-lease --status`, and
before/after service/model/execution checks, then append the result to
`docs/task-receipts/operator-model-preemption-verification-20260916.md`.

## Delegation record

`adint-9b349-audit` performed a read-only audit. Its report was personally inspected and
matched the parent receipt's boundary: no qualifying contention event exists. The worker
made no task, board, file, or mesh-state changes.
