#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/chat.log" <<'EOF'
2026-09-07T00:00:01Z  chat@test  ::  [task] old-slug: original wording {#deadbeef}
2026-09-07T00:00:02Z  chat@test  ::  [task] new-slug: refactored wording {#deadbeef}
2026-09-07T00:00:03Z  docs@test  ::  [fyi] [old task wording](#deadbeef)
2026-09-07T00:00:04Z  chat@test  ::  [task] uuid-old: original UUID wording {#123e4567-e89b-42d3-a456-426614174000}
2026-09-07T00:00:05Z  chat@test  ::  [task] uuid-new: refactored UUID wording {#123e4567-e89b-42d3-a456-426614174000}
2026-09-07T00:00:06Z  docs@test  ::  [fyi] [UUID task wording](#123e4567-e89b-42d3-a456-426614174000)
EOF

out="$(MESH_DIR="$td" "$root/scripts/mesh-board-id" check)"
grep -q 'MARKDOWN {#deadbeef} resolves current: new-slug' <<<"$out"
grep -q 'MARKDOWN {#123e4567-e89b-42d3-a456-426614174000} resolves current: uuid-new' <<<"$out"
grep -q 'check: 4 \[task\].*markdown 2' <<<"$out"

link="$(MESH_DIR="$td" "$root/scripts/mesh-board-id" markdown deadbeef)"
[ "$link" = '[new-slug: refactored wording](#deadbeef)' ]
link="$(MESH_DIR="$td" "$root/scripts/mesh-board-id" markdown 123e4567-e89b-42d3-a456-426614174000)"
[ "$link" = '[uuid-new: refactored UUID wording](#123e4567-e89b-42d3-a456-426614174000)' ]

printf '%s\n' '2026-09-07T00:00:07Z  docs@test  ::  [fyi] [missing task](#cafebabe)' >>"$td/chat.log"
printf '%s\n' '2026-09-07T00:00:08Z  docs@test  ::  [fyi] [missing UUID task](#123e4567-e89b-42d3-a456-426614174001)' >>"$td/chat.log"
if MESH_DIR="$td" "$root/scripts/mesh-board-id" check >/dev/null 2>&1; then
  echo 'Markdown dangling anchor unexpectedly passed' >&2
  exit 1
fi

out="$(MESH_DIR="$td" "$root/scripts/mesh-board-id" check 2>&1 || true)"
grep -q 'MARKDOWN-DANGLING {#cafebabe}' <<<"$out"
grep -q 'MARKDOWN-DANGLING {#123e4567-e89b-42d3-a456-426614174001}' <<<"$out"

printf '%s\n' 'test-mesh-board-id-markdown: PASS (Markdown anchor follows UUID refiling)' 
