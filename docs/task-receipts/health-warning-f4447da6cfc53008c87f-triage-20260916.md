# TinyFleet S06 health-warning triage — 2026-09-16

Task: `health-warning/f4447da6cfc53008c87f/triage` (owner `health`).

## Live evidence

At `2026-09-16T04:22:27Z`, a non-destructive `nvidia-smi` read reported:

```text
GPU 0 NVIDIA GeForce RTX 3060: total=12288 MiB used=8502 MiB free=3411 MiB util=0% temp=47C
```

The frozen S06 minimum is `2048 MiB`, so the current measured slack is
`3411 - 2048 = 1363 MiB`. CUDA consumers were present (800 MiB Python,
5350/2108/108 MiB Ollama processes, and 104 MiB Python); this is available
headroom, not idle capacity. `mesh-voice-clone.service`,
`mesh-room-gigaam.service`, and `ollama.service` were all `active`.

## Wiring and disposition

The inspected launch path remains `scripts/mesh-study-launch` →
`mesh-heavy-run` → `mesh-gpu-lease`. It sets the 2048 MiB minimum, enables the
bounded managed-service lease, and the runner performs fresh repeated probes,
returning retryable `EX_TEMPFAIL` when admission or recheck cannot be met.

Disposition: **resolved for this sample; no service or workload was stopped,
restarted, or preempted.** S06 is formally admissible at this observation,
subject to the launcher's immediate reservation and live recheck. A future
failed/non-numeric probe, free memory below 2048 MiB, or reservation refusal is
queued/retryable rather than a study failure.

Evidence commands: `nvidia-smi --query-gpu=...`,
`nvidia-smi --query-compute-apps=...`, `systemctl --user is-active ...`, and
`rg -n 'MESH_HEAVY_GPU|gpu-min|memory.free|EX_TEMPFAIL|mesh-gpu-lease'
scripts/mesh-heavy-run scripts/mesh-study-launch scripts/mesh-gpu-lease`.
