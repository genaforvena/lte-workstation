#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/home/.mesh" "$td/bin"
cat > "$td/bin/mesh-chat" <<'EOF_CHAT'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "${MESH_LAND_CHAT_CAPTURE:?}"
EOF_CHAT
chmod +x "$td/bin/mesh-chat"
: > "$td/chat"
: > "$td/trace"

run_post() {
  HOME="$td/home" PATH="$td/bin:/usr/bin:/bin" \
    MESH_REPO="$repo_root" \
    MESH_DIR="$td/home/.mesh" MESH_LAND_CHAT_CAPTURE="$td/chat" \
    MESH_LAND_BOARD_TRACE="$td/trace" \
    bash "$repo_root/scripts/mesh-land" --test-board-post "$1" "$2"
}

run_post done artifact-sha-1
run_post done artifact-sha-1
run_post health-fail artifact-sha-1
run_post health-fail artifact-shared

[[ "$(wc -l < "$td/chat")" -eq 2 ]]
grep -Fxq 'done artifact-sha-1' "$td/chat"
grep -Fxq 'health-fail artifact-shared' "$td/chat"
[[ "$(grep -Fc 'repeat signature=artifact-sha-1' "$td/trace")" -eq 2 ]]

echo 'mesh-land idempotent output: PASS'
