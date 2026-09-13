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

grep -Fq 'mesh-task done recorder record <artifact> [result]' "$td/board" || {
  echo 'FAIL: initial chain dispatch did not carry the exact structured completion command' >&2
  exit 1
}

grep -Fq 'mesh-task reject recorder record <reason>' "$td/board" || {
  echo 'FAIL: initial chain dispatch did not carry the exact structured rejection command' >&2
  exit 1
}

grep -Fq 'A board [done] line alone does not close the task ledger.' "$td/board" || {
  echo 'FAIL: initial chain dispatch did not distinguish board prose from ledger closure' >&2
  exit 1
}

# Reflexes run with a minimal PATH.  Dispatch must use the mesh-chat installed
# beside mesh-task, rather than silently creating an open row that no mind is
# told about because the interactive-shell PATH happened to be absent.
cp "$repo/scripts/mesh-task" "$td/bin/mesh-task"
chmod +x "$td/bin/mesh-task"
: >"$td/fallback-board"
env PATH=/usr/bin:/bin PYTHONPATH="$repo/scripts" MESH_DIR="$td/fallback-mesh" \
  MESH_TASK_DIR="$td/fallback-mesh/chains" MESH_TASK_HANDOFF_CMD=/bin/true \
  TEST_BOARD="$td/fallback-board" "$td/bin/mesh-task" create fallback "$td/plan.tsv" >/dev/null
grep -Fq '[task] fallback/record' "$td/fallback-board" || {
  echo 'FAIL: sibling mesh-chat fallback did not dispatch under minimal PATH' >&2
  exit 1
}

echo 'test-mesh-task-dispatch-receipt: PASS (dispatch carries exact commands and works without interactive PATH)'
