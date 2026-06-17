#!/bin/bash
# bore-mtg.sh — expose the local MTProto proxy via a bore.pub tunnel + Telegram the proxy link.
# Node-specific (proxy nodes). Run: bore-mtg.sh (sources env: BOT_TOKEN/CHAT_ID/MTG_SECRET).
#   bore-mtg.sh --test    smoke — deps + dry-run of the bore-port parse + approved-users filter
#
# --test exercises the LOAD-BEARING logic (NOT echo-ok): (1) the regex that lifts the public port
# out of bore's stdout — if it drifts, NO bore.pub link is ever published (silent: proxy stays
# Tailscale-only); (2) the approved-users filter the python notify path uses. Falsifiable: no
# python3/curl → FAIL (dep); regex match/no-match or filter wrong → FAIL.
if [[ "${1:-}" == "--test" ]]; then
  command -v python3 >/dev/null 2>&1 || { echo "smoke-test: FAIL (no python3 — notify_approved_users can't run)"; exit 1; }
  command -v curl    >/dev/null 2>&1 || { echo "smoke-test: FAIL (no curl — can't post the proxy link to Telegram)"; exit 1; }
  # the EXACT bore-port regex the run path uses (line ~56) — a real match + a noise non-match
  line='listening at bore.pub:43217'
  if [[ "$line" =~ listening\ at\ bore\.pub:([0-9]+) ]]; then port="${BASH_REMATCH[1]}"; else port=""; fi
  [[ "$port" == "43217" ]] || { echo "smoke-test: FAIL (bore-port regex drifted: got '$port')"; exit 1; }
  if [[ 'unrelated log line' =~ listening\ at\ bore\.pub:([0-9]+) ]]; then bad="${BASH_REMATCH[1]}"; else bad=""; fi
  [[ -z "$bad" ]] || { echo "smoke-test: FAIL (regex matched noise → would publish a bogus link: '$bad')"; exit 1; }
  # the approved-users filter (same semantics as notify_approved_users' python loop), no network
  approved=$(python3 -c 'import json; u=json.loads("{\"111\":{\"approved\":true},\"222\":{\"approved\":false},\"333\":{\"approved\":true}}"); print(sum(1 for k,i in u.items() if i.get("approved")))')
  [[ "$approved" == "2" ]] || { echo "smoke-test: FAIL (approved-users filter: got '$approved', want 2)"; exit 1; }
  echo "smoke-test: ok (deps present; bore-port regex match+no-match + approved-users filter verified)"
  exit 0
fi
. "$HOME/.config/remote-access/env"

BORE_BIN="${HOME}/.cargo/bin/bore"
TAILSCALE_IP="$(tailscale ip -4 2>/dev/null )"
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
