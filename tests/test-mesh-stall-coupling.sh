#!/usr/bin/env bash
set -u

root="$(cd "$(dirname "$0")/.." && pwd)"
tool="$root/scripts/mesh-stall-coupling"

[ -x "$tool" ] || { echo "FAIL: missing executable $tool"; exit 1; }

td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/cpu" <<'EOF'
some avg10=12.50 avg60=8.00 avg300=4.00 total=100
full avg10=0.00 avg60=0.00 avg300=0.00 total=0
EOF
cat >"$td/memory" <<'EOF'
some avg10=3.00 avg60=2.00 avg300=1.00 total=200
full avg10=0.00 avg60=0.00 avg300=0.00 total=0
EOF

out="$(MESH_STALL_CPU_FILE="$td/cpu" MESH_STALL_MEMORY_FILE="$td/memory" "$tool" --json 2>&1)"
rc=$?
[ "$rc" -eq 0 ] || { echo "FAIL: joint pressure fixture rc=$rc: $out"; exit 1; }
printf '%s' "$out" | grep -q '"relation":"COUPLED"' || {
  echo "FAIL: simultaneous pressure did not produce COUPLED: $out"; exit 1;
}

cat >"$td/memory" <<'EOF'
some avg10=0.00 avg60=0.00 avg300=0.00 total=200
full avg10=0.00 avg60=0.00 avg300=0.00 total=0
EOF
out="$(MESH_STALL_CPU_FILE="$td/cpu" MESH_STALL_MEMORY_FILE="$td/memory" "$tool" --json 2>&1)"
[ "$?" -eq 0 ] || { echo "FAIL: one-sided pressure fixture failed: $out"; exit 1; }
printf '%s' "$out" | grep -q '"relation":"CPU_ONLY"' || {
  echo "FAIL: one-sided pressure was treated as coupled: $out"; exit 1;
}

set +e
MESH_STALL_CPU_FILE="$td/missing" MESH_STALL_MEMORY_FILE="$td/memory" "$tool" --json >/dev/null 2>&1
rc=$?
set -e
[ "$rc" -eq 2 ] || { echo "FAIL: unreachable CPU PSI returned rc=$rc, want 2"; exit 1; }

printf 'garbage\n' >"$td/cpu"
set +e
MESH_STALL_CPU_FILE="$td/cpu" MESH_STALL_MEMORY_FILE="$td/memory" "$tool" --json >/dev/null 2>&1
rc=$?
set -e
[ "$rc" -eq 2 ] || { echo "FAIL: malformed CPU PSI returned rc=$rc, want 2"; exit 1; }

echo 'test-mesh-stall-coupling: PASS (joint relation + one-sided distinction + honest rc=2 paths)'
