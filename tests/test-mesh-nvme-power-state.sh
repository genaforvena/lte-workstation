#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
tool="$root/scripts/mesh-nvme-power-state"

test -x "$tool"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/nvme0/device/power" "$tmp/nvme1/device/power"
printf 'active\n' > "$tmp/nvme0/device/power/runtime_status"
printf 'suspended\n' > "$tmp/nvme1/device/power/runtime_status"

out="$(MESH_NVME_POWER_ROOT="$tmp" MESH_DIR="$tmp/mesh" "$tool" --json)"
printf '%s\n' "$out" | grep -q '"verdict":"MIXED"'
printf '%s\n' "$out" | grep -q '"controllers":2'
test -s "$tmp/mesh/.nvme-power-state"

mkdir -p "$tmp/empty"
if MESH_NVME_POWER_ROOT="$tmp/empty" MESH_DIR="$tmp/mesh2" "$tool" --json >/dev/null 2>&1; then
  echo "expected unreachable NVMe power source to exit 2" >&2
  exit 1
else
  test "$?" -eq 2
fi

echo "test-mesh-nvme-power-state: PASS"
