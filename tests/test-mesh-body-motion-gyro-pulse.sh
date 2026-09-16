#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tool="$repo/scripts/mesh-body-motion"
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/.mesh"
printf '100||0|\n' > "$td/.mesh/.body-motion-state-simulate"

# The latest gyro sample is quiet, but the paired samples contain a real rotation pulse.
# `_mesh_gyro_delta` is the measured value produced by the live stream summarizer.
json='{"bma420":{"values":[0,0,9.8]},"LINEARACCEL":{"values":[0.05,0,0]},"GYROSCOPE":{"values":[0.05,0,0]},"STEP_COUNTER":{"values":[100]},"tmd2755_l":{"values":[50]},"tmd2755_p":{"values":[5]},"_mesh_gyro_delta":0.75}'
set +e
out=$(printf '%s' "$json" | HOME="$td" "$tool" --simulate=- --json 2>&1)
rc=$?
set -e
[ "$rc" -eq 0 ] || { echo "FAIL: paired gyro pulse should classify (rc=$rc): $out"; exit 1; }
grep -q 'rotation-pulse-without-translation' <<<"$out" \
  || { echo "FAIL: gyro pulse relation missing: $out"; exit 1; }
grep -q '"gyro_delta":0.75' <<<"$out" \
  || { echo "FAIL: measured gyro delta missing from JSON: $out"; exit 1; }

echo 'mesh-body-motion paired gyro pulse: PASS'
