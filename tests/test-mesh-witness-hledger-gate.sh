#!/usr/bin/env bash
# Historical filename: the witness gate is now the task replay/audit gate.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh"
printf 'old valid view\n' >"$td/mesh/coordination.summary"
printf '2026-09-08T07:00:00Z  raw@test  ::  [fyi] source\n' >"$td/mesh/chat.log"

cat >"$td/bin/mesh-task" <<'EOF'
#!/bin/sh
echo 'synthetic task audit failure' >&2
exit 7
EOF
chmod +x "$td/bin/mesh-task"

if PATH="$td/bin:$PATH" MESH_DIR="$td/mesh" \
  MESH_WITNESS_COORDINATION_SUMMARY="$td/mesh/coordination.summary" \
  "$repo/scripts/mesh-task-journal" >"$td/stdout" 2>"$td/stderr"; then
  echo 'FAIL: witness accepted a failed task audit' >&2
  exit 1
fi
grep -q '^old valid view$' "$td/mesh/coordination.summary"
grep -q 'mesh-task audit failed' "$td/stderr"
echo 'test-mesh-witness-hledger-gate: PASS (task audit failure preserves last valid view)'
