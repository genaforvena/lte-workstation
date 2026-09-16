# Model-preemption live wiring verification — 2026-09-16

## Scope

Owner step: `operator-model-preemption-20260916/verify-live-dispatch-wiring`.

## Wiring inspected

The live study entry point `scripts/mesh-study-launch:60-63` declares the minimum free VRAM,
sets `MESH_HEAVY_GPU_PREEMPT=1`, and invokes `mesh-heavy-run`. The admission path in
`scripts/mesh-heavy-run:109-140,608-622` requests a bounded `mesh-gpu-lease` only for a
GPU-only shortfall, retains the job on failed acquisition, and releases the lease on exit.
`scripts/mesh-gpu-lease:27-32,160-215` limits mutation to the managed-service allowlist and
restores the prior active set. No direct or ambiguous `ollama stop` path was found in the
dispatch or study-launch surfaces.

Source and installed tools matched by SHA-256:

```
mesh-heavy-run  bb6fed3272d562873951f69a05605ab81e2740ad0f2de9392399335d881e8182
mesh-gpu-lease  ff2ea240a269233592ea809e8e00796b4e7b0b9bbe3482f5c1bb366efbe01165
mesh-study-launch 204eb988a48d284ad14ae29bfc27bd635c6979065eded5f9eb4805aea0b28184
```

## Verification evidence

At `2026-09-16T06:34:30Z`, the live probes observed an RTX 3060 with `9102 MiB` free of
`12288 MiB`; `ollama ps` showed its header and no resident model rows. The user services
`ollama.service`, `mesh-room-gigaam.service`, and `mesh-voice-clone.service` were all active
before and after verification. No live model or service was stopped by these checks.

Focused commands and results:

```
python3 tests/test-mesh-gpu-lease.py       PASS
scripts/mesh-gpu-lease --test              PASS
MESH_DIR=<temporary directory> scripts/mesh-heavy-run --test  PASS
tests/test-mesh-study-launch.sh            PASS
```

The isolated heavy-run test exercised the durable GPU queue, bounded selective lease,
restoration, and retry policy. The study-launch test confirmed frozen registration, VRAM retry,
and invocation of the durable heavy queue. This verifies the deployed wiring and its live
non-mutation boundary; no GPU-bound production job was launched because the verification task
does not authorize one.

## Delegation

`genome-preemption-audit` was launched for a read-only repository audit. Its final report was
inspected, but the result is corroborative only; the source paths, hashes, focused tests, and
live probes above were personally inspected and are the completion evidence.

## Result

The preemption mechanism is wired and deployed through the approved heavy-job admission path,
with selective restoration and durable retry. Live production state remained unchanged.
