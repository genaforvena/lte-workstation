# Shared GPU lease coordination — 2026-09-16

## Scope

Owner step: `operator-gpu-resource-coordination-20260916/diagnose-and-repair-shared-gpu-lease`.

The shared repair was already present in commit `ec96272f` before this task was dispatched;
no unrelated dirty paths were changed. The implementation is deployed: source and installed
SHA-256 values match for both `scripts/mesh-gpu-lease` and `scripts/mesh-heavy-run`.

## Evidence

- Live GPU at 2026-09-16T04:56:11Z: RTX 3060, 12,288 MiB total, 9,250 MiB used,
  2,663 MiB free.
- `ollama ps` showed resident `qwen3-vl:4b-instruct`, `gemma4:e2b-it-qat`, and
  `all-minilm:latest`; `ollama.service` is active. `mesh-gpu-lease --status` reported
  `GPU_LEASE=none` after the expiry sweep restored `mesh-voice-clone.service`,
  `mesh-room-gigaam.service`, and `ollama.service`.
- `scripts/mesh-gpu-lease` records restoration intent before stopping services, stops only
  the allowlisted mesh services, returns `75` when managed release cannot reach the threshold,
  and restores prior active state on release/expiry.
- `scripts/mesh-heavy-run` enters the lease only for GPU-only shortfall with
  `MESH_HEAVY_GPU_PREEMPT=1`; refused acquisition is queued with the GPU threshold,
  preemption flag, and TTL, and the drain retries the same policy. External processes are
  never in the allowlist.

## Verification

Green:

```text
mesh-gpu-lease --test: PASS
python3 tests/test-mesh-gpu-lease.py: PASS
scripts/mesh-heavy-run --test: ok (... GPU lease ... queued GPU preemption ...)
```

Mutation-red: a temporary copy with the lease-admission branch replaced by `if false; then`
failed its own regression at `smoke-test: FAIL (GPU lease was not acquired and restored around
the admitted job)` with exit 1. The repository source was not mutated by this proof.

## Disposition

The existing shared contract satisfies this step's acceptance condition: temporary GPU scarcity
becomes a bounded lease/queue retry, managed services restore their prior state, and unrelated
GPU processes remain protected. The dependent haunt, adint, wake, cross-owner, and Telegram
steps remain open for their owners.

Delegation record: `genome-gpu-lease-audit` was launched for an independent read-only wiring
audit. It stopped without a separate inspectable report, so its output was not used as evidence;
all evidence above was personally inspected.
