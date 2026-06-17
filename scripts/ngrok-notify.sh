#!/bin/bash
# ngrok-notify.sh — on ngrok start, read the live tunnel URL and Telegram the operator the
# fresh SSH (+ mosh-over-Tailscale) connect lines. Node-specific (ngrok-ingress nodes).
#   ngrok-notify.sh           run (sourced env: BOT_TOKEN/CHAT_ID); sends the notification
#   ngrok-notify.sh --test    smoke — deps + dry-run of the tunnel-URL parse / host:port split
#
# --test dry-runs the LOAD-BEARING logic (NOT echo-ok): the exact `python3` expression that lifts
# public_url out of ngrok's /api/tunnels JSON (lines below) + the cut host/port split that builds
# the ssh line. A drift here would silently send "Machine online" with a BROKEN ssh command and no
# error — the one failure mode a smoke test must catch. Falsifiable: no curl/python3 → FAIL (dep);
# parse or split regresses → FAIL; empty-tunnels guard breaks → FAIL.
if [ "${1:-}" = "--test" ]; then
  command -v curl    >/dev/null 2>&1 || { echo "smoke-test: FAIL (no curl — can't query ngrok API or send Telegram)"; exit 1; }
  command -v python3 >/dev/null 2>&1 || { echo "smoke-test: FAIL (no python3 — can't parse /api/tunnels JSON)"; exit 1; }
  parse='import sys,json; t=json.load(sys.stdin)["tunnels"]; print(t[0]["public_url"] if t else "")'
  addr=$(printf '%s' '{"tunnels":[{"public_url":"tcp://0.tcp.ngrok.io:18922"}]}' | python3 -c "$parse" 2>/dev/null)
  [ "$addr" = "tcp://0.tcp.ngrok.io:18922" ] || { echo "smoke-test: FAIL (tunnel-URL parse drifted: got '$addr')"; exit 1; }
  host=$(echo "$addr" | cut -d'/' -f3 | cut -d':' -f1)
  port=$(echo "$addr" | cut -d':' -f3)
  [ "$host" = "0.tcp.ngrok.io" ] && [ "$port" = "18922" ] \
    || { echo "smoke-test: FAIL (host/port split wrong: host='$host' port='$port')"; exit 1; }
  empty=$(printf '%s' '{"tunnels":[]}' | python3 -c "$parse" 2>/dev/null)
  [ -z "$empty" ] || { echo "smoke-test: FAIL (empty-tunnels guard broken: got '$empty' — would notify with no addr)"; exit 1; }
  echo "smoke-test: ok (deps present; tunnel-URL parse + host:port split + empty-tunnels guard verified)"
  exit 0
fi
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
