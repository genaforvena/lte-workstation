#!/usr/bin/env bash
set -u

root="$(cd "$(dirname "$0")/.." && pwd)"
tool="$root/scripts/mesh-io-contention"

[ -x "$tool" ] || { echo "FAIL: missing executable $tool"; exit 1; }

td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

set +e
MESH_IO_CONTENTION_PROC_STAT="$td/missing-stat" \
MESH_IO_CONTENTION_DISKSTATS="$td/missing-disk" \
MESH_IO_CONTENTION_STATE="$td/state" \
  "$tool" >/dev/null 2>&1
rc=$?
set -e
if [ "$rc" -eq 0 ]; then
  echo 'FAIL: unreachable kernel sources were accepted'
  exit 1
fi
[ "$rc" -eq 2 ] || { echo "FAIL: unreachable kernel sources returned rc=$rc, want 2"; exit 1; }

echo 'ok: unreachable sources are UNKNOWN (rc=2)'
