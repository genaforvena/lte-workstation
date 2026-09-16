#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-phone-saf-ls"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/mesh-phone-ip" <<'EOF'
#!/usr/bin/env bash
printf '192.0.2.10\n'
EOF
cat >"$td/ssh" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" > "${MESH_TEST_SSH_ARGS_FILE:?}"
case "${MESH_TEST_SSH_MODE:-success}" in
  success) printf '[{"name":"fixture","uri":"content://fixture"}]\n' ;;
  empty) printf '[]\n' ;;
  malformed) printf '{not-json}\n' ;;
  fail) exit 255 ;;
esac
EOF
chmod +x "$td/mesh-phone-ip" "$td/ssh"

uri='content://com.android.externalstorage.documents/tree/primary%3ADownload'
args_file="$td/args"
out="$(PATH="$td:$PATH" MESH_TEST_SSH_MODE=success MESH_TEST_SSH_ARGS_FILE="$args_file" \
  "$TOOL" "$uri")" || { echo "FAIL: successful SAF list returned non-zero: $out" >&2; exit 1; }
printf '%s\n' "$out" | grep -q '"name":"fixture"' || {
  echo "FAIL: successful SAF list omitted JSON array: $out" >&2
  exit 1
}
grep -q 'termux-saf-ls' "$args_file" || { echo 'FAIL: consumer did not invoke termux-saf-ls' >&2; exit 1; }
grep -q "$uri" "$args_file" || { echo 'FAIL: folder URI was not passed to the remote command' >&2; exit 1; }

out="$(PATH="$td:$PATH" MESH_TEST_SSH_MODE=empty MESH_TEST_SSH_ARGS_FILE="$args_file" \
  "$TOOL" "$uri")" || { echo "FAIL: [] must be valid empty data: $out" >&2; exit 1; }
printf '%s\n' "$out" | grep -q '^\[\]$' || { echo "FAIL: [] was not preserved: $out" >&2; exit 1; }

if PATH="$td:$PATH" MESH_TEST_SSH_MODE=malformed MESH_TEST_SSH_ARGS_FILE="$args_file" \
  "$TOOL" "$uri" >/tmp/mesh-phone-saf-ls-malformed.out 2>&1; then
  echo 'FAIL: malformed JSON must be UNKNOWN' >&2
  exit 1
fi
grep -q 'UNKNOWN' /tmp/mesh-phone-saf-ls-malformed.out || { echo 'FAIL: malformed JSON lacked UNKNOWN' >&2; exit 1; }

if PATH="$td:$PATH" MESH_TEST_SSH_MODE=fail MESH_TEST_SSH_ARGS_FILE="$args_file" \
  "$TOOL" "$uri" >/tmp/mesh-phone-saf-ls-fail.out 2>&1; then
  echo 'FAIL: transport failure must be UNKNOWN' >&2
  exit 1
fi
grep -q 'UNKNOWN' /tmp/mesh-phone-saf-ls-fail.out || { echo 'FAIL: transport failure lacked UNKNOWN' >&2; exit 1; }

echo 'test-mesh-phone-saf-ls: ok'
