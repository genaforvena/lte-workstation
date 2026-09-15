# Wake GPU VRAM blocker recheck — 2026-09-14

## Result

The exact-owner resolver `unblock/wake/4e2802e65ca808df/resolve` was taken by
`wake` and checked against the live RTX 3060 state. No safe mesh-owned memory
release action was available, so the live-score task remains blocked pending a
safe capacity window. No process was stopped and no score was started.

## Evidence

- `mesh-dash --once wake` at 2026-09-14 18:33:53 UTC showed no lane run in
  flight, 0% GPU utilization, and 11,525 MiB GPU memory in use.
- `nvidia-smi` at 18:34:26 UTC showed 11,525 / 12,288 MiB in use (763 MiB
  free), allocated to `mesh-room-gigaam` (800 MiB),
  `mesh-voice-clone-daemon` (3,264 MiB), and two Ollama servers (2,800 MiB and
  4,634 MiB).
- `nvidia-smi` at 18:35:02 UTC showed 8,720 / 12,288 MiB in use (3,568 MiB
  free). The 2,800 MiB Ollama server had exited; the remaining allocations were
  `mesh-room-gigaam` (800 MiB), `mesh-voice-clone-daemon` (3,264 MiB), and an
  Ollama `llama-server` (4,634 MiB).
- `mesh-task check resume
  wake-live-score-validation-20260914/live-score-existing-rung wake` returned
  exit 2, so the original validation is not eligible to resume yet.

The remaining allocations belong to live mesh audio/inference services. Their
owners were not part of this wake task, and stopping them is not a safe
mesh-owned prerequisite. Free VRAM also varied by 2,805 MiB in under a minute,
so a single free-memory reading does not establish a stable enough window for
the existing Qwen load plus retained scoring logits.

## Retry

Retry the existing live-score task only after its resume check passes and a
fresh capacity observation establishes enough stable VRAM for Qwen plus the
scoring forward pass. Do not evict the resident services to manufacture that
window.
