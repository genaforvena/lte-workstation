#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-social-fusion"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/state"

printf 'MODERATE\n' > "$td/state/.ambient-level"
printf 'count=3 strongest=phone\n' > "$td/state/.presence-state"
printf 'ACTIVE\n' > "$td/state/.activity.state"
printf 'SOCIAL-ONLINE\n' > "$td/state/.social-context.state"
touch "$td/state/.ambient-level" "$td/state/.presence-state" "$td/state/.activity.state" "$td/state/.social-context.state"

rm "$td/state/.ambient-level" "$td/state/.presence-state" "$td/state/.activity.state"
out="$(MESH_STATE_DIR="$td/state" "$TOOL" --coupling-audit --json)"
printf '%s' "$out" | grep -q '"coupling_audit":"COUPLING-DOMINANT-CANDIDATE"' || { echo "FAIL: candidate: $out"; exit 1; }
printf '%s' "$out" | grep -q '"local_coverage":"0/3"' || { echo "FAIL: local coverage: $out"; exit 1; }
printf '%s' "$out" | grep -q '"social_status":"LIVE"' || { echo "FAIL: social status: $out"; exit 1; }
printf '%s' "$out" | grep -Eq '"(ambient|presence|activity|social)_age_s":"(na|[0-9]+)"' || { echo "FAIL: ages: $out"; exit 1; }

printf 'MODERATE\n' > "$td/state/.ambient-level"
printf 'count=3 strongest=phone\n' > "$td/state/.presence-state"
printf 'ACTIVE\n' > "$td/state/.activity.state"
touch "$td/state/.ambient-level" "$td/state/.presence-state" "$td/state/.activity.state"
out="$(MESH_STATE_DIR="$td/state" "$TOOL" --coupling-audit --json)"
printf '%s' "$out" | grep -q '"coupling_audit":"RECOVERED"' || { echo "FAIL: recovery: $out"; exit 1; }
printf '%s' "$out" | grep -Eq '"coupling_recovery_s":"[0-9]+"' || { echo "FAIL: recovery duration: $out"; exit 1; }

out="$(MESH_STATE_DIR="$td/state" "$TOOL" --json)"
printf '%s' "$out" | grep -q '"operator_state":"SOCIAL_ENGAGED"' || { echo "FAIL: normal fusion: $out"; exit 1; }
echo 'ok: coupling audit distinguishes partner dominance and local recovery'
