# Model-preemption implementation — 2026-09-16

## Scope

Owner step: `operator-model-preemption-20260916/implement-model-preemption`.

## Implemented contract

The existing landed implementation uses `scripts/mesh-heavy-run` as the GPU-bound admission
edge. When RAM admission is clear but measured free VRAM is below the declared
`MESH_HEAVY_GPU_MIN_FREE_MB`, `MESH_HEAVY_GPU_PREEMPT=1` requests a bounded
`mesh-gpu-lease`. A lease stops only the allowlisted managed services in
`scripts/mesh-gpu-lease`, records restoration intent before the first stop, and restores the
previously active set on release, expiry, failed capacity, or failed acquisition. Ambiguous or
unmanaged processes are not targeted. A failed lease returns `EX_TEMPFAIL` and preserves the
job in the durable heavy-job queue, including the GPU policy for retry.

## Evidence personally inspected

- `scripts/mesh-heavy-run:109-140,608-622` — GPU-only eligibility, typed retry, token release,
  and queue behavior.
- `scripts/mesh-gpu-lease:27-32,160-215` — explicit service allowlist, pre-write restoration
  record, selective stop, capacity rollback, and exact restore.
- `tests/test-mesh-gpu-lease.py` — selective preemption, protected inactive service state,
  rollback, and expiry restoration.
- Live `ollama ps` at 2026-09-16T05:34Z — three resident models were observed:
  `qwen3-vl:4b-instruct`, `all-minilm:latest`, and `qwen3.5:4b`.

## Verification

- `python3 tests/test-mesh-gpu-lease.py` — PASS.
- `scripts/mesh-gpu-lease --test` — PASS.
- `MESH_DIR=<isolated temporary directory> scripts/mesh-heavy-run --test` — PASS.

The first heavy-run test attempt used the live default queue and was blocked by an already
running drain over the node's large historical queue; the isolated rerun passed. No live model
or service was stopped by this verification.

## Delegation record

A read-only repository audit was delegated to `genome-preemption-audit`. The worker stopped after
tool activity without producing a separate inspectable report; its output was not used as proof.
All completion evidence above was inspected directly in the repository or produced by the listed
commands.
