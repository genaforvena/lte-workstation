# Haunt GPU recovery — 2026-09-16

Task: `operator-gpu-resource-coordination-20260916/verify-haunt-recovery`

## Evidence

- Fresh preflight at `2026-09-16T05:04:10Z`: RTX 3060 had 5,470 MiB free;
  `ollama ps` showed resident `qwen3-vl:4b-instruct` and `all-minilm:latest`.
- First admission attempt correctly returned transient `75` after
  `mesh-voice-clone.service` failed to stop within 60 seconds and queued the
  exact command as `/home/mesh-home/.mesh/heavy-queue/f547806f386da52df6a0833a82c0924e.job`.
- After the operator authorized freeing space, the two resident Ollama models
  were unloaded. The second attempt used `mesh-heavy-run` with
  `MESH_HEAVY_GPU_MIN_FREE_MB=5600`, `MESH_HEAVY_GPU_PREEMPT=1`, and RAM budget
  4096 MiB. It acquired a GPU lease (`196aeb80…`), ran the exact fresh command,
  and exited 0.
- Tape: `/home/mesh-home/src/hyperhauntology_for_kids/runs/tiny-fleet-v1_zy_h2-establishment-3.jsonl`
  (21 lines; SHA-256
  `3c3c02ff2bf696c3e3558e98b5c33bdd92d81c02599dcf9dc744454dbc1be2c0`).
- Independent replay returned `NO-CALLS` for all four families: the derail
  phase produced no answers, so this is not an establishment, null, or H2
  result.
- Lease release reported restoration of `mesh-voice-clone.service`,
  `mesh-room-gigaam.service`, and `ollama.service`. Postflight showed all three
  active, `GPU_LEASE=none`, and 11,908 MiB free.

## Delegation

`haunt-gpu-recovery-audit` performed a read-only audit. I personally inspected
its report against the receipt, canonical task journal, queue file, and live
service/GPU state; the report was advisory and no worker mutation was used as
evidence.

## Disposition

The shared GPU contract is wired and can execute a mesh GPU job after bounded
resource recovery. The fresh model result is `NO-CALLS`, with the next valid
action being a future establishment attempt under a model/runtime that answers
the derail phase. The consumed duplicate queue entry is quarantined beside the
original job file so the automatic drain cannot rerun the same output path.
