#!/usr/bin/env bash
set -euo pipefail

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/bin" "$tmp/mesh"
printf '2026-09-08T07:00:00Z  raw@test  ::  [fyi] source\n' >"$tmp/mesh/chat.log"
cat >"$tmp/bin/mesh-task" <<'EOF'
#!/bin/sh
sleep 2
exit 0
EOF
chmod +x "$tmp/bin/mesh-task"

PATH="$tmp/bin:$PATH" MESH_DIR="$tmp/mesh" \
  MESH_WITNESS_COORDINATION_SUMMARY="$tmp/mesh/summary" \
  "$root/scripts/mesh-task-journal" >/dev/null 2>&1 &
first=$!
sleep 0.1
if ! timeout 0.3 env PATH="$tmp/bin:$PATH" MESH_DIR="$tmp/mesh" \
  MESH_WITNESS_COORDINATION_SUMMARY="$tmp/mesh/summary" \
  "$root/scripts/mesh-task-journal" >/dev/null 2>&1; then
  echo 'FAIL: concurrent task replay waited instead of skipping' >&2
  kill "$first" 2>/dev/null || true
  wait "$first" 2>/dev/null || true
  exit 1
fi
wait "$first"

set +e
PATH="$tmp/bin:$PATH" MESH_DIR="$tmp/mesh" \
  MESH_WITNESS_COORDINATION_SUMMARY="$tmp/mesh/summary" \
  MESH_WITNESS_TASK_TIMEOUT=0.1s "$root/scripts/mesh-task-journal" >/dev/null 2>&1
timed_rc=$?
set -e
[ "$timed_rc" = 1 ] || { echo "FAIL: hung task audit was not bounded (rc=$timed_rc)" >&2; exit 1; }
echo 'PASS: witness task replay has a non-blocking single-writer guard'
