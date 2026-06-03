#!/bin/bash
. "$HOME/.config/remote-access/env"

BORE_BIN="${HOME}/.cargo/bin/bore"

"$BORE_BIN" local 443 --to bore.pub 2>&1 | while IFS= read -r line; do
    echo "$line"
    if [[ "$line" =~ listening\ at\ bore\.pub:([0-9]+) ]]; then
        PORT="${BASH_REMATCH[1]}"
        LINK="https://t.me/proxy?server=bore.pub&port=${PORT}&secret=${MTG_SECRET}"
        curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
          -H "Content-Type: application/json" \
          -d "{\"chat_id\": \"$CHAT_ID\",\"text\": \"🔐 MTProto proxy online\nServer: bore.pub:${PORT}\",\"reply_markup\": {\"inline_keyboard\": [[{\"text\": \"Add Proxy to Telegram\", \"url\": \"$LINK\"}]]}}" \
          > /dev/null 2>&1
    fi
done
