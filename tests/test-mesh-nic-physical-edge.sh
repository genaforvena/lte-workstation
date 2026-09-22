#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

root="$td/sys"
state="$td/state"
mkdir -p "$root/enp-test/device" "$root/enp-test/statistics"
printf '1\n' > "$root/enp-test/carrier"
printf '0\n' > "$root/enp-test/statistics/tx_carrier_errors"
printf '4\n' > "$root/enp-test/carrier_changes"

MESH_NIC_PHYSICAL_ROOT="$root" MESH_NIC_PHYSICAL_STATE="$state" \
  "$repo/scripts/mesh-nic-physical" --json >/dev/null

hold="$(MESH_NIC_PHYSICAL_ROOT="$root" MESH_NIC_PHYSICAL_STATE="$state" \
  "$repo/scripts/mesh-nic-physical" --edge)"
[ -z "$hold" ] || { echo "FAIL: unchanged HOLD emitted: $hold"; exit 1; }

printf '7\n' > "$root/enp-test/statistics/tx_carrier_errors"
fire="$(MESH_NIC_PHYSICAL_ROOT="$root" MESH_NIC_PHYSICAL_STATE="$state" \
  "$repo/scripts/mesh-nic-physical" --edge)"
case "$fire" in
  *'[nic-physical] UP-CARRIER-FAULT'*) : ;;
  *) echo "FAIL: changed edge did not FIRE: $fire"; exit 1 ;;
esac

repeat="$(MESH_NIC_PHYSICAL_ROOT="$root" MESH_NIC_PHYSICAL_STATE="$state" \
  "$repo/scripts/mesh-nic-physical" --edge)"
[ -z "$repeat" ] || { echo "FAIL: unchanged FIRE repeated: $repeat"; exit 1; }

echo 'mesh-nic-physical edge output: PASS'
