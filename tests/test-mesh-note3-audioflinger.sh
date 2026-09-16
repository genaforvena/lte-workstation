#!/usr/bin/env bash
set -u
set -o pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-note3-audioflinger"
TD="$(mktemp -d -t mesh-note3-audioflinger-test.XXXXXX)"
trap 'rm -rf "$TD"' EXIT

cat >"$TD/full.txt" <<'EOF'
Hardware status: 0
Output thread 0x1:
  Sample rate: 48000
  Channel Count: 2
  Format: 0x1 (pcm16)
  4 Tracks of which 0 are active
EOF

out="$("$TOOL" --parse "$TD/full.txt")"
printf '%s\n' "$out" | grep -q '"hardware_status":"0"' || { echo "FAIL hardware status: $out"; exit 1; }
printf '%s\n' "$out" | grep -q '"sample_rate":"48000"' || { echo "FAIL sample rate: $out"; exit 1; }
printf '%s\n' "$out" | grep -q '"channel_count":"2"' || { echo "FAIL channels: $out"; exit 1; }
printf '%s\n' "$out" | grep -q '"format":"pcm16"' || { echo "FAIL format: $out"; exit 1; }
printf '%s\n' "$out" | grep -q '"track_count":"4"' || { echo "FAIL tracks: $out"; exit 1; }
printf '%s\n' "$out" | grep -q '"timestamp":"' || { echo "FAIL timestamp: $out"; exit 1; }

cat >"$TD/partial.txt" <<'EOF'
Hardware status: 0
Output thread 0x1:
  Format: 0x1 (pcm16)
EOF
out="$("$TOOL" --parse "$TD/partial.txt")"
printf '%s\n' "$out" | grep -q '"hardware_status":"0"' || { echo "FAIL partial hardware: $out"; exit 1; }
printf '%s\n' "$out" | grep -q '"sample_rate":"UNKNOWN"' || { echo "FAIL missing rate not UNKNOWN: $out"; exit 1; }
printf '%s\n' "$out" | grep -q '"track_count":"UNKNOWN"' || { echo "FAIL missing tracks not UNKNOWN: $out"; exit 1; }

set +e
out="$("$TOOL" --parse "$TD/missing.txt" 2>/dev/null)"
rc=$?
set -e
[ "$rc" -eq 2 ] || { echo "FAIL missing dump rc=$rc output=$out"; exit 1; }
printf '%s\n' "$out" | grep -q '"hardware_status":"UNKNOWN"' || { echo "FAIL missing dump not UNKNOWN: $out"; exit 1; }

echo "PASS mesh-note3-audioflinger parser and UNKNOWN handling"
