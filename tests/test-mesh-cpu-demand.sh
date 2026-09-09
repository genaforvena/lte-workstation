#!/usr/bin/env bash
set -u
set -o pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-cpu-demand"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

fail=0
mkdir -p "$td/cpufreq/policy0" "$td/cpufreq/policy1" "$td/cpufreq/policy2"
printf '2200000\n' > "$td/cpufreq/policy0/scaling_cur_freq"
printf '4500000\n' > "$td/cpufreq/policy1/scaling_cur_freq"
# policy2 intentionally has no readable file: it must remain visible as na.

out="$(MESH_CPU_DEMAND_ROOT="$td/cpufreq" MESH_CPU_DEMAND_STATE="$td/state" \
  "$TOOL" --json)" || { echo "fixture invocation failed: $out"; exit 1; }
printf '%s\n' "$out" | grep -q '"policies":3' || { echo "missing policy count: $out"; fail=1; }
printf '%s\n' "$out" | grep -q '"readable":2' || { echo "missing readable count: $out"; fail=1; }
printf '%s\n' "$out" | grep -q 'policy2.*na' || { echo "unreadable policy was not na: $out"; fail=1; }
printf '%s\n' "$out" | grep -q '"average_khz":3350000' || { echo "wrong average: $out"; fail=1; }
printf '%s\n' "$out" | grep -q '"age_s":0' || { echo "missing fresh age: $out"; fail=1; }
[ -s "$td/state" ] || { echo "state artifact missing"; fail=1; }
edge="$(MESH_CPU_DEMAND_ROOT="$td/cpufreq" MESH_CPU_DEMAND_STATE="$td/state" "$TOOL" --edge)"
[ -z "$edge" ] || { echo "unchanged --edge was noisy: $edge"; fail=1; }

mkdir -p "$td/home/.mesh"
cp "$td/state" "$td/home/.mesh/.cpu-demand-state"
roll="$(HOME="$td/home" "$ROOT/scripts/mesh-sensorium" --cached 2>/dev/null)"
printf '%s\n' "$roll" | grep -q '^CPU[[:space:]]\+demand=3350000kHz readable=2/3' || {
  echo "cached sensorium wiring missing: $roll"; fail=1;
}

live_rc=0
live="$(MESH_CPU_DEMAND_ROOT=/sys/devices/system/cpu/cpufreq \
  MESH_CPU_DEMAND_STATE="$td/live-state" "$TOOL" --json 2>/dev/null)" || live_rc=$?
case "$live_rc" in
  0) printf '%s\n' "$live" | grep -q '"readable":[1-9]' || { echo "live read has no readable policy: $live"; fail=1; } ;;
  2) printf '%s\n' "$live" | grep -q 'UNKNOWN\|OFFLINE' || { echo "rc2 was not honest: $live"; fail=1; } ;;
  *) echo "unexpected live rc=$live_rc: $live"; fail=1 ;;
esac

if [ "$fail" -eq 0 ]; then
  echo "ok (fixture per-policy read + unreadable=na + live hardware gate)"
else
  echo "FAIL"
  exit 1
fi
