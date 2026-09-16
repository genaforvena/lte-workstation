#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tool="$repo/scripts/mesh-nic-rx-nohandler"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/home/.mesh" "$tmp/sys/physical/device" "$tmp/sys/physical/statistics"
printf '23\n' > "$tmp/sys/physical/statistics/rx_nohandler"

out=$(HOME="$tmp/home" MESH_RX_NOHANDLER_SYS_NET="$tmp/sys" \
  "$tool" --test 2>&1)
grep -q 'REAL physical rx_nohandler=23' <<<"$out"

out=$(HOME="$tmp/home" MESH_RX_NOHANDLER_SYS_NET="$tmp/sys" \
  MESH_RX_NOHANDLER_STATE="$tmp/home/.mesh/state" "$tool" --json)
grep -q '"rx_nohandler":23' <<<"$out"
grep -q 'iface=physical|rx_nohandler=23' "$tmp/home/.mesh/state"

echo "PASS: mesh-nic-rx-nohandler --test and live fixture artifact"
