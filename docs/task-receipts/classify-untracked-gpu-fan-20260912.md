# GPU fan deployment candidate classification — 2026-09-12

Task: `repo-sync-followups-20260912/classify-untracked-gpu-fan` (owner `genome`).

The task's original premise had changed before this claim: `scripts/mesh-gpu-fan` is tracked at
HEAD commit `0e375216`, so it is no longer an untracked candidate. Its deployed bytes already
matched the committed source, but the deployed path was a regular file instead of the exact
manifest-owned symlink; the report-only `mesh-sync-tools` run still listed it as drift.

Backed up the deployed file to
`/home/mesh-home/.mesh/tools-backup/mesh-gpu-fan.classify-untracked-20260912`, then replaced only
`~/.local/bin/mesh-gpu-fan` with a symlink to
`/home/mesh-home/lte-workstation/scripts/mesh-gpu-fan`. Verified the exact link target and that
source/deployed SHA-256 both equal
`7d98c22c6dd6db331dce6f3166947f191339bc5f771ef1deb8de6c3dcda9559e`.

Verification:

- `scripts/mesh-gpu-fan --test` — PASS, including fixture parsing, N/A exit-2 handling, and a real
  NVIDIA driver read (`gpu_index=0`, `fan_speed_percent=0`).
- `scripts/mesh-sync-tools --test` — PASS, including checked manifest inventory and nested manifest
  parity.
- Fresh report-only `scripts/mesh-sync-tools` — exit 1 because unrelated drift remains; its
  `2026-09-12T16:38:03Z DRIFT:` row no longer contains `mesh-gpu-fan`.
- No global `--apply` was run; the unrelated dirty checkout and drift were left untouched.

Resource decision: this was a local filesystem repair and focused verification; no GPU workload,
remote node, or queued resource slot was needed. The tool's own real hardware read was available.
