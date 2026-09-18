#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tool="$repo/scripts/mesh-nic-multicast-rx"
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT

mkdir -p "$td/net/eth0/statistics" "$td/net/lo/statistics" "$td/devices/mock-ethernet"
printf '42\n' > "$td/net/eth0/statistics/multicast"
printf '1\n' > "$td/net/lo/statistics/multicast"
ln -s "$td/devices/mock-ethernet" "$td/net/eth0/device"

set +e
fixture_out=$(MESH_NIC_MULTICAST_ROOT="$td/net" MESH_NIC_MULTICAST_STATE="$td/state" "$tool" --json 2>&1)
fixture_rc=$?
set -e
[ "$fixture_rc" -eq 0 ] || { echo "FAIL: fixture read rc=$fixture_rc: $fixture_out"; exit 1; }
grep -q '"multicast_frames":42' <<<"$fixture_out" || { echo "FAIL: fixture count: $fixture_out"; exit 1; }
[ -s "$td/state" ] || { echo 'FAIL: successful read must write state'; exit 1; }

set +e
MESH_NIC_MULTICAST_ROOT="$td/missing" MESH_NIC_MULTICAST_STATE="$td/missing-state" "$tool" >/dev/null 2>&1
missing_rc=$?
set -e
[ "$missing_rc" -eq 2 ] || { echo "FAIL: absent source must exit 2, got $missing_rc"; exit 1; }

set +e
live_out=$(MESH_NIC_MULTICAST_STATE="$td/live-state" "$tool" --test 2>&1)
live_rc=$?
set -e
[ "$live_rc" -eq 0 ] || { echo "FAIL: real multicast read gate failed rc=$live_rc: $live_out"; exit 1; }
grep -q 'REAL multicast counter read' <<<"$live_out" || { echo "FAIL: --test omitted real-read evidence: $live_out"; exit 1; }

echo 'test-mesh-nic-multicast-rx: PASS (fixture, unreachable exit-2, and real multicast counter read)'
