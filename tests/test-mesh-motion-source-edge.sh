#!/usr/bin/env bash
set -u
set -o pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/.mesh" "$TMP/.local/bin"

cat >"$TMP/.local/bin/mesh-wifi-motion" <<'EOF'
#!/usr/bin/env bash
printf '[wifi-motion] MOTION signature=scatter\n'
EOF
cat >"$TMP/.local/bin/mesh-presence" <<'EOF'
#!/usr/bin/env bash
printf 'presence reachable\n'
EOF
chmod +x "$TMP/.local/bin/mesh-wifi-motion" "$TMP/.local/bin/mesh-presence"

# The audit seeds the discovered state predecessor (`STATE.prev`). Keep the
# legacy hard-coded predecessor equal to the current verdict so only the
# discovered predecessor can force FIRE.
printf 'UNATTRIBUTED\n' >"$TMP/.mesh/.motion-source.prev"
printf 'ZZ_EDGE_AUDIT_SEED\n' >"$TMP/.mesh/.motion-source.state.prev"

out="$(HOME="$TMP" PATH="$TMP/.local/bin:$PATH" "$ROOT/scripts/mesh-motion-source" --edge)"
[ -n "$out" ] || { echo "FAIL: audit-seeded STATE.prev did not force an edge"; exit 1; }
printf '%s\n' "$out" | grep -q '\[motion-source-unattributed\]' \
  || { echo "FAIL: edge output did not report UNATTRIBUTED: $out"; exit 1; }
echo "ok: audit-seeded STATE.prev forces FIRE"
