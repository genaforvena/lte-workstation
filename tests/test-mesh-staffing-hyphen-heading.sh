#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf -- "$td"' EXIT
mkdir -p "$td/charter" "$td/bin"
cat >"$td/charter/foo-bar.md" <<'EOF'
# foo-bar — private channel
EOF
cat >"$td/bin/mesh-promises" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' '{"open": [], "holds": []}'
EOF
chmod +x "$td/bin/mesh-promises"

out=$(MESH_STAFFING_LIVE_WINDOWS='foo-bar' MESH_STAFFING_CHARTER_DIR="$td/charter" \
  MESH_STAFFING_PROMISES_BIN="$td/bin/mesh-promises" "$root/scripts/mesh-staffing" --json)
OUT="$out" python3 - <<'PY'
import json, os
row = json.loads(os.environ["OUT"])["windows"][0]
assert row["window"] == "foo-bar"
assert row["role"] == "private channel"
assert row["eligible"] is True
PY
echo 'test-mesh-staffing-hyphen-heading: PASS'
