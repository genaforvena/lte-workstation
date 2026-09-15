#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/.mesh"
cat >"$td/bin/mesh-promises" <<'EOF'
#!/bin/sh
echo 'synthetic promise feed failure' >&2
exit 9
EOF
chmod +x "$td/bin/mesh-promises"
printf 'host: test\nminds: codex\n' >"$td/.mesh-card"
printf '%s  tester@test  ::  [task] stale-ledger-canary: route only with a valid promise feed\n' \
  "$(date -u +%FT%TZ)" >"$td/.mesh/chat.log"

if PATH="$td/bin:$PATH" HOME="$td" MESH_DIR="$td/.mesh" \
    MESH_MIND_WORKERS=no-such-window "$repo/scripts/mesh-dispatch" >"$td/stdout" 2>"$td/stderr"; then
  cat "$td/stdout" "$td/stderr" "$td/.mesh/dispatch.log" 2>/dev/null >&2 || true
  echo 'FAIL: dispatch continued after a failed promise feed' >&2
  exit 1
fi
grep -q 'REFUSED ledger-feed failed' "$td/.mesh/dispatch.log"
echo 'test-mesh-dispatch-hledger-gate: PASS (failed feed blocks routing)'
