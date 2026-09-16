# Unblock result — genome / model-preemption live dispatch

## Task

`unblock/genome/2ef34af9b062c661/resolve`

Parent: `operator-model-preemption-20260916/verify-live-dispatch-wiring`.

## Decision

The safe mesh-owned prerequisite was re-measured, but the required external event is
still absent. The parent remains typed-blocked; no managed service, model, or unrelated
process was changed.

## Fresh live evidence

Reading time: `2026-09-16T07:10:54Z` UTC.

- `ollama.service`: inactive (rc 3)
- `mesh-room-gigaam.service`: inactive (rc 4)
- `mesh-voice-clone.service`: inactive (rc 4)
- `ollama ps`: `tiny-fleet-v1:latest`, `100% GPU`, approximately four minutes remaining
- `mesh-gpu-lease --status`: `GPU_LEASE=none`
- `nvidia-smi`: GPU 0, 12,288 MiB total, 6,084 MiB used, 5,829 MiB free

This does not satisfy the acceptance predicate: an active managed service plus an
authorized GPU contention job producing a real shortfall. The resident Ollama model is
not by itself authorization to create contention, and starting a service or job merely
to manufacture the event would cross the safety boundary.

## Exact retry edge

When a managed service is active and an authorized GPU job creates a real shortfall,
rerun the focused lease/heavy-run/study-launch checks and capture before/after
`ollama ps`, `mesh-gpu-lease --status`, service state, and execution state; append the
result to `docs/task-receipts/operator-model-preemption-verification-20260916.md`.

## Delegation record

`genome-unblock-audit` was delegated read-only inspection of the unblock chain and
failure evidence. Its report was personally inspected but referenced a stale, different
candidate and changed no files; it was not used as evidence. The live commands above
were run and inspected in this window.
