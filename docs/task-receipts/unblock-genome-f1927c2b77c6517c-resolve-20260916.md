# Genome unblock resolution — `unblock/genome/f1927c2b77c6517c/resolve`

Observed: `2026-09-16T11:12:43Z`

## Blocked predicate

The parent `operator-model-preemption-20260916/verify-live-dispatch-wiring` can
complete only after an authorized GPU job runs while an allowlisted managed GPU
service is active and creates a measured free-VRAM shortfall. The implementation
and deployed wiring are already verified; the real preemption/unblock event is not.

## Live evidence personally inspected

- `systemctl --user show ollama.service mesh-room-gigaam.service mesh-voice-clone.service -p ActiveState -p SubState -p UnitFileState`: all three reported `active/running/enabled`.
- `ollama ps`: resident `qwen3-vl:4b-instruct`, `4.2 GB`, `100% GPU`, expiring in about two minutes.
- `mesh-gpu-lease --status`: `GPU_LEASE=none`.
- `nvidia-smi`: RTX 3060, `2210 MiB` free of `12288 MiB`; compute processes included Ollama `llama-server` using `5350 MiB` and mesh Python processes using `800 MiB`, `2844 MiB`, and `790 MiB`.
- The only non-terminal queue entry is `7d7578b6e525843d7e238b8e9f2720b8.running`; its job is `touch /tmp/tmp.3fypaQCj8P/lease-ran`, with `gpu_preempt=1`, and repeated `rc=75` headroom retries. It is a self-test touch job, not an authorized production contention job, and was not altered or used as a substitute.
- Existing parent evidence in `docs/task-receipts/operator-model-preemption-verification-20260916.md` records the focused tests, source/installed hashes, scheduler wiring, and the same acceptance boundary.

## Mesh-owned decision

No repository, scheduler, dependency, or service prerequisite is missing. Stopping
or reconfiguring the active services, or manufacturing contention with the self-test
queue, would consume unrelated work and falsify the acceptance event. No mutation was
performed.

Delegation: `genome-unblock-audit` was assigned a read-only cross-check. Its relay
submission timed out and produced no final report; the worker's earlier transcript
was not used as evidence. I personally inspected the parent receipt and corroborated
the live state with the commands above.

## Typed external boundary and retry edge

Disposition: `external-event` block remains honest and actionable. Retry when an
authorized GPU job is admitted while an allowlisted managed service is active and
the job records a real free-VRAM shortfall. Then rerun:

```text
python3 tests/test-mesh-gpu-lease.py
scripts/mesh-gpu-lease --test
MESH_DIR=<temporary directory> scripts/mesh-heavy-run --test
bash tests/test-mesh-study-launch.sh
ollama ps
scripts/mesh-gpu-lease --status
systemctl --user show ollama.service mesh-room-gigaam.service mesh-voice-clone.service -p ActiveState -p SubState -p UnitFileState
nvidia-smi
```

Append before/after service, model, lease, and execution evidence to
`docs/task-receipts/operator-model-preemption-verification-20260916.md`, then resume
the parent verification. The unblock step is complete as a typed block; it does not
claim the parent capability was achieved.
