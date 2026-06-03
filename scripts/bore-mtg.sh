#!/bin/bash
. "$HOME/.config/remote-access/env"

BORE_BIN="${HOME}/.cargo/bin/bore"
TAILSCALE_IP="$(tailscale ip -4 2>/dev/null || echo '')"

# Send Tailscale-based proxy link immediately (permanent, works on LTE where bore.pub may be blocked)
if [[ -n "$TAILSCALE_IP" ]]; then
    TAILSCALE_LINK="https://t.me/proxy?server=${TAILSCALE_IP}&port=443&secret=${MTG_SECRET}"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
      -H "Content-Type: application/json" \
      -d "{\"chat_id\": \"$CHAT_ID\",\"text\": \"MTProto proxy online (Tailscale)\nServer: ${TAILSCALE_IP}:443\",\"reply_markup\": {\"inline_keyboard\": [[{\"text\": \"Add Proxy (Tailscale, use on LTE)\", \"url\": \"$TAILSCALE_LINK\"}]]}}" \
      > /dev/null 2>&1
fi

"$BORE_BIN" local 443 --to bore.pub 2>&1 | while IFS= read -r line; do
    echo "$line"
    if [[ "$line" =~ listening\ at\ bore\.pub:([0-9]+) ]]; then
        PORT="${BASH_REMATCH[1]}"
        LINK="https://t.me/proxy?server=bore.pub&port=${PORT}&secret=${MTG_SECRET}"
        curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
          -H "Content-Type: application/json" \
          -d "{\"chat_id\": \"$CHAT_ID\",\"text\": \"MTProto proxy online (bore fallback)\nServer: bore.pub:${PORT}\",\"reply_markup\": {\"inline_keyboard\": [[{\"text\": \"Add Proxy (bore)\", \"url\": \"$LINK\"}]]}}" \
          > /dev/null 2>&1
    fi
done
