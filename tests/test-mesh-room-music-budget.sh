#!/usr/bin/env bash
set -euo pipefail

script="$(cd "$(dirname "$0")/.." && pwd)/scripts/mesh-room-music"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/grainneukeln/.venv/bin" "$td/grainneukeln/output" "$td/.mesh"

cat >"$td/bin/ffprobe" <<'EOF'
#!/usr/bin/env bash
printf '10.0\n'
EOF
chmod +x "$td/bin/ffprobe"

cat >"$td/bin/mesh-heavy-run" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$1" >"$TEST_BUDGET"
printf 'render\n' >"$TEST_OUTPUT/render.mp3"
exit 0
EOF
chmod +x "$td/bin/mesh-heavy-run"

cat >"$td/grainneukeln/.venv/bin/python" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
chmod +x "$td/grainneukeln/.venv/bin/python"
: >"$td/grainneukeln/main.py"
: >"$td/source.wav"

budget_file="$td/budget"
PATH="$td/bin:$PATH" \
  HOME="$td" \
  MESH_DIR="$td/.mesh" \
  MESH_GRAIN_DIR="$td/grainneukeln" \
  MESH_RMC_AUTOMIX='amc l 120 w 4 ss 1.0 s 1.0' \
  MESH_RMC_PARAMS_LOG="$td/params.log" \
  MESH_RMC_ATTEMPTS_LOG="$td/attempts.log" \
  TEST_BUDGET="$budget_file" \
  TEST_OUTPUT="$td/grainneukeln/output" \
  "$script" --remix "$td/source.wav" >/dev/null

budget="$(<"$budget_file")"
[ "$budget" -gt 2500 ] || {
  echo "FAIL: default grainneukeln budget must exceed 2500MB, got ${budget}MB"
  exit 1
}

echo "test-mesh-room-music-budget: PASS (${budget}MB)"
