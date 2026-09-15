#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh/chains"
printf 'alpha\tfirst\tproduce the predecessor artifact\nbeta\tsecond\tconsume the handoff\n' >"$td/plan.tsv"
printf 'handoff fixture\n' >"$td/artifact"

cat >"$td/bin/mesh-chat" <<'EOF'
#!/bin/sh
printf '%s\n' "$1" >>"$TEST_BOARD"
EOF
cat >"$td/bin/mesh-handoff" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >>"$TEST_HANDOFF"
EOF
chmod +x "$td/bin/mesh-chat" "$td/bin/mesh-handoff"

base=(MESH_DIR="$td/mesh" MESH_TASK_DIR="$td/mesh/chains"
  MESH_TASK_CHAT_CMD="$td/bin/mesh-chat" MESH_TASK_HANDOFF_CMD="$td/bin/mesh-handoff"
  TEST_BOARD="$td/board" TEST_HANDOFF="$td/handoff")
env "${base[@]}" MESH_TASK_ACTOR=alpha python3 "$repo/scripts/mesh-task" create demo "$td/plan.tsv" >/dev/null
env "${base[@]}" MESH_TASK_ACTOR=alpha python3 "$repo/scripts/mesh-task" take demo first >/dev/null
env "${base[@]}" MESH_TASK_ACTOR=alpha python3 "$repo/scripts/mesh-task" done demo first "$repo/scripts/mesh-task" verified >/dev/null

grep -Fq '/clear' "$td/handoff"
grep -Fq 'C-m' "$td/handoff"
grep -Fq 'tmux send-keys -t <pane> C-m' "$td/handoff"

echo 'test-mesh-task-handoff-reset-instruction: PASS (handoff returns /clear plus tmux C-m submit)'
