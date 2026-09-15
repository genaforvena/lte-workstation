#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/home/.mesh" "$tmp/home/.local/bin"

cat > "$tmp/home/.local/bin/tmux" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat > "$tmp/home/.local/bin/mesh-tell" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$HOME/tell.log"
exit 0
EOF
cat > "$tmp/home/.local/bin/mesh-chat" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$HOME/board.log"
EOF
chmod +x "$tmp/home/.local/bin/"*

printf '2026-09-13T15:00:00Z  from=140230022  "private sample"\n' > "$tmp/home/.mesh/tg-strangers.log"
printf '0\n' > "$tmp/home/.mesh/.roz-channel.offset"

HOME="$tmp/home" ROZ_CHAT_ID=140230022 "$ROOT/scripts/mesh-roz-channel"

if [[ ! -s "$tmp/home/tell.log" ]]; then
  echo "FAIL: inbound private message was not delivered to tg-roz"
  exit 1
fi
if [[ -s "$tmp/home/board.log" ]]; then
  echo "FAIL: inbound private text was copied to mesh-chat"
  exit 1
fi
echo "ok: inbound routing does not write message text to mesh-chat"
