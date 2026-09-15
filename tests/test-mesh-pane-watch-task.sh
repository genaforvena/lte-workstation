#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT
mkdir -p "$td/bin" "$td/.mesh/pane-watch"

cat >"$td/bin/tmux" <<'EOF'
#!/usr/bin/env bash
case "$*" in
  *list-windows*) printf 'witness\n' ;;
  *list-panes*) printf '0\n1\n' ;;
  *capture-pane*) printf 'STATIC-FRAME\n' ;;
  *) exit 0 ;;
esac
EOF
cat >"$td/bin/mesh-task" <<'EOF'
#!/usr/bin/env bash
if [ "${1:-}" = create ]; then
  printf '%s\n' "$2" >>"$MESH_TASK_CREATED"
  cp "$3" "$MESH_TASK_PLAN"
  exit 0
fi
exit 0
EOF
cat >"$td/bin/mesh-chat" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >>"$MESH_CHAT_POSTS"
EOF
chmod +x "$td/bin"/*

for _ in 1 2 3; do
  PATH="$td/bin:$PATH" HOME="$td" MESH_PANEWATCH_NOHEAL=1 MESH_PANEWATCH_CYCLES=2 \
    MESH_TASK_CREATED="$td/created" MESH_TASK_PLAN="$td/plan" MESH_CHAT_POSTS="$td/posts" \
    "$repo/scripts/mesh-pane-watch" >/dev/null
done

[ "$(wc -l <"$td/created")" = 1 ] || {
  echo 'FAIL: freeze edge did not create exactly one canonical task' >&2
  exit 1
}
grep -Eq '^pane-liveness/[^/]+/witness/[0-9]+$' "$td/created"
grep -q $'^health\tinvestigate\t100\t' "$td/plan"
[ ! -s "$td/posts" ] || {
  echo 'FAIL: successful canonical task creation emitted only a prose fallback' >&2
  exit 1
}
echo 'PASS: frozen pane edge creates one exact-owner health task'
