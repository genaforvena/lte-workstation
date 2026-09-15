#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fixture="$(mktemp -d)"
trap 'rm -rf "$fixture"' EXIT
mkdir -p "$fixture/.local/bin" "$fixture/.mesh"
cat >"$fixture/.local/bin/mesh-land" <<'EOF_LAND'
#!/usr/bin/env bash
sleep 10
EOF_LAND
cat >"$fixture/.local/bin/mesh-sync-tools" <<'EOF_SYNC'
#!/usr/bin/env bash
sleep 10
EOF_SYNC
chmod +x "$fixture/.local/bin/mesh-land" "$fixture/.local/bin/mesh-sync-tools"

out="$(
  timeout 5s env HOME="$fixture" MESH_DIR="$fixture/.mesh" MESH_REPO="$ROOT" \
    "$ROOT/scripts/mesh-dash" --once genome 2>&1
)"

grep -Fq 'mesh-land probe timed out after' <<<"$out"
grep -Fq 'mesh-sync-tools probe timed out after' <<<"$out"
echo 'test-mesh-dash-genome-once-bounds-land-probe: PASS'
