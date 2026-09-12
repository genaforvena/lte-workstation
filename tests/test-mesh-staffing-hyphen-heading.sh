#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf -- "$td"' EXIT
mkdir -p "$td/charter" "$td/bin"
cat >"$td/charter/foo-bar.md" <<'EOF'
# foo-bar — private channel
EOF
cat >"$td/bin/mesh-task" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
chmod +x "$td/bin/mesh-task"

out=$(MESH_STAFFING_LIVE_WINDOWS='foo-bar' MESH_STAFFING_CHARTER_DIR="$td/charter" \
  MESH_STAFFING_TASK_BIN="$td/bin/mesh-task" "$root/scripts/mesh-staffing" --json)
OUT="$out" python3 - <<'PY'
import json, os
row = json.loads(os.environ["OUT"])["windows"][0]
assert row["window"] == "foo-bar"
assert row["role"] == "private channel"
assert row["eligible"] is True
PY
echo 'test-mesh-staffing-hyphen-heading: PASS'
