#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

proc="$td/net-dev"
state="$td/state"
prev="$td/prev"

write_proc() {
  printf 'Inter-|   Receive                                                |  Transmit\n'
  printf ' face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed\n'
  printf '  lo: %s 0 0 0 0 0 0 0 0 %s 0 0 0 0 0 0 0\n' "$1" "$1"
}

now_ns="$(date +%s%N)"
printf '%s\nrx_lo=0\ntx_lo=0\n' "$((now_ns - 1000000000))" >"$prev"
printf 'lo rx=0 tx=0\nspike=0\n' >"$state"
write_proc 0 >"$proc"

hold="$(MESH_NET_IO_PROC="$proc" MESH_NET_IO_STATE="$state" MESH_NET_IO_PREV="$prev" \
  MESH_NET_IFACES=lo MESH_NET_SPIKE=50 "$repo/scripts/mesh-net-io" --edge)"
[ -z "$hold" ] || { echo "FAIL: unchanged HOLD emitted: $hold"; exit 1; }

write_proc 100000000 >"$proc"
fire="$(MESH_NET_IO_PROC="$proc" MESH_NET_IO_STATE="$state" MESH_NET_IO_PREV="$prev" \
  MESH_NET_IFACES=lo MESH_NET_SPIKE=50 "$repo/scripts/mesh-net-io" --edge)"
[ -n "$fire" ] || { echo 'FAIL: spike transition did not FIRE'; exit 1; }

write_proc 200000000 >"$proc"
repeat="$(MESH_NET_IO_PROC="$proc" MESH_NET_IO_STATE="$state" MESH_NET_IO_PREV="$prev" \
  MESH_NET_IFACES=lo MESH_NET_SPIKE=50 "$repo/scripts/mesh-net-io" --edge)"
[ -z "$repeat" ] || { echo "FAIL: unchanged FIRE repeated: $repeat"; exit 1; }

echo 'mesh-net-io edge output: PASS'
