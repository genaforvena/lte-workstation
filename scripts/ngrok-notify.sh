#!/bin/bash
. "$HOME/.config/remote-access/env"

sleep 5

ADDR=$(curl -s http://localhost:4040/api/tunnels | python3 -c \
  "import sys,json; t=json.load(sys.stdin)['tunnels']; print(t[0]['public_url'] if t else '')" \
  2>/dev/null)

if [ -n "$ADDR" ]; then
  HOST=$(echo "$ADDR" | cut -d'/' -f3 | cut -d':' -f1)
  PORT=$(echo "$ADDR" | cut -d':' -f3)
  TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "")

  if [ -n "$TAILSCALE_IP" ]; then
    MOSH_BLOCK="\n\n⚡ Mosh via Tailscale (permanent):\nmosh $USER@$TAILSCALE_IP\n\nMosh = SSH but survives network switches. Preferred on mobile."
  else
    MOSH_BLOCK=""
  fi

  curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{
      \"chat_id\": \"$CHAT_ID\",
      \"text\": \"🏠 Machine online\n\n📡 SSH (changes on reboot):\nssh -p $PORT $USER@$HOST${MOSH_BLOCK}\"
    }" > /dev/null
fi
