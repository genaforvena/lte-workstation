#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
tool="$root/scripts/mesh-nic-rx-loss"

[ -x "$tool" ] || { echo "FAIL: mesh-nic-rx-loss is not executable" >&2; exit 1; }

MESH_NIC_STATS_ROOT="$root/tests/does-not-exist" "$tool" --test >/dev/null 2>&1 && {
  echo "FAIL: missing sysfs source must make --test exit 2" >&2; exit 1;
} || { rc=$?; [ "$rc" = 2 ] || { echo "FAIL: missing sysfs source rc=$rc, want 2" >&2; exit 1; }; }

echo "ok: nic-tx-rate contract"
