#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/mesh"
printf '2026-09-11T22:00:00Z sender@host :: [handoff] health: completed; next is health\n' >"$td/chat.log"
printf 'IDLE\n' >"$td/state"

cat >"$td/bin/mesh-mind-state" <<'EOF'
#!/bin/sh
cat "$MESH_STATE"
EOF
cat >"$td/bin/mesh-clear" <<'EOF'
#!/bin/sh
printf '%s\n' "$1" >>"$MESH_CLEARS"
EOF
cat >"$td/bin/mesh-fsnotify" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >>"$MESH_FSN_CALLS"
exit 0
EOF
chmod +x "$td/bin/mesh-mind-state" "$td/bin/mesh-clear" "$td/bin/mesh-fsnotify"

base=(MESH_DIR="$td/mesh" MESH_CHAT_LOG="$td/chat.log" MESH_STATE="$td/state"
  MESH_CLEARS="$td/clears" MESH_MIND_STATE_CMD="$td/bin/mesh-mind-state"
  MESH_CLEAR_CMD="$td/bin/mesh-clear" MESH_FSN_CMD="$td/bin/mesh-fsnotify"
  MESH_FSN_CALLS="$td/fsn-calls" PATH="$td/bin:$PATH")
env "${base[@]}" python3 "$repo/scripts/mesh-handoff-reactor" --once
grep -Fxq health "$td/clears"

# A handoff for a working pane must stay queued rather than being discarded at the first scan.
: >"$td/clears"
printf 'WORKING\n' >"$td/state"
printf '2026-09-11T22:00:01Z sender@host :: [handoff] witness: still working\n' >>"$td/chat.log"
env "${base[@]}" python3 "$repo/scripts/mesh-handoff-reactor" --once
test ! -s "$td/clears"
printf 'IDLE\n' >"$td/state"
env "${base[@]}" python3 "$repo/scripts/mesh-handoff-reactor" --once
grep -Fxq witness "$td/clears"
env "${base[@]}" python3 "$repo/scripts/mesh-handoff-reactor" --listen
grep -Fq -- '--window 290 --debounce 4' "$td/fsn-calls"

echo 'test-mesh-handoff-reactor: PASS (new handoffs clear idle panes and retain working panes for retry)'
