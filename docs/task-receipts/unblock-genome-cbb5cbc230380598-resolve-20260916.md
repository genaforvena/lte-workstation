# Unblock receipt: live model-preemption verification retry

- Task: `unblock/genome/cbb5cbc230380598/resolve`
- Parent: `operator-model-preemption-20260916/verify-live-dispatch-wiring`
- Checked: `2026-09-16T09:53:54Z` (UTC)

## Mesh-owned prerequisite work

The current source and deployed tools were rechecked, then all four focused wiring gates were
run. Every gate passed:

```
python3 tests/test-mesh-gpu-lease.py       PASS
scripts/mesh-gpu-lease --test              PASS
MESH_DIR=<temporary directory> scripts/mesh-heavy-run --test  PASS
bash tests/test-mesh-study-launch.sh       PASS
```

The source/deployed SHA pairs also matched for `mesh-heavy-run`, `mesh-gpu-lease`, and
`mesh-study-launch`. No source or scheduler change is missing from this unblock.

## Fresh live state

At the check time all three managed services were active and enabled:

```
ollama.service             active / enabled
mesh-room-gigaam.service   active / enabled
mesh-voice-clone.service   active / enabled
```

The RTX 3060 reported `3187 MiB` free of `12288 MiB`; `ollama ps` showed
`qwen3-vl:4b-instruct` at `100% GPU`; and `mesh-gpu-lease --status` reported `GPU_LEASE=none`.
The active-service predicate is therefore now satisfied, but no authorized GPU contention job
was present and no preemption/unblock event occurred.

## Disposition

The mesh-owned prerequisite is verified and the parent wiring remains intact. The remaining
irreducible external atom is an already-authorized GPU-bound job that creates a real shortfall.
Do not manufacture that event by stopping services, changing masks, or launching synthetic load.
When that atom exists, rerun the four focused gates plus `ollama ps`, `mesh-gpu-lease --status`,
and before/after service/model/execution state; append the resulting preemption/unblock evidence
to `docs/task-receipts/operator-model-preemption-verification-20260916.md`.

## Delegation

No subagent was launched: this retry was one tightly coupled owner/substrate verification, and
claiming, live-state reads, tests, artifact writing, and task disposition stayed in this window.
