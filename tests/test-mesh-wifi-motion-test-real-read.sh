#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tool="$repo/scripts/mesh-wifi-motion"
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT
home="$td/home"
mkdir -p "$home/.mesh"

run_test() {
  local outvar="$1" rcvar="$2" out rc
  set +e
  out=$(HOME="$home" PATH="$PATH" "$tool" --test 2>&1)
  rc=$?
  set -e
  printf -v "$outvar" '%s' "$out"
  printf -v "$rcvar" '%s' "$rc"
}

# Classifier fixtures alone must not certify the sense when its real scan tape is absent.
run_test absent_out absent_rc
[ "$absent_rc" -eq 2 ] || { echo "FAIL: missing real Wi-Fi tape must exit 2, got rc=$absent_rc: $absent_out"; exit 1; }
grep -qi 'real.*artifact.*unavailable\|real.*scan.*unavailable' <<<"$absent_out" \
  || { echo "FAIL: missing tape must explain the honest degraded path: $absent_out"; exit 1; }

# A fresh six-scan tape exercises the same JSON/classifier path as the live sense and must expose
# the measured verdict and scan age as the test artifact.
log="$home/.mesh/wifi.log"
for i in 5 4 3 2 1 0; do
  ts=$(date -u -d "-$((i * 10)) min" +%FT%TZ)
  printf '%s host n=4 aps=[60|AA:AA:AA:AA:AA:01|A|5240 55|BB:BB:BB:BB:BB:02|B|5240 50|CC:CC:CC:CC:CC:03|C|5240 45|DD:DD:DD:DD:DD:04|D|5240]\n' "$ts" >> "$log"
done
run_test fresh_out fresh_rc
[ "$fresh_rc" -eq 0 ] || { echo "FAIL: fresh real-read artifact should pass (rc=$fresh_rc): $fresh_out"; exit 1; }
grep -q 'real-read artifact:.*verdict=STILL.*age_s=' <<<"$fresh_out" \
  || { echo "FAIL: passing test must report its fresh classified scan artifact: $fresh_out"; exit 1; }

# A producer clock slightly ahead is within the sense's configured skew tolerance. Keep the runtime
# classification valid while surfacing freshness as UNKNOWN; --test must not misreport this as a
# broken real-read path.
: > "$log"
for i in 5 4 3 2 1 0; do
  ts=$(date -u -d "$((60 - i * 600)) seconds" +%FT%TZ)
  printf '%s host n=4 aps=[60|AA:AA:AA:AA:AA:01|A|5240 55|BB:BB:BB:BB:BB:02|B|5240 50|CC:CC:CC:CC:CC:03|C|5240 45|DD:DD:DD:DD:DD:04|D|5240]\n' "$ts" >> "$log"
done
run_test skew_out skew_rc
[ "$skew_rc" -eq 0 ] || { echo "FAIL: tolerated clock skew should remain a classifiable real-read artifact (rc=$skew_rc): $skew_out"; exit 1; }
grep -Eq 'real-read artifact:.*verdict=STILL.*age_s=-[0-9]+ freshness=UNKNOWN' <<<"$skew_out" \
  || { echo "FAIL: tolerated future timestamp must publish its negative age as UNKNOWN freshness: $skew_out"; exit 1; }

# Stale and malformed tapes are blindness, not calm rooms.
old="$td/stale.log"
stale_ts=$(date -u -d '-3 hours' +%FT%TZ)
for i in 1 2 3 4 5 6; do
  printf '%s host n=4 aps=[60|AA:AA:AA:AA:AA:01|A|5240 55|BB:BB:BB:BB:BB:02|B|5240 50|CC:CC:CC:CC:CC:03|C|5240 45|DD:DD:DD:DD:DD:04|D|5240]\n' "$stale_ts" >> "$old"
done
cp "$old" "$log"
run_test stale_out stale_rc
[ "$stale_rc" -eq 2 ] || { echo "FAIL: stale real tape must exit 2, got rc=$stale_rc: $stale_out"; exit 1; }

printf 'not-a-scan\n' > "$log"
run_test malformed_out malformed_rc
[ "$malformed_rc" -eq 2 ] || { echo "FAIL: malformed real tape must exit 2, got rc=$malformed_rc: $malformed_out"; exit 1; }

# The runtime path must honor the same timestamp requirement as --test. A syntactically scan-like
# line without producer time is not evidence of a current room state and must not become STILL.
printf 'host n=4 aps=[60|AA:AA:AA:AA:AA:01|A|5240 55|BB:BB:BB:BB:BB:02|B|5240 50|CC:CC:CC:CC:CC:03|C|5240 45|DD:DD:DD:DD:DD:04|D|5240]\n' > "$log"
set +e
untime_out=$(HOME="$home" MESH_WIFI_MOTION_LOG="$log" MESH_WIFI_MOTION_REFRESH=0 "$tool" --json 2>&1)
untime_rc=$?
set -e
[ "$untime_rc" -eq 2 ] || { echo "FAIL: runtime must reject an untimeable tape (rc=$untime_rc): $untime_out"; exit 1; }
grep -q 'timestamp_unparseable' <<<"$untime_out" \
  || { echo "FAIL: runtime degraded path must name the missing timestamp: $untime_out"; exit 1; }

echo 'mesh-wifi-motion --test live-artifact gate: PASS'
