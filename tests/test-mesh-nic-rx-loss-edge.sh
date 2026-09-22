#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

make_root() {
  local root="$1" errors="$2" tx="$3"
  mkdir -p "$root/enx-test/statistics"
  printf '0\n' > "$root/enx-test/statistics/rx_missed_errors"
  printf '%s\n' "$errors" > "$root/enx-test/statistics/rx_errors"
  printf '%s\n' "$tx" > "$root/enx-test/statistics/tx_bytes"
}

make_root "$td/clean" 0 100
make_root "$td/clean2" 0 200
make_root "$td/fault1" 5 1100
make_root "$td/fault2" 10 1200
state="$td/state"

MESH_NIC_STATS_ROOT="$td/clean" MESH_NIC_STATS_ROOT2="$td/clean2" \
  MESH_NIC_STATE="$state" MESH_NIC_INTERVAL=1 "$repo/scripts/mesh-nic-rx-loss" --json >/dev/null

hold="$(MESH_NIC_STATS_ROOT="$td/clean" MESH_NIC_STATS_ROOT2="$td/clean2" \
  MESH_NIC_STATE="$state" MESH_NIC_INTERVAL=1 "$repo/scripts/mesh-nic-rx-loss" --edge)"
[ -z "$hold" ] || { echo "FAIL: unchanged CLEAN HOLD emitted: $hold"; exit 1; }

fire="$(MESH_NIC_STATS_ROOT="$td/clean" MESH_NIC_STATS_ROOT2="$td/fault1" \
  MESH_NIC_STATE="$state" MESH_NIC_INTERVAL=1 "$repo/scripts/mesh-nic-rx-loss" --edge)"
case "$fire" in
  *'[nic-rx-loss] DRIVER_ERRORS'*) : ;;
  *) echo "FAIL: changed DRIVER_ERRORS edge did not FIRE: $fire"; exit 1 ;;
esac

repeat="$(MESH_NIC_STATS_ROOT="$td/fault1" MESH_NIC_STATS_ROOT2="$td/fault2" \
  MESH_NIC_STATE="$state" MESH_NIC_INTERVAL=1 "$repo/scripts/mesh-nic-rx-loss" --edge)"
[ -z "$repeat" ] || { echo "FAIL: unchanged DRIVER_ERRORS FIRE repeated: $repeat"; exit 1; }

echo 'mesh-nic-rx-loss edge output: PASS'
