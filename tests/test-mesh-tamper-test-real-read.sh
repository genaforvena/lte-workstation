#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tool="$repo/scripts/mesh-tamper"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
home="$tmp/home"
mkdir -p "$home/.local/bin" "$home/.mesh"

cat > "$home/.local/bin/mesh-phone-ip" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' 192.0.2.1
EOF
cat > "$home/.local/bin/ssh" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$MESH_TEST_SSH_ARGS"
printf '%s' "${MESH_TEST_SSH_OUTPUT:-TAMPER_EOF=124}"
exit "${MESH_TEST_SSH_RC:-0}"
EOF
chmod +x "$home/.local/bin/mesh-phone-ip" "$home/.local/bin/ssh"

args_file="$tmp/ssh-args"
set +e
out=$(HOME="$home" PATH="$home/.local/bin:/usr/bin:/bin" \
  MESH_TEST_SSH_ARGS="$args_file" MESH_TAMPER_TEST_WINDOW=3 \
  "$tool" --test 2>&1)
rc=$?
set -e
[ "$rc" -eq 0 ] || { echo "FAIL: valid no-motion watch should pass --test (rc=$rc): $out"; exit 1; }
grep -q 'real-read artifact: body-quiet' <<<"$out" \
  || { echo "FAIL: --test did not report a real no-motion artifact: $out"; exit 1; }
grep -q 'termux-sensor -s SIGNIFICANT_MOTION' "$args_file" \
  || { echo "FAIL: --test did not invoke the bounded SIGNIFICANT_MOTION watch: $(cat "$args_file")"; exit 1; }
[ ! -e "$home/.mesh/.tamper-state" ] && [ ! -e "$home/.mesh/.tamper-events" ] \
  || { echo "FAIL: --test wrote a liveness artifact under its isolated HOME"; exit 1; }

set +e
out=$(HOME="$home" PATH="$home/.local/bin:/usr/bin:/bin" \
  MESH_TEST_SSH_ARGS="$args_file" MESH_TEST_SSH_OUTPUT='termux-sensor: not foundTAMPER_EOF=127' \
  "$tool" --test 2>&1)
rc=$?
set -e
[ "$rc" -eq 2 ] || { echo "FAIL: sensor command failure must degrade --test (rc=$rc): $out"; exit 1; }
grep -q 'real sensor read hollow' <<<"$out" \
  || { echo "FAIL: failed sensor read must be named hollow: $out"; exit 1; }

echo "PASS: --test runs a bounded real sensor command, reports its artifact, degrades errors, and leaves liveness files untouched"
