#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-social-fusion"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/state"

fresh() {
  touch "$td/state/.ambient-level" "$td/state/.presence-state" \
    "$td/state/.activity.state" "$td/state/.audio-path-state"
}

printf 'MODERATE\n' > "$td/state/.ambient-level"
printf 'count=1 strongest=phone\n' > "$td/state/.presence-state"
printf 'ACTIVE\n' > "$td/state/.activity.state"
printf 'AUDIBLE\n' > "$td/state/.audio-path-state"
fresh
out="$(MESH_STATE_DIR="$td/state" "$TOOL" --json)"
printf '%s' "$out" | grep -q '"media_relation":"MEDIA_AUDIBLE"' || {
  echo "FAIL: live presence+activity+audio must derive MEDIA_AUDIBLE: $out"
  exit 1
}
printf '%s' "$out" | grep -q '"media_coverage":"3/3"' || {
  echo "FAIL: media relation must report overlap coverage: $out"
  exit 1
}

rm "$td/state/.audio-path-state"
set +e
out="$(MESH_STATE_DIR="$td/state" "$TOOL" --json 2>&1)"
rc=$?
set -e
[ "$rc" -eq 0 ] || { echo "FAIL: unrelated core axes remain assessable, got rc=$rc: $out"; exit 1; }
printf '%s' "$out" | grep -q '"media_relation":"UNKNOWN"' || {
  echo "FAIL: unreachable audio must not mint a media state: $out"
  exit 1
}
printf '%s' "$out" | grep -q '"audio_status":"UNREACHABLE"' || {
  echo "FAIL: unreachable audio must remain visible: $out"
  exit 1
}
printf '%s' "$out" | grep -q '"media_coverage":"0/3"' || {
  echo "FAIL: unreachable audio must zero media overlap: $out"
  exit 1
}

echo 'ok: media fusion distinguishes audible playback from unreachable audio'
