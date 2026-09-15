#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tool="$repo/scripts/mesh-body-motion"
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/.local/bin" "$td/.mesh"

cat > "$td/.local/bin/mesh-phone-ip" <<'EOF'
#!/bin/sh
printf '192.0.2.10\n'
EOF
cat > "$td/.local/bin/mesh-state-touch" <<'EOF'
#!/bin/sh
exit 0
EOF
cat > "$td/.local/bin/ssh" <<'EOF'
#!/bin/sh
case "$*" in
  *"command -v termux-sensor"*)
    [ "${SENSOR_MODE:-good}" != unreachable ] || exit 1
    printf '/data/data/com.termux/files/usr/bin/termux-sensor\n'
    ;;
  *"termux-sensor -s bma420"*)
    case "${SENSOR_MODE:-good}" in
      good) printf '%s\n%s\n' '{"bma420":{"values":[0,0,9.8]}}' '{"bma420":{"values":[0,0,9.7]}}' ;;
      hollow) printf '%s\n' '{"bma420":{"values":[]}}' ;;
      single) printf '%s\n' '{"bma420":{"values":[0,0,9.8]}}' ;;
      *) exit 1 ;;
    esac
    ;;
  *) exit 1 ;;
esac
EOF
chmod +x "$td/.local/bin/mesh-phone-ip" "$td/.local/bin/ssh"

run_test() {
  local mode="$1" outvar="$2" rcvar="$3" out rc
  set +e
  out=$(HOME="$td" SENSOR_MODE="$mode" PATH=/usr/bin:/bin "$tool" --test 2>&1)
  rc=$?
  set -e
  printf -v "$outvar" '%s' "$out"
  printf -v "$rcvar" '%s' "$rc"
}

run_test good good_out good_rc
[ "$good_rc" -eq 0 ] || { echo "FAIL: valid hardware sample should pass (rc=$good_rc): $good_out"; exit 1; }
grep -q 'real-read artifact:.*accel_mag=9.7' <<<"$good_out" \
  || { echo "FAIL: passing test must report the measured sensor artifact: $good_out"; exit 1; }
grep -q 'accel_samples=2' <<<"$good_out" \
  || { echo "FAIL: passing test must report two measured samples: $good_out"; exit 1; }

run_test hollow hollow_out hollow_rc
[ "$hollow_rc" -eq 2 ] || { echo "FAIL: reachable hollow driver must exit 2 (rc=$hollow_rc): $hollow_out"; exit 1; }
grep -qi 'hollow\|no usable accelerometer sample' <<<"$hollow_out" \
  || { echo "FAIL: hollow driver must identify the missing real sample: $hollow_out"; exit 1; }

run_test single single_out single_rc
[ "$single_rc" -eq 2 ] || { echo "FAIL: one plausible sample must not pass (rc=$single_rc): $single_out"; exit 1; }
grep -qi 'two.*sample\|frozen\|incomplete' <<<"$single_out" \
  || { echo "FAIL: single sample must identify incomplete real-read evidence: $single_out"; exit 1; }

run_test unreachable unreachable_out unreachable_rc
[ "$unreachable_rc" -eq 2 ] || { echo "FAIL: unreachable phone must exit 2 (rc=$unreachable_rc): $unreachable_out"; exit 1; }
grep -qi 'phone unreachable' <<<"$unreachable_out" \
  || { echo "FAIL: unreachable phone must remain explicitly unavailable: $unreachable_out"; exit 1; }

set +e
live_out=$(HOME="$td" SENSOR_MODE=good PATH=/usr/bin:/bin "$tool" --json 2>&1)
live_rc=$?
set -e
[ "$live_rc" -eq 0 ] || { echo "FAIL: live classifier should accept two real samples (rc=$live_rc): $live_out"; exit 1; }
grep -q '"accel_mag":9.7' <<<"$live_out" \
  || { echo "FAIL: live fused artifact must classify from the latest accelerometer sample: $live_out"; exit 1; }

set +e
single_out=$(HOME="$td" SENSOR_MODE=single PATH=/usr/bin:/bin "$tool" --json 2>&1)
single_rc=$?
set -e
[ "$single_rc" -eq 2 ] || { echo "FAIL: live classifier must reject a single sample (rc=$single_rc): $single_out"; exit 1; }
grep -qi 'two valid accelerometer samples' <<<"$single_out" \
  || { echo "FAIL: single-sample live path must explain its honest degradation: $single_out"; exit 1; }

echo 'mesh-body-motion two-sample real-read and live-classifier gates: PASS'
