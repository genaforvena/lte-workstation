# Unblock receipt — genome model preemption verification — 2026-09-16

## Task

`unblock/genome/928dee73a44db3de/resolve` for
`operator-model-preemption-20260916/verify-live-dispatch-wiring`.

## Fresh safe evidence

At `2026-09-16T10:22:49Z`, the live node reported:

```
ollama ps: qwen3-vl:4b-instruct, 100% GPU, 4 minutes remaining
systemctl --user is-active ollama.service mesh-room-gigaam.service mesh-voice-clone.service: active active active
mesh-gpu-lease --status: GPU_LEASE=none
```

No model or service was stopped. The required real contention atom is not present: no
authorized GPU-bound job is running that could create a measured VRAM shortfall. Starting one
solely to manufacture the acceptance event is outside this unblock task's safe authority.

## Wiring checks

All focused checks passed without mutation:

```
python3 tests/test-mesh-gpu-lease.py                         PASS
scripts/mesh-gpu-lease --test                               PASS
MESH_DIR=<isolated temporary directory> scripts/mesh-heavy-run --test  PASS
bash tests/test-mesh-study-launch.sh                         PASS
```

The existing verification receipt remains the source evidence for source/installed hash parity
and the scheduler wiring. This receipt adds the current live state and confirms the lease is not
held.

## Typed block and exact retry edge

Block on `external-event`: an authorized GPU job must run while a managed GPU service is active
and produce a real free-VRAM shortfall. Then rerun the four focused checks plus `ollama ps`,
`mesh-gpu-lease --status`, and before/after service/model state; append the resulting execution
and unblock evidence here before resuming the parent.

## Delegation

`genome-unblock-audit` was assigned a read-only audit. Its prompt submission timed out and no
inspectable report was produced; it was not used as evidence. The receipt and checks above were
personally inspected and executed in this window.
