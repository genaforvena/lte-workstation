#!/usr/bin/env bash
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
cat > "$tmp/tmux" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$TMUX_CALLS"
case "$1" in
  has-session) exit 0 ;;
  list-clients) printf '%s\n' "${TMUX_CLIENTS:-274 69 private}" ;;
  list-windows) printf 'minds 2 80 24\nwitness 1 80 24\npub 2 80 24\ncodex 1 274 68\nforeign 2 80 24\n' ;;
  display-message) if [[ "$*" == *pane_start_command* ]]; then target="${*: -2:1}"; role="${target#*.}"; role="${target#*:}"; role="${role%%.*}"; echo "exec mesh-dash $role"; elif [[ "$*" == *pane_height* ]]; then echo 11; else echo '274 68'; fi ;;
esac
EOF
chmod +x "$tmp/tmux"
TMUX_CALLS="$tmp/calls" PATH="$tmp:$PATH" "$repo/scripts/mesh-pane-geometry" --ensure private > "$tmp/out"
grep -q 'resize-window -t private:minds -x 274 -y 68' "$tmp/calls"
grep -q 'resize-pane -t private:minds.0 -y 51' "$tmp/calls"
grep -q 'resize-window -t private:witness -x 274 -y 68' "$tmp/calls"
! grep -q 'private:codex' "$tmp/calls"
! grep -q 'private:foreign' "$tmp/calls"
[ "$(grep -c '^resize-window' "$tmp/calls")" = 3 ]
: > "$tmp/calls"
if TMUX_CLIENTS='80 24 private' TMUX_CALLS="$tmp/calls" PATH="$tmp:$PATH" "$repo/scripts/mesh-pane-geometry" --ensure private > "$tmp/out" 2>&1; then
  echo 'small client unexpectedly accepted' >&2; exit 1
fi
! grep -q '^resize-' "$tmp/calls"
: > "$tmp/calls"
if TMUX_CLIENTS=$'274 69 private\n180 66 private' TMUX_CALLS="$tmp/calls" PATH="$tmp:$PATH" "$repo/scripts/mesh-pane-geometry" --ensure private > "$tmp/out" 2>&1; then
  echo 'ambiguous clients unexpectedly accepted' >&2; exit 1
fi
! grep -q '^resize-' "$tmp/calls"
echo 'mesh-pane-geometry test: PASS'
