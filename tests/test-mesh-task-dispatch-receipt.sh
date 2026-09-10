#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh/chains"
printf 'discover\trecord\twrite one durable recorder artifact\n' >"$td/plan.tsv"

cat >"$td/bin/mesh-chat" <<'EOF'
#!/bin/sh
printf '%s\n' "$1" >>"$TEST_BOARD"
EOF
chmod +x "$td/bin/mesh-chat"

env MESH_DIR="$td/mesh" MESH_TASK_DIR="$td/mesh/chains" \
  MESH_TASK_CHAT_CMD="$td/bin/mesh-chat" MESH_TASK_HANDOFF_CMD=/bin/true \
  TEST_BOARD="$td/board" \
  python3 "$repo/scripts/mesh-task" create recorder "$td/plan.tsv" >/dev/null

grep -Fq 'Run: mesh-task take recorder record' "$td/board" || {
  echo 'FAIL: initial chain dispatch did not carry the exact owner claim command' >&2
  exit 1
}

echo 'test-mesh-task-dispatch-receipt: PASS (initial dispatch carries exact take command)'
