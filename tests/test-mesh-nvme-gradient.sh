#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-nvme-gradient"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

mkdir -p "$td/nvme0/hwmon0" "$td/nvme1/hwmon1"
printf '40000\n' >"$td/nvme0/hwmon0/temp1_input"
printf '55000\n' >"$td/nvme1/hwmon1/temp1_input"

out="$(MESH_NVME_GRADIENT_ROOT="$td" MESH_NVME_GRADIENT_STATE="$td/state" "$TOOL" --json 2>&1)"
rc=$?
[ "$rc" -eq 0 ] || { echo "FAIL: fixture read rc=$rc: $out"; exit 1; }
printf '%s\n' "$out" | grep -q '"relation":"THERMAL-GRADIENT"' || {
  echo "FAIL: expected thermal-gradient relation: $out"; exit 1;
}
printf '%s\n' "$out" | grep -q '"delta_mc":15000' || {
  echo "FAIL: expected 15000 mC delta: $out"; exit 1;
}

MESH_NVME_GRADIENT_ROOT="$td/missing" MESH_NVME_GRADIENT_STATE="$td/state2" "$TOOL" >/dev/null 2>&1
rc=$?
if [ "$rc" -eq 0 ]; then
  echo 'FAIL: missing controllers were reported as reachable'; exit 1
fi
[ "$rc" -eq 2 ] || { echo "FAIL: missing controllers rc=$rc, want 2"; exit 1; }

echo 'ok: nvme gradient relation and unreachable path'
