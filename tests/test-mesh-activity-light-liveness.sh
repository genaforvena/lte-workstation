#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
tool="$repo/scripts/mesh-activity-light"
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT

mkdir -p "$td/bin" "$td/.mesh"

cat >"$td/bin/mesh-phone-ip" <<'EOF'
#!/usr/bin/env bash
echo 127.0.0.1
EOF
cat >"$td/bin/mesh-light" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' '{"change_class":"STABLE","velocity":0,"level":42}'
EOF
cat >"$td/bin/mesh-body-motion" <<'EOF'
#!/usr/bin/env bash
echo '[body-still]'
EOF
cat >"$td/bin/mesh-tamper" <<'EOF'
#!/usr/bin/env bash
echo '[body-quiet]'
EOF
cat >"$td/bin/timeout" <<'EOF'
#!/usr/bin/env bash
if [ "${2:-}" = bash ] && [ "${3:-}" = -c ]; then
  exit 0
fi
shift
"$@"
EOF
ln -s "$repo/scripts/mesh-state-touch" "$td/bin/mesh-state-touch"
chmod +x "$td/bin"/*

run_env=(HOME="$td" PATH="$td/bin:/usr/bin:/bin")
env "${run_env[@]}" "$tool" --json >"$td/first.json"
state="$td/.mesh/.activity-light.state"
[ -s "$state" ]
first_value=$(cat "$state")
touch -d '@1' "$state"

env "${run_env[@]}" "$tool" --json >"$td/second.json"
second_value=$(cat "$state")
[ "$second_value" = "$first_value" ]
[ "$(stat -c %Y "$state")" -gt 1 ]
grep -q '"verdict":"STATIC"' "$td/second.json"

echo 'mesh-activity-light liveness: PASS'
