#!/usr/bin/env bash
set -u

repo="$(cd "$(dirname "$0")/.." && pwd)"
dash="$repo/scripts/mesh-dash"

help_out="$(timeout 2 "$dash" --help 2>&1)" || {
  rc=$?
  echo "FAIL: --help did not exit successfully within 2s (rc=$rc)"
  exit 1
}
printf '%s\n' "$help_out" | grep -q '^Usage: mesh-dash' \
  || { echo "FAIL: --help omitted usage line"; exit 1; }
printf '%s\n' "$help_out" | grep -q -- '--once' \
  || { echo "FAIL: --help omitted --once"; exit 1; }

td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/.mesh"
cat > "$td/bin/mesh-room-music" <<'EOF'
#!/usr/bin/env bash
sleep 5
EOF
chmod +x "$td/bin/mesh-room-music"

slow_out="$(HOME="$td" MESH_DIR="$td/.mesh" PATH="$td/bin:$PATH" \
  MESH_DASH_SOUND_TIMEOUT=1 "$dash" --once sound 2>&1)" || {
  rc=$?
  echo "FAIL: timed-out sound render exited nonzero (rc=$rc)"
  exit 1
}
printf '%s\n' "$slow_out" | grep -q 'diversity TIMEOUT' \
  || { echo "FAIL: slow sound render omitted timeout diagnosis"; exit 1; }
printf '%s\n' "$slow_out" | grep -q 'mesh-room-music --diversity' \
  || { echo "FAIL: timeout diagnosis omitted the bounded dependency"; exit 1; }

echo 'test-mesh-dash-help-option: PASS'
