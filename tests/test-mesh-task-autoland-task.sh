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
  MESH_TASK_CHAT_LOG="$td/mesh/chat.log" \
  MESH_CHAT_LOG="$td/mesh/chat.log" \
  MESH_TASK_HANDOFF_CMD=/bin/true \
  MESH_TASK_ACTOR=genome \
  python3 "$repo/scripts/mesh-task" create parser-guard "$td/plan.tsv" >/dev/null

env \
  MESH_DIR="$td/mesh" \
  MESH_TASK_DIR="$td/mesh/chains" \
  MESH_TASK_CHAT_CMD="$td/chat" \
  MESH_TASK_CHAT_LOG="$td/mesh/chat.log" \
  MESH_CHAT_LOG="$td/mesh/chat.log" \
  MESH_TASK_HANDOFF_CMD=/bin/true \
  MESH_TASK_ACTOR=genome \
  python3 "$repo/scripts/mesh-task" take parser-guard implement >/dev/null

env \
  MESH_DIR="$td/mesh" \
  MESH_TASK_DIR="$td/mesh/chains" \
  MESH_TASK_CHAT_CMD="$td/chat" \
  MESH_TASK_CHAT_LOG="$td/mesh/chat.log" \
  MESH_CHAT_LOG="$td/mesh/chat.log" \
  MESH_TASK_HANDOFF_CMD=/bin/true \
  MESH_TASK_ACTOR=genome \
  python3 "$repo/scripts/mesh-task" done parser-guard implement "$repo/scripts/mesh-task" \
    'parser guard verified pane:check' >/dev/null

# Simulate a crash after the board write but before the local completion marker.
python3 - "$td/mesh/chains/parser-guard.json" <<'PY'
import json
import sys
path = sys.argv[1]
with open(path) as handle:
    data = json.load(handle)
data["steps"][0].pop("autoland_task_posted", None)
with open(path, "w") as handle:
    json.dump(data, handle)
    handle.write("\n")
PY

env \
  MESH_DIR="$td/mesh" \
  MESH_TASK_DIR="$td/mesh/chains" \
  MESH_TASK_CHAT_CMD="$td/chat" \
  MESH_TASK_CHAT_LOG="$td/mesh/chat.log" \
  MESH_CHAT_LOG="$td/mesh/chat.log" \
  MESH_TASK_HANDOFF_CMD=/bin/true \
  MESH_TASK_ACTOR=genome \
  python3 "$repo/scripts/mesh-task" done parser-guard implement "$repo/scripts/mesh-task" \
    'parser guard verified pane:check' >/dev/null

grep -q '\[task\].*autoland/parser-guard/implement.*owner: genome' "$td/mesh/chat.log"
grep -q 'Suggested commit subject:.*parser-guard/implement.*parser guard verified' "$td/mesh/chat.log"
grep -q 'Why/context: implement the parser guard' "$td/mesh/chat.log"
grep -q "Artifact: $repo/scripts/mesh-task" "$td/mesh/chat.log"
grep -q 'artifact-sha256:' "$td/mesh/chat.log"
[ "$(grep -c 'autoland/parser-guard/implement' "$td/mesh/chat.log")" = 1 ]

echo 'test-mesh-task-autoland-task: PASS'
