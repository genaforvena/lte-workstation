#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/task-chains"
cat >"$td/task-chains/complete-chain.json" <<'EOF'
{
  "chain": "complete-chain",
  "status": "complete",
  "current": 1,
  "steps": [
    {"id": "complete-chain/first", "slug": "first", "owner": "genome", "status": "done", "artifact": "/tmp/first.md"},
    {"id": "complete-chain/last", "slug": "last", "owner": "witness", "status": "done", "artifact": "/tmp/last.md"}
  ]
}
EOF

MESH_DIR="$td" MESH_TASK_DIR="$td/task-chains" python3 "$repo/scripts/mesh-task" import >/dev/null
out="$(MESH_DIR="$td" MESH_TASK_DIR="$td/task-chains" python3 "$repo/scripts/mesh-task" audit)"
grep -q $'^DONE\tgenome\tcomplete-chain/first\tartifact=/tmp/first.md$' <<<"$out"
grep -q $'^DONE\twitness\tcomplete-chain/last\tartifact=/tmp/last.md$' <<<"$out"
echo 'test-mesh-task-audit-complete: PASS'
