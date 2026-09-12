#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
tool="$root/scripts/mesh-uvc-metadata"
tmp=$(mktemp -d -t mesh-uvc-metadata-test.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

[ -x "$tool" ]
grep -q '^# reflex-cadence: ' "$tool"
grep -q '^# reflex-artifact: ' "$tool"
# The wrapper is not wired until the node card can advertise the physical metadata organ.
grep -q 'mesh-uvc-metadata' "$root/scripts/mesh-card" \
  || { echo 'uvc metadata wiring: mesh-card does not declare the wrapper' >&2; exit 1; }
grep -q '^    uvc-metadata)' "$root/scripts/mesh-organ-keepalive" \
  || { echo 'uvc metadata wiring: keepalive has no real probe arm' >&2; exit 1; }

# Parse the kernel's packed uvc_meta_buf stream into timestamped JSONL records.
python3 - "$tmp/sample.bin" <<'PY'
import struct, sys
with open(sys.argv[1], 'wb') as stream:
    stream.write(struct.pack('<QHBB', 123456789, 0x481, 12, 0x8d))
    stream.write(bytes.fromhex('01 02 03 04 05 06 07 08 09 0a'))
PY
"$tool" --parse "$tmp/sample.bin" >"$tmp/parsed.jsonl"
python3 - "$tmp/parsed.jsonl" <<'PY'
import json, sys
row = json.loads(open(sys.argv[1]).read())
assert row == {
    'timestamp_ns': 123456789,
    'sof': 0x481,
    'header_length': 12,
    'flags': 0x8d,
    'payload_header_hex': '0c8d0102030405060708090a',
}
PY
printf '\001' >>"$tmp/sample.bin"
if "$tool" --parse "$tmp/sample.bin" >"$tmp/malformed.jsonl" 2>"$tmp/malformed.err"; then
  echo 'uvc metadata parser accepted a truncated record' >&2
  exit 1
fi
grep -q 'truncated' "$tmp/malformed.err"

# Runtime acquisition retries transient failures without promoting failed partial data.
fakebin="$tmp/retry-bin"
fakehome="$tmp/retry-home"
fake_dev="$tmp/retry-device"
fake_out="$tmp/retry-output.bin"
fake_count="$tmp/retry-count"
mkdir -p "$fakebin" "$fakehome"
: >"$fake_dev"
cat >"$fakebin/v4l2-ctl" <<'EOF'
#!/bin/sh
count=0
[ ! -f "$FAKE_UVC_COUNT_FILE" ] || count=$(cat "$FAKE_UVC_COUNT_FILE")
count=$((count + 1))
printf '%s\n' "$count" >"$FAKE_UVC_COUNT_FILE"
for arg in "$@"; do
  case "$arg" in --stream-to=*) dest=${arg#--stream-to=} ;; esac
done
[ -n "${dest:-}" ] || exit 90
if [ "$count" -lt 3 ]; then
  printf 'partial-failure' >"$dest"
  exit 1
fi
python3 - "$dest" <<'PY'
import struct, sys
with open(sys.argv[1], 'wb') as stream:
    stream.write(struct.pack('<QHBB', 987654321, 0x482, 12, 0x8d))
    stream.write(bytes(range(10)))
PY
EOF
chmod +x "$fakebin/v4l2-ctl"
if ! HOME="$fakehome" PATH="$fakebin:/usr/bin:/bin" FAKE_UVC_COUNT_FILE="$fake_count" \
  MESH_UVC_METADATA_DEV="$fake_dev" MESH_UVC_METADATA_OUT="$fake_out" \
  "$tool" >"$tmp/retry.out" 2>&1; then
  cat "$tmp/retry.out" >&2
  echo 'uvc metadata runtime did not recover after transient read failures' >&2
  exit 1
fi
[ "$(cat "$fake_count")" = 3 ] || { echo 'uvc metadata runtime did not use three bounded attempts' >&2; exit 1; }
"$tool" --parse "$fake_out" >"$tmp/runtime-parsed.jsonl"
python3 - "$tmp/runtime-parsed.jsonl" "$fake_out" <<'PY'
import json, sys
rows = [json.loads(line) for line in open(sys.argv[1])]
assert len(rows) == 1 and rows[0]['timestamp_ns'] == 987654321
assert len(open(sys.argv[2], 'rb').read()) == 22
PY
[ -s "${fake_out%.bin}.jsonl" ] || { echo 'uvc metadata runtime did not publish parsed JSONL' >&2; exit 1; }
cp "$fake_out" "$tmp/retained.bin"

# A zero-exit read containing malformed bytes must not replace the last valid raw or parsed artifact.
cat >"$fakebin/v4l2-ctl" <<'EOF'
#!/bin/sh
for arg in "$@"; do
  case "$arg" in --stream-to=*) dest=${arg#--stream-to=} ;; esac
done
printf 'malformed' >"$dest"
EOF
chmod +x "$fakebin/v4l2-ctl"
if HOME="$fakehome" PATH="$fakebin:/usr/bin:/bin" MESH_UVC_METADATA_ATTEMPTS=1 \
  MESH_UVC_METADATA_DEV="$fake_dev" MESH_UVC_METADATA_OUT="$fake_out" \
  "$tool" >"$tmp/malformed-runtime.out" 2>&1; then
  echo 'uvc metadata runtime accepted a malformed non-empty stream' >&2
  exit 1
fi
"$tool" --parse "$fake_out" >"$tmp/retained-parsed.jsonl"
cmp -s "$tmp/retained.bin" "$fake_out" || {
  echo 'uvc metadata runtime replaced the last raw artifact after malformed input' >&2; exit 1;
}
cmp -s "$tmp/runtime-parsed.jsonl" "${fake_out%.bin}.jsonl" || {
  echo 'uvc metadata runtime replaced the last parsed artifact after malformed input' >&2; exit 1;
}

if [ -e /dev/video1 ]; then
  MESH_UVC_METADATA_TIMEOUT=2 MESH_UVC_METADATA_DEV=/dev/video1 "$tool" --test
else
  echo 'uvc metadata live test: SKIP (/dev/video1 absent)'
fi

# A wedged V4L2 endpoint must not hold the reflex forever.
fakebin="$tmp/fake-bin"
mkdir -p "$fakebin"
cat >"$fakebin/v4l2-ctl" <<'EOF'
#!/bin/sh
sleep 5
EOF
chmod +x "$fakebin/v4l2-ctl"
start=$(date +%s)
if timeout 3 env PATH="$fakebin:/usr/bin:/bin" MESH_UVC_METADATA_TIMEOUT=1 MESH_UVC_METADATA_TEST_ATTEMPTS=1 MESH_UVC_METADATA_DEV=/dev/null "$tool" --test >"$tmp/hung.out" 2>&1; then
  echo 'uvc metadata test accepted a wedged endpoint' >&2
  exit 1
fi
elapsed=$(( $(date +%s) - start ))
[ "$elapsed" -lt 3 ] || { echo "uvc metadata probe exceeded outer bound (${elapsed}s)" >&2; exit 1; }
grep -q 'metadata read' "$tmp/hung.out"

if MESH_UVC_METADATA_DEV=/dev/does-not-exist "$tool" --test >"$tmp/negative.out" 2>&1; then
  echo 'uvc metadata test accepted a missing device' >&2
  exit 1
fi
grep -q 'no metadata device' "$tmp/negative.out"

echo 'uvc metadata contract: negative gate and live probe pass'
