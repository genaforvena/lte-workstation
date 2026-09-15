#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh"
printf '#!/bin/sh\nprintf fired\\n >>"$FIRED"\n' >"$td/bin/materialize"
chmod +x "$td/bin/materialize"
: >"$td/mesh/chat.log"

FIRED="$td/fired" MESH_TASK_WATCH_LOCK="$td/task-watch.lock" \
  "$repo/scripts/mesh-task-watch" --window 4 --debounce 0 \
  "$td/mesh/chat.log" -- "$td/bin/materialize" >/dev/null 2>&1 &
watcher=$!
sleep 0.4
printf '2026-09-08T07:00:00Z  test  ::  [task-state] fixture\n' >>"$td/mesh/chat.log"
for _ in $(seq 1 20); do
  [[ -s "$td/fired" ]] && break
  sleep 0.1
done
kill "$watcher" 2>/dev/null || true
wait "$watcher" 2>/dev/null || true
grep -q fired "$td/fired" || {
  echo 'FAIL: chat.log write did not trigger task materialization' >&2
  exit 1
}
echo 'PASS: task watcher fires materialization from a chat.log write'
