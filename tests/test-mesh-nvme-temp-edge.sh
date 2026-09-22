#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

make_root() {
  local root="$1" sensor="$2"
  mkdir -p "$root/nvme0/hwmon0"
  printf '40850\n' > "$root/nvme0/hwmon0/temp1_input"
  printf 'Composite\n' > "$root/nvme0/hwmon0/temp1_label"
  printf '74850\n' > "$root/nvme0/hwmon0/temp1_max"
  printf '79850\n' > "$root/nvme0/hwmon0/temp1_crit"
  printf '%s\n' "$sensor" > "$root/nvme0/hwmon0/temp2_input"
  printf 'Sensor 1\n' > "$root/nvme0/hwmon0/temp2_label"
  printf '65261850\n' > "$root/nvme0/hwmon0/temp2_max"
  printf -- '-273150\n' > "$root/nvme0/hwmon0/temp2_min"
}

make_root "$td/warm" 50000
make_root "$td/hot" 76000
make_root "$td/hot2" 76500
state_dir="$td/mesh"

MESH_NVME_ROOT="$td/warm" MESH_DIR="$state_dir" \
  "$repo/scripts/mesh-nvme-temp" --json >/dev/null

hold="$(MESH_NVME_ROOT="$td/warm" MESH_DIR="$state_dir" \
  "$repo/scripts/mesh-nvme-temp" --edge)"
[ -z "$hold" ] || { echo "FAIL: unchanged WARM HOLD emitted: $hold"; exit 1; }

fire="$(MESH_NVME_ROOT="$td/hot" MESH_DIR="$state_dir" \
  "$repo/scripts/mesh-nvme-temp" --edge)"
case "$fire" in
  *'[nvme-temp] HOT'*) : ;;
  *) echo "FAIL: changed HOT edge did not FIRE: $fire"; exit 1 ;;
esac

repeat="$(MESH_NVME_ROOT="$td/hot2" MESH_DIR="$state_dir" \
  "$repo/scripts/mesh-nvme-temp" --edge)"
[ -z "$repeat" ] || { echo "FAIL: unchanged HOT FIRE repeated: $repeat"; exit 1; }

echo 'mesh-nvme-temp edge output: PASS'
