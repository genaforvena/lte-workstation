#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

mkdir -p "$td/bin" "$td/mesh"
mkdir -p "$td/home/.local/bin"
cat >"$td/bin/mesh-clear" <<'EOF'
#!/bin/sh
if [ "${1:-}" = --test ]; then
  echo clear-test-ok
  exit 0
fi
exit 2
EOF
cat >"$td/bin/crontab" <<'EOF'
#!/bin/sh
printf '%s\n' '*/5 * * * * /fake/mesh-handoff-reactor --listen'
EOF
cat >"$td/bin/pgrep" <<'EOF'
#!/bin/sh
exit 0
EOF
chmod +x "$td/bin/mesh-clear" "$td/bin/crontab" "$td/bin/pgrep"
ln -s "$td/bin/mesh-clear" "$td/home/.local/bin/mesh-clear"
printf '%s\n' '{"pending":[]}' >"$td/mesh/handoff-reactor.json"

PATH="$td/bin:/usr/bin:/bin" \
MESH_DIR="$td/mesh" MESH_CLEAR_CMD="$td/bin/mesh-clear" \
MESH_REACTOR_STATE="$td/mesh/handoff-reactor.json" MESH_CRONTAB_CMD="$td/bin/crontab" \
MESH_PGREP_CMD="$td/bin/pgrep" bash "$ROOT/scripts/mesh-clear-health" >"$td/out"
grep -Fq 'clear-health: OK' "$td/out"
grep -Fq 'verdict=OK' "$td/mesh/clear-health.state"

PATH="/usr/bin:/bin" HOME="$td/home" MESH_DIR="$td/mesh" \
  MESH_REACTOR_STATE="$td/mesh/handoff-reactor.json" MESH_CRONTAB_CMD="$td/bin/crontab" \
  MESH_PGREP_CMD="$td/bin/pgrep" bash "$ROOT/scripts/mesh-clear-health" >"$td/cron-path-out"
grep -Fq 'clear-health: OK' "$td/cron-path-out"

cat >"$td/bin/mesh-clear" <<'EOF'
#!/bin/sh
exit 9
EOF
chmod +x "$td/bin/mesh-clear"
if PATH="$td/bin:/usr/bin:/bin" MESH_DIR="$td/mesh" MESH_CLEAR_CMD="$td/bin/mesh-clear" \
  MESH_REACTOR_STATE="$td/mesh/handoff-reactor.json" MESH_CRONTAB_CMD="$td/bin/crontab" \
  MESH_PGREP_CMD="$td/bin/pgrep" bash "$ROOT/scripts/mesh-clear-health" >"$td/fail-out" 2>&1; then
  echo 'FAIL: clear-health passed a failing clear test' >&2
  exit 1
fi
grep -Fq 'clear-test rc=9' "$td/fail-out"
grep -Fq 'verdict=FAIL' "$td/mesh/clear-health.state"

touch -d '1 hour ago' "$td/mesh/handoff-reactor.json"
if PATH="$td/bin:/usr/bin:/bin" MESH_DIR="$td/mesh" MESH_CLEAR_CMD="$td/bin/mesh-clear" \
  MESH_REACTOR_STATE="$td/mesh/handoff-reactor.json" MESH_CRONTAB_CMD="$td/bin/crontab" \
  MESH_PGREP_CMD="$td/bin/pgrep" MESH_CLEAR_HEALTH_MAX_REACTOR_AGE=900 \
  bash "$ROOT/scripts/mesh-clear-health" >"$td/stale-out" 2>&1; then
  echo 'FAIL: clear-health passed stale reactor evidence' >&2
  exit 1
fi
grep -Fq 'reactor-state-stale' "$td/stale-out"

echo 'test-mesh-clear-health: PASS (reflex records fresh OK/FAIL evidence from the real clear self-test)'
