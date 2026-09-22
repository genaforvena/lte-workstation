#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

export MESH_STATE_DIR="$td"
export MESH_PRESENCE_LOG="$td/presence.log"
export MESH_ACTIVITY_PRESENCE_LEASE_S=900
export MESH_ACTIVITY_AMBIENT_LEASE_S=600
export MESH_ACTIVITY_ROOM_LEASE_S=900

now="$(date -u +%s)"
iso() { date -u -d "@$1" '+%Y-%m-%dT%H:%M:%SZ'; }

printf 'MODERATE\n' > "$td/.activity.state"
printf 'MODERATE\n' > "$td/.ambient-level"
printf 'PRESENT|dwell_s=10|changes_24h=1\n' > "$td/.room-sense.state"
printf '%s mesh-home n=1 devices=[-58|28:11:A5:B8:9E:A2|speaker]\n' "$(iso "$now")" > "$td/presence.log"

hold="$("$repo/scripts/mesh-activity" --edge --from-cache)"
[ -z "$hold" ] || { echo "FAIL: held edge emitted output: $hold"; exit 1; }

printf 'QUIET\n' > "$td/.ambient-level"
printf '%s mesh-home n=1 devices=[-58|28:11:A5:B8:9E:A2|speaker]\n' "$(iso "$((now + 1))")" > "$td/presence.log"
first="$("$repo/scripts/mesh-activity" --edge --from-cache)"
[ -z "$first" ] || { echo "FAIL: first changed sample emitted before debounce: $first"; exit 1; }

printf '%s mesh-home n=1 devices=[-58|28:11:A5:B8:9E:A2|speaker]\n' "$(iso "$((now + 2))")" > "$td/presence.log"
fire="$("$repo/scripts/mesh-activity" --edge --from-cache)"
case "$fire" in
  *'[activity] AMBIENT'*) : ;;
  *) echo "FAIL: confirmed edge did not emit transition: $fire"; exit 1 ;;
esac

echo 'mesh-activity edge output: PASS'
