# Mesh resource autonomy — 2026-09-11

## Policy

Temporary local resource pressure is a scheduling condition, not a reason to declare a task
impossible or return the choice to the operator. Heavy jobs retain their command, working directory,
resource thresholds, and latest headroom evidence in the durable queue. The recurring
`mesh-heavy-drain` retries deferred jobs; non-resource failures remain visible as failed evidence
instead of being retried or discarded without limit. A workload must not kill or displace shared
consumers to obtain capacity.
`mesh-home` is the explicit primary compute node (`MESH_PRIMARY_COMPUTE=mesh-home`); its live resource
gate still admits work from current headroom rather than treating the role declaration as proof of
capacity.

## Live evidence

- `mesh-heavy-run --test`: passed its resource-gate, preflight, serialization, and queue-path tests.
- `mesh-heavy-drain --test`: passed; it verifies a recurring drain exists for resource-deferred jobs.
- Installed crontab contains `*/2 * * * * ... mesh-heavy-drain --run`.
- `mesh-study-launch --test`: passed with frozen registration SHA256
  `2498cc3146b673751f15106d39c31b059188c9af60668dfa6998e00eb5e230ba`, RAM budget 10240 MB,
  and minimum free VRAM 2048 MiB.
- At observation, the local RTX 3060 reported 2341 MiB free of 12288 MiB (0% utilization), above
  the study launcher's admission threshold. No study was launched by this verification.

## Current study limitation

The S06 chain remains blocked at `run-paired-replications` (step 27/42). The active Tiny Fleet runner
is still uncommitted and its own S06 implementation receipt lists missing trained adapters and an
incomplete training/execution path. That is a real implementation prerequisite, not evidence that
the GPU is unavailable. The runner currently labels execution as training even though its shown path
only evaluates adapters that already exist; do not treat its smoke or current untracked state as a
completed replication.

The resource mechanism here queues/retries on the primary node. A read-only fleet check at 2026-09-11
23:15 UTC found no safe alternative for this study. `MESH_ROLES` lists `phaedra:compute` and Tailscale
reports it online, but it has only 1962 MiB total RAM (1317 MiB available), far below this launcher's
10240 MiB budget; `nvidia-smi` and `mesh-resource-guard` are unavailable there, so GPU/headroom
admission cannot be proven either. The other configured compute peers (`ilya`, `default-string`,
`server`, `ideapad`) were offline; the online Mac is configured as an organ, not compute. So “try
another node” is not currently justified by fresh eligible capacity evidence; this study stays in the
durable local retry queue. Cross-node placement needs fresh headroom publication and verified remote
execution semantics before it can safely claim or use capacity.

## Exact next action

The S06 owner must finish and land a real, immutable-registration training-plus-evaluation runner,
including the missing adapter production path and raw per-seed artifacts. Then invoke
`mesh-study-launch`; temporary resource deferrals should remain queued for the existing drain. The
independent verifier should run only after the full artifact exists. Do not report S06 complete from
resource-gate tests alone.
