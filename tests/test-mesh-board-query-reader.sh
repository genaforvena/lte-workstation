#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

board="$tmp/chat.log"
cat >"$board" <<'EOF'
2026-09-09T00:00:01Z  genome@alpha  ::  [task] repair ; owner:genome, status:open, task:repair
2026-09-09T00:00:02Z  tg@beta  ::  [fyi] observed ; status:done
2026-09-09T00:00:03Z  health@alpha  ::  [task] inspect ; owner:health, status:open
EOF

count="$(MESH_BOARD_LOG="$board" python3 "$root/scripts/mesh-board" query --count 'marker=task' AND 'node=alpha')"
[[ "$count" == 2 ]]

json="$(MESH_BOARD_LOG="$board" python3 "$root/scripts/mesh-board" query --json 'owner=genome')"
grep -Fq '"marker": "task"' <<<"$json"
grep -Fq '"node": "alpha"' <<<"$json"

if MESH_BOARD_LOG="$board" python3 "$root/scripts/mesh-board" query --count 'marker=missing' >/dev/null; then
  echo 'expected no-match query to return non-zero' >&2
  exit 1
fi

echo 'mesh-board query reader: PASS (tmux text board metadata query via named reader)'
