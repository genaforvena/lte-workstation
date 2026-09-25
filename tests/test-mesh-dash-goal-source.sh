#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
cache="$td/.goal-tg.cache"
printf 'unchanged goal\n' > "$cache"

observed(){
  MESH_DIR="$td" MESH_DASH_GOAL_TTL=99999 "$ROOT/scripts/mesh-dash" --once tg \
    | sed -n 's/^goal-source=\(FRESH\|STALE\|UNKNOWN\) · .*/\1/p'
}
assert_state(){
  local actual
  actual="$(observed)"
  [ "$actual" = "$1" ] || { printf 'FAIL: goal source wanted %s, got %s\n' "$1" "$actual" >&2; exit 1; }
}
touch -d '6 minutes ago' "$cache"
assert_state STALE
touch -d '10 seconds ago' "$cache"
assert_state FRESH
rm "$cache"
assert_state UNKNOWN
printf 'test-mesh-dash-goal-source: PASS (stale, recovery, missing without repaint reset)\n'
