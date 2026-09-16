# Genome unblock resolution — `unblock/genome/493bb4ed7d87e6ff/resolve`

Timestamp: `2026-09-16T10:54:27Z`

## Blocked predicate

The parent live-dispatch verification can complete only when an allowlisted managed
GPU service is active **and** an authorized GPU job creates a real free-VRAM shortfall
that exercises preemption/unblock. The first condition is currently satisfied; the
second is not.

## Personally inspected live evidence

- `systemctl --user show ollama.service mesh-room-gigaam.service mesh-voice-clone.service
  -p ActiveState -p SubState -p UnitFileState` reported all three `active/running/enabled`.
- `scripts/mesh-gpu-lease --status` reported `GPU_LEASE=none`.
- `ollama ps` reported resident `qwen3-vl:4b-instruct`, `4.2 GB`, `100% GPU`, with about
  four minutes remaining.
- `nvidia-smi` reported an RTX 3060 with `2897 MiB` free of `12288 MiB`; compute state
  included Ollama `llama-server` using `5350 MiB` and two mesh Python processes using
  `800 MiB` and `2844 MiB`.
- The only current `~/.mesh/heavy-queue/*.job` entries are self-test `touch` jobs with
  `gpu_preempt=0`; they are not authorized production contention jobs and were not
  altered or run as a substitute.
- Existing wiring and focused checks are already documented in
  `docs/task-receipts/operator-model-preemption-verification-20260916.md`.

## Mesh-owned recovery decision

No safe repository or scheduler prerequisite is missing. The services are active and
the lease mechanism is installed; manufacturing contention by changing or launching
the self-test queue would falsify the acceptance event and could consume unrelated GPU
work. No service was stopped, restarted, or reconfigured.

Delegation: `genome-gpu-audit` was launched for a read-only cross-check. It inspected
the receipt and live-state paths but produced no final report; this artifact relies on
the live commands above and my inspection of the source receipt, not on a worker claim.

## Typed external boundary and retry edge

Remain blocked on `external-event`: an authorized GPU job must run while an allowlisted
managed service is active and create a measured free-VRAM shortfall. At that event,
rerun the four focused checks (`python3 tests/test-mesh-gpu-lease.py`,
`scripts/mesh-gpu-lease --test`, `MESH_DIR=<temporary directory> scripts/mesh-heavy-run
--test`, and `bash tests/test-mesh-study-launch.sh`) plus `ollama ps`,
`scripts/mesh-gpu-lease --status`, before/after service and model state, and execution
state; append the resulting preemption/unblock evidence to
`docs/task-receipts/operator-model-preemption-verification-20260916.md`.
