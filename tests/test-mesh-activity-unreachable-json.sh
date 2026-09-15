#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tool="$repo/scripts/mesh-activity"
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT

mkdir -p "$td/bin" "$td/.mesh"
cat >"$td/bin/mesh-ambient-level" <<'EOF'
#!/usr/bin/env bash
echo '[ambient] MODERATE'
EOF
cat >"$td/bin/mesh-presence" <<'EOF'
#!/usr/bin/env bash
if [ "${MESH_PRESENCE_FIXTURE:-empty}" = unreachable ]; then
  exit 1
fi
printf '%s\n' '=== mesh-presence test ===' '---' 'inventory: 0 devices'
EOF
chmod +x "$td/bin"/*

printf 'PRESENT|dwell_s=10|changes_24h=1\n' >"$td/.mesh/.room-sense.state"
run_env=(HOME="$td" MESH_STATE_DIR="$td/.mesh" PATH="$td/bin:$repo/scripts:/usr/bin:/bin")

env "${run_env[@]}" MESH_PRESENCE_FIXTURE=empty "$tool" --json >"$td/empty.json"
grep -q '"devices":"0"' "$td/empty.json"
grep -q '"gaps":""' "$td/empty.json"

env "${run_env[@]}" MESH_PRESENCE_FIXTURE=unreachable "$tool" --json >"$td/unreachable.json"
grep -q '"devices":"UNKNOWN"' "$td/unreachable.json"
grep -q '"gaps":".*devices:' "$td/unreachable.json"
grep -q 'unreachable\|failed\|no output' "$td/unreachable.json"

echo 'mesh-activity unreachable JSON: PASS'
