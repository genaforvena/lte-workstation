#!/usr/bin/env bash
set -euo pipefail

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/bin" "$tmp/mesh"
for tool in mesh-board mesh-task mesh-dispatch mesh-chat; do
  printf '#!/bin/sh\nexit 0\n' >"$tmp/bin/$tool"
  chmod +x "$tmp/bin/$tool"
done
printf '#!/bin/sh\nsleep 2\nexit 0\n' >"$tmp/bin/mesh-promises"
chmod +x "$tmp/bin/mesh-promises"

PATH="$tmp/bin:$PATH" MESH_DIR="$tmp/mesh" MESH_CHAT_LOG="$tmp/mesh/chat.log" \
  MESH_WITNESS_PROMISE_STATE="$tmp/mesh/state" MESH_WITNESS_COORDINATION_SUMMARY="$tmp/mesh/summary" \
  "$root/scripts/mesh-witness-promises" >/dev/null 2>&1 &
first=$!
sleep 0.1
if timeout 0.3 env PATH="$tmp/bin:$PATH" MESH_DIR="$tmp/mesh" MESH_CHAT_LOG="$tmp/mesh/chat.log" \
  MESH_WITNESS_PROMISE_STATE="$tmp/mesh/state" MESH_WITNESS_COORDINATION_SUMMARY="$tmp/mesh/summary" \
  "$root/scripts/mesh-witness-promises" >/dev/null 2>&1; then
  :
else
  echo 'FAIL: concurrent auditor waited for the first promise feed instead of skipping' >&2
  kill "$first" 2>/dev/null || true
  wait "$first" 2>/dev/null || true
  exit 1
fi
wait "$first"
set +e
timeout 8s env PATH="$tmp/bin:$PATH" MESH_DIR="$tmp/mesh" MESH_CHAT_LOG="$tmp/mesh/chat.log" \
  MESH_WITNESS_PROMISE_STATE="$tmp/mesh/state" MESH_WITNESS_COORDINATION_SUMMARY="$tmp/mesh/summary" \
  MESH_WITNESS_PROMISE_TIMEOUT=0.1s "$root/scripts/mesh-witness-promises" >/dev/null 2>&1
timed_rc=$?
set -e
[ "$timed_rc" = 1 ] || { echo "FAIL: hung feed was not bounded (rc=$timed_rc)" >&2; exit 1; }
echo 'PASS: witness promise auditor has a non-blocking single-writer guard'
