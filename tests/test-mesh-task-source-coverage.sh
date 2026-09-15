#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh"
cat >"$td/bin/mesh-promises" <<'EOF'
#!/bin/sh
case "${1:-}" in --feed|--check) exit 0;; *) exit 2;; esac
EOF
cat >"$td/bin/mesh-board" <<'EOF'
#!/bin/sh
exit 0
EOF
cat >"$td/bin/mesh-task" <<'EOF'
#!/bin/sh
exit 0
EOF
cat >"$td/bin/mesh-dispatch" <<'EOF'
#!/bin/sh
exit 0
EOF
chmod +x "$td/bin"/*
printf '2026-09-08T07:00:00Z  raw@test  ::  [fyi] ordinary prose\n' >"$td/mesh/chat.log"
printf '2026-09-08T07:00:01Z  raw@test  ::  binary event\n' >>"$td/mesh/chat.log"
printf '2026-09-08T07:00:02Z  raw@test  ::  [task-state] not a valid structured record\n' >>"$td/mesh/chat.log"
MESH_DIR="$td/mesh" MESH_CHAT_LOG="$td/mesh/chat.log" \
MESH_WITNESS_COORDINATION_SUMMARY="$td/mesh/summary" \
MESH_WITNESS_PROMISE_STATE="$td/mesh/state" PATH="$td/bin:$PATH" \
  "$repo/scripts/mesh-task-journal" >/dev/null

grep -Eq '^source_events=3 replayed_events=3 source_errors=1 source_bytes=[0-9]+ source_sha256=[0-9a-f]{64}$' "$td/mesh/summary"
echo 'test-mesh-task-source-coverage: PASS (all chat.log records replayed and hashed)'
