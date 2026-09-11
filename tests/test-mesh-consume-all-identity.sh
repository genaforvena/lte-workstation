#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
supervisor="$root/scripts/mesh-consume-all"
tmp="$(mktemp -d)"
cleanup(){
  local p
  for p in "${decoy:-}" "${spawned:-}" "${p1:-}" "${p2:-}"; do
    [ -n "$p" ] && kill "$p" 2>/dev/null || true
  done
  rm -rf "$tmp"
}
trap cleanup EXIT INT TERM
mkdir -p "$tmp/home/.mesh" "$tmp/bin"

cat > "$tmp/bin/tmux" <<'EOF'
#!/usr/bin/env bash
case "$*" in
  *has-session*) exit 0 ;;
  *list-windows*) printf '%s\n' probe ;;
  *list-panes*) printf '%s\n' 0 1 ;;
  *display-message*) printf '%s\n' 'mesh-dash probe' ;;
  *) exit 0 ;;
esac
EOF
cat > "$tmp/bin/mesh-pane-consume" <<'EOF'
#!/usr/bin/env bash
sleep 30
EOF
chmod +x "$tmp/bin/tmux" "$tmp/bin/mesh-pane-consume"

# Red-first decoy: its argv contains the historical text fragment but its argv structure is not a
# driver.  The supervisor must neither report nor kill it.
bash -c 'exec -a "mesh-pane-consume probe --interval decoy" sleep 30' &
decoy="$!"

# Two concurrent ensure passes must converge to one exact driver.  The lock makes the observation and
# spawn decision single-writer; without it this assertion is red.
env HOME="$tmp/home" PATH="$tmp/bin:$PATH" MESH_CONSUME_CHANNELS='probe:1' "$supervisor" & p1=$!
env HOME="$tmp/home" PATH="$tmp/bin:$PATH" MESH_CONSUME_CHANNELS='probe:1' "$supervisor" & p2=$!
wait "$p1" "$p2"

mapfile -t exact < <(env HOME="$tmp/home" PATH="$tmp/bin:$PATH" MESH_CONSUME_CHANNELS='probe:1' "$supervisor" --status | awk '/probe[[:space:]]+pid/{print $3}')
[ "${#exact[@]}" -eq 1 ] || { echo "FAIL: expected one exact driver, got ${#exact[@]}"; exit 1; }
spawned="${exact[0]}"
[ "${exact[0]}" != "$decoy" ] || { echo 'FAIL: decoy was treated as the driver'; exit 1; }
kill -0 "$decoy" 2>/dev/null || { echo 'FAIL: decoy was killed'; exit 1; }

echo 'ok: exact /proc argv identity excludes decoys and concurrent passes converge under lock'
