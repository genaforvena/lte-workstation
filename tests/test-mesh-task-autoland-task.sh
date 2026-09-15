#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/mesh/chains"
printf 'genome\timplement\timplement the parser guard\n' >"$td/plan.tsv"
printf 'verified parser artifact\n' >"$td/artifact.md"
printf '%s\n' '#!/usr/bin/env bash' 'printf "%s\\n" "$1" >>"$MESH_TASK_CHAT_LOG"' >"$td/chat"
chmod +x "$td/chat"

env \
  MESH_DIR="$td/mesh" \
  MESH_TASK_DIR="$td/mesh/chains" \
  MESH_TASK_CHAT_CMD="$td/chat" \
  MESH_TASK_CHAT_LOG="$td/chat.log" \
  MESH_TASK_HANDOFF_CMD=/bin/true \
  MESH_TASK_ACTOR=genome \
  python3 "$repo/scripts/mesh-task" create parser-guard "$td/plan.tsv" >/dev/null

env \
  MESH_DIR="$td/mesh" \
  MESH_TASK_DIR="$td/mesh/chains" \
  MESH_TASK_CHAT_CMD="$td/chat" \
  MESH_TASK_CHAT_LOG="$td/chat.log" \
  MESH_TASK_HANDOFF_CMD=/bin/true \
  MESH_TASK_ACTOR=genome \
  python3 "$repo/scripts/mesh-task" take parser-guard implement >/dev/null

env \
  MESH_DIR="$td/mesh" \
  MESH_TASK_DIR="$td/mesh/chains" \
  MESH_TASK_CHAT_CMD="$td/chat" \
  MESH_TASK_CHAT_LOG="$td/chat.log" \
  MESH_TASK_HANDOFF_CMD=/bin/true \
  MESH_TASK_ACTOR=genome \
  python3 "$repo/scripts/mesh-task" done parser-guard implement "$repo/scripts/mesh-task" \
    'parser guard verified' >/dev/null

env \
  MESH_DIR="$td/mesh" \
  MESH_TASK_DIR="$td/mesh/chains" \
  MESH_TASK_CHAT_CMD="$td/chat" \
  MESH_TASK_CHAT_LOG="$td/chat.log" \
  MESH_TASK_HANDOFF_CMD=/bin/true \
  MESH_TASK_ACTOR=genome \
  python3 "$repo/scripts/mesh-task" done parser-guard implement "$repo/scripts/mesh-task" \
    'parser guard verified' >/dev/null

grep -q '\[task\].*autoland/parser-guard/implement.*owner: genome' "$td/chat.log"
grep -q 'Suggested commit subject:.*parser-guard/implement.*parser guard verified' "$td/chat.log"
grep -q 'Why/context: implement the parser guard' "$td/chat.log"
grep -q "Artifact: $repo/scripts/mesh-task" "$td/chat.log"
grep -q 'artifact-sha256:' "$td/chat.log"
[ "$(grep -c 'autoland/parser-guard/implement' "$td/chat.log")" = 1 ]

echo 'test-mesh-task-autoland-task: PASS'
