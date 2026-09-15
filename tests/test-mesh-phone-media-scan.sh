#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-phone-media-scan"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/mesh-phone-ip" <<'EOF'
#!/usr/bin/env bash
printf '192.0.2.10\n'
EOF
cat >"$td/ssh" <<'EOF'
#!/usr/bin/env bash
if [ "${MESH_TEST_SSH_MODE:-success}" = fail ]; then
  exit 255
fi
if [ "${MESH_TEST_SSH_MODE:-success}" = empty ]; then
  exit 0
fi
printf 'Finished scanning 1 file(s)\n'
printf '%s\n' '-rw-rw----. 1 root everybody 95046 Jun 4 17:32 /sdcard/fixture.m4a'
EOF
chmod +x "$td/mesh-phone-ip" "$td/ssh"

path=/sdcard/fixture.m4a
out="$(PATH="$td:$PATH" MESH_TEST_SSH_MODE=success "$TOOL" "$path")" || {
  echo "FAIL: successful media scan returned non-zero: $out" >&2
  exit 1
}
printf '%s\n' "$out" | grep -q 'Finished scanning 1 file(s)' || {
  echo "FAIL: successful scan omitted non-empty scan result: $out" >&2
  exit 1
}

if PATH="$td:$PATH" MESH_TEST_SSH_MODE=empty "$TOOL" "$path" >/tmp/mesh-phone-media-scan-empty.out 2>&1; then
  echo 'FAIL: empty scan result must not be success' >&2
  exit 1
fi
grep -q 'UNKNOWN' /tmp/mesh-phone-media-scan-empty.out || {
  echo 'FAIL: empty scan result must render UNKNOWN' >&2
  exit 1
}

if PATH="$td:$PATH" MESH_TEST_SSH_MODE=fail "$TOOL" "$path" >/tmp/mesh-phone-media-scan-fail.out 2>&1; then
  echo 'FAIL: transport failure must not be success' >&2
  exit 1
fi
grep -q 'UNKNOWN' /tmp/mesh-phone-media-scan-fail.out || {
  echo 'FAIL: transport failure must render UNKNOWN' >&2
  exit 1
}

echo 'test-mesh-phone-media-scan: ok'
