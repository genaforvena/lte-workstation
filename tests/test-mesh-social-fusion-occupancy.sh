#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-social-fusion"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/state"

fresh() { touch "$td/state/.ambient-level" "$td/state/.presence-state" "$td/state/.activity.state" "$td/state/.social-context.state"; }

printf 'MODERATE\n' > "$td/state/.ambient-level"
printf 'count=2 strongest=phone\n' > "$td/state/.presence-state"
printf 'ACTIVE\n' > "$td/state/.activity.state"
printf 'FAMILY-TIME\n' > "$td/state/.social-context.state"
fresh

out="$(MESH_STATE_DIR="$td/state" "$TOOL" --json)"
printf '%s' "$out" | grep -q '"occupancy":"OCCUPIED"' || { echo "FAIL: joint live pattern must be OCCUPIED: $out"; exit 1; }
printf '%s' "$out" | grep -q '"occupancy_coverage":"3/3"' || { echo "FAIL: occupancy coverage must be overlap: $out"; exit 1; }

printf 'QUIET\n' > "$td/state/.ambient-level"
printf 'count=0 strongest=none\n' > "$td/state/.presence-state"
printf 'IDLE\n' > "$td/state/.activity.state"
fresh
out="$(MESH_STATE_DIR="$td/state" "$TOOL" --json)"
printf '%s' "$out" | grep -q '"occupancy":"EMPTY"' || { echo "FAIL: joint empty pattern must be EMPTY: $out"; exit 1; }

rm "$td/state/.presence-state"
set +e
out="$(MESH_STATE_DIR="$td/state" "$TOOL" --json 2>&1)"
rc=$?
set -e
[ "$rc" -eq 2 ] || { echo "FAIL: unreachable presence must make fusion rc=2, got $rc: $out"; exit 1; }
printf '%s' "$out" | grep -q '"occupancy":"UNKNOWN"' || { echo "FAIL: unreachable presence must be UNKNOWN: $out"; exit 1; }
printf '%s' "$out" | grep -q '"occupancy_coverage":"0/3"' || { echo "FAIL: unreachable presence must have zero overlap: $out"; exit 1; }

# A distinct cross-sense relation: BLE presence × activity × phone social context.
# No single axis can mint an operator state, and the overlap must stay visible.
printf 'count=3 strongest=phone\n' > "$td/state/.presence-state"
printf 'ACTIVE\n' > "$td/state/.activity.state"
printf 'FAMILY-TIME\n' > "$td/state/.social-context.state"
fresh
out="$(MESH_STATE_DIR="$td/state" "$TOOL" --json)"
printf '%s' "$out" | grep -q '"operator_state":"SOCIAL_ENGAGED"' || { echo "FAIL: live 3-axis tuple must derive SOCIAL_ENGAGED: $out"; exit 1; }
printf '%s' "$out" | grep -q '"operator_coverage":"3/3"' || { echo "FAIL: operator coverage must be overlap: $out"; exit 1; }

rm "$td/state/.social-context.state"
set +e
out="$(MESH_STATE_DIR="$td/state" "$TOOL" --json 2>&1)"
rc=$?
set -e
[ "$rc" -eq 0 ] || { echo "FAIL: unrelated core axes should remain assessable, got rc=$rc: $out"; exit 1; }
printf '%s' "$out" | grep -q '"operator_state":"UNKNOWN"' || { echo "FAIL: unreachable social context must be UNKNOWN: $out"; exit 1; }
printf '%s' "$out" | grep -q '"operator_coverage":"0/3"' || { echo "FAIL: unreachable social context must have zero overlap: $out"; exit 1; }
printf '%s' "$out" | grep -q '"social_status":"UNREACHABLE"' || { echo "FAIL: unreachable social context must remain visibly UNREACHABLE: $out"; exit 1; }

echo 'ok: occupancy fusion distinguishes joint occupancy from unreachable input'
