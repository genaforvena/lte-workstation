#!/usr/bin/env bash
# Regression: an unreadable BLE cache is not the same observation as a real empty scan.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-social-fusion"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/state"

# These are live-enough, successful empty readings.  Presence is deliberately absent.
printf 'QUIET\n' > "$td/state/.ambient-level"
printf 'IDLE\n' > "$td/state/.activity.state"
printf 'SOLO-LEISURE\n' > "$td/state/.social-context.state"

set +e
out="$(MESH_STATE_DIR="$td/state" "$TOOL" --json 2>&1)"
rc=$?
set -e

[ "$rc" -eq 2 ] || { echo "FAIL: missing BLE axis must exit 2, got $rc: $out"; exit 1; }
printf '%s' "$out" | grep -q '"presence":"UNREACHABLE"' || {
  echo "FAIL: missing BLE cache must be visibly UNREACHABLE: $out"; exit 1;
}
printf '%s' "$out" | grep -q '"verdict":"UNCERTAIN"' || {
  echo "FAIL: missing BLE cache must not mint SOLO_QUIET: $out"; exit 1;
}
echo "ok: absent BLE cache is UNREACHABLE, not empty"
