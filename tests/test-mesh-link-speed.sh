#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-link-speed"

td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/sys/class/net/eth0" "$td/sys/class/net/lo"
printf '1000\n' > "$td/sys/class/net/eth0/speed"
printf -- '-1\n' > "$td/sys/class/net/lo/speed"

out="$(MESH_LINK_SPEED_ROOT="$td/sys/class/net" "$TOOL" --json 2>/dev/null)"
rc=$?
[ "$rc" -eq 0 ] || { echo "fixture read failed rc=$rc"; exit 1; }
printf '%s\n' "$out" | grep -q '"eth0"' || { echo "fixture omitted eth0: $out"; exit 1; }
printf '%s\n' "$out" | grep -q '"speed_mbps":1000' || { echo "fixture speed wrong: $out"; exit 1; }

mkdir -p "$td/empty"
MESH_LINK_SPEED_ROOT="$td/empty" "$TOOL" --json >/dev/null 2>&1
rc=$?
[ "$rc" -eq 2 ] || { echo "empty root must be honest exit 2, got $rc"; exit 1; }

echo "test-mesh-link-speed: PASS"
