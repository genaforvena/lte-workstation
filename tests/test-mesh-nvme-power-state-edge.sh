#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

make_root() {
  local root="$1" status="$2"
  mkdir -p "$root/nvme0/device/power" "$root/nvme1/device/power"
  printf '%s\n' "$status" > "$root/nvme0/device/power/runtime_status"
  printf '%s\n' "$status" > "$root/nvme1/device/power/runtime_status"
}

make_root "$td/active" active
make_root "$td/active2" active
make_root "$td/suspended" suspended
make_root "$td/suspended2" suspended
state_dir="$td/mesh"

MESH_NVME_POWER_ROOT="$td/active" MESH_DIR="$state_dir" \
  "$repo/scripts/mesh-nvme-power-state" --json >/dev/null

hold="$(MESH_NVME_POWER_ROOT="$td/active" MESH_DIR="$state_dir" \
  "$repo/scripts/mesh-nvme-power-state" --edge)"
[ -z "$hold" ] || { echo "FAIL: unchanged ACTIVE HOLD emitted: $hold"; exit 1; }

fire="$(MESH_NVME_POWER_ROOT="$td/suspended" MESH_DIR="$state_dir" \
  "$repo/scripts/mesh-nvme-power-state" --edge)"
case "$fire" in
  *'[nvme-power-state] SUSPENDED'*) : ;;
  *) echo "FAIL: changed SUSPENDED edge did not FIRE: $fire"; exit 1 ;;
esac

repeat="$(MESH_NVME_POWER_ROOT="$td/suspended2" MESH_DIR="$state_dir" \
  "$repo/scripts/mesh-nvme-power-state" --edge)"
[ -z "$repeat" ] || { echo "FAIL: unchanged SUSPENDED FIRE repeated: $repeat"; exit 1; }

echo 'mesh-nvme-power-state edge output: PASS'
