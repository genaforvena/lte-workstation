#!/bin/bash
. "$HOME/.config/remote-access/env"

BORE_BIN="${HOME}/.cargo/bin/bore"
TAILSCALE_IP="$(tailscale ip -4 2>/dev/null || echo '100.125.157.75')"
STATE_FILE="$HOME/.config/proxy-bot/state.json"
USERS_FILE="$HOME/.config/proxy-bot/users.json"

write_state() {
    local tailscale_link="$1" bore_link="$2" bore_port="$3"
    mkdir -p "$(dirname "$STATE_FILE")"
    printf '{"tailscale_link":"%s","bore_link":"%s","bore_port":%s,"updated_at":"%s"}\n' \
        "$tailscale_link" "$bore_link" "$bore_port" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        > "$STATE_FILE"
}

notify_approved_users() {
    local link="$1"
    [[ -f "$USERS_FILE" ]] || return
    # Read approved user IDs and notify each
    python3 - "$USERS_FILE" "$link" "$BOT_TOKEN" <<'EOF'
import json, sys, urllib.request, urllib.parse

users_file, link, token = sys.argv[1], sys.argv[2], sys.argv[3]
users = json.loads(open(users_file).read())
payload_tpl = {
    "text": "Proxy link updated. Tap to re-add:",
    "reply_markup": {"inline_keyboard": [[{"text": "Add Proxy", "url": link}]]}
}
for uid, info in users.items():
    if info.get("approved"):
        payload = {**payload_tpl, "chat_id": int(uid)}
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        try:
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            print(f"warn: could not notify {uid}: {e}", file=sys.stderr)
EOF
}

# Tailscale link (permanent — owner's LTE link)
TAILSCALE_LINK="https://t.me/proxy?server=${TAILSCALE_IP}&port=443&secret=${MTG_SECRET}"
write_state "$TAILSCALE_LINK" "" "null"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"$CHAT_ID\",\"text\": \"MTProto proxy online (Tailscale)\nServer: ${TAILSCALE_IP}:443\",\"reply_markup\": {\"inline_keyboard\": [[{\"text\": \"Add Proxy (Tailscale, use on LTE)\", \"url\": \"$TAILSCALE_LINK\"}]]}}" \
  > /dev/null 2>&1

"$BORE_BIN" local 443 --to bore.pub 2>&1 | while IFS= read -r line; do
    echo "$line"
    if [[ "$line" =~ listening\ at\ bore\.pub:([0-9]+) ]]; then
        PORT="${BASH_REMATCH[1]}"
        BORE_LINK="https://t.me/proxy?server=bore.pub&port=${PORT}&secret=${MTG_SECRET}"

        write_state "$TAILSCALE_LINK" "$BORE_LINK" "$PORT"
        notify_approved_users "$BORE_LINK"

        curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
          -H "Content-Type: application/json" \
          -d "{\"chat_id\": \"$CHAT_ID\",\"text\": \"MTProto proxy online (bore fallback)\nServer: bore.pub:${PORT}\",\"reply_markup\": {\"inline_keyboard\": [[{\"text\": \"Add Proxy (bore)\", \"url\": \"$BORE_LINK\"}]]}}" \
          > /dev/null 2>&1
    fi
done
