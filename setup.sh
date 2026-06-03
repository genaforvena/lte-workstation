#!/usr/bin/env bash
# One-time setup for lte-workstation.
# Run from the repo root: ./setup.sh
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${GREEN}→${NC} $*"; }
warn()    { echo -e "${YELLOW}!${NC} $*"; }
error()   { echo -e "${RED}✗${NC} $*" >&2; }
section() { echo -e "\n${BLUE}── $* ──${NC}"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config/remote-access"
CONFIG_FILE="$CONFIG_DIR/env"

# ── Prerequisites ─────────────────────────────────────────────────────────────
section "Checking prerequisites"

MISSING=()

check_cmd() {
    local name="$1" cmd="$2" hint="$3"
    if command -v "$cmd" &>/dev/null || [[ -x "$cmd" ]]; then
        info "$name: OK"
    else
        warn "$name not found.  Install: $hint"
        MISSING+=("$name")
    fi
}

check_cmd "Docker"    "docker"                 "https://docs.docker.com/engine/install/"
check_cmd "ngrok"     "$HOME/.local/bin/ngrok" "Download at https://ngrok.com/download → put in ~/.local/bin/"
check_cmd "bore"      "$HOME/.cargo/bin/bore"  "cargo install bore-cli  (needs Rust: https://rustup.rs)"
check_cmd "mosh"      "mosh"                   "sudo apt install mosh"
check_cmd "tailscale" "tailscale"              "https://tailscale.com/download"

if [[ ${#MISSING[@]} -gt 0 ]]; then
    echo ""
    error "Missing: ${MISSING[*]}"
    error "Install missing tools and re-run."
    exit 1
fi

# ── Telegram ──────────────────────────────────────────────────────────────────
section "Telegram bot setup"
cat <<'HINT'
1. Open Telegram → message @BotFather → /newbot → follow prompts → copy the token
2. Message @userinfobot to get your numeric chat ID
HINT
echo ""
read -rp "Bot token:  " BOT_TOKEN
read -rp "Chat ID:    " CHAT_ID

# ── ngrok ─────────────────────────────────────────────────────────────────────
section "ngrok auth token"
echo "Get yours at: https://dashboard.ngrok.com/get-started/your-authtoken"
echo ""
read -rp "ngrok auth token: " NGROK_TOKEN

# ── MTProto proxy (optional) ──────────────────────────────────────────────────
section "MTProto Telegram proxy (optional)"
cat <<'HINT'
Skip this if Telegram works fine on your network.
If you're in a region where Telegram is blocked (Russia, Iran, etc.), set up a
fake-TLS proxy. Enter a domain name that looks like normal HTTPS traffic — it
should be a real domain reachable from your network (e.g. yandex.ru for Russia).
HINT
echo ""
read -rp "SNI domain for fake-TLS [press Enter to skip]: " SNI_DOMAIN
SNI_DOMAIN="${SNI_DOMAIN:-none}"

MTG_SECRET=""
if [[ "$SNI_DOMAIN" != "none" && -n "$SNI_DOMAIN" ]]; then
    info "Generating MTG secret for domain: $SNI_DOMAIN"
    MTG_SECRET=$(docker run --rm ghcr.io/9seconds/mtg:2 generate-secret --hex "$SNI_DOMAIN" 2>/dev/null)
    if [[ -z "$MTG_SECRET" ]]; then
        error "Failed to generate MTG secret. Is Docker running?"
        exit 1
    fi
    info "Secret: $MTG_SECRET"
fi

# ── Write config ──────────────────────────────────────────────────────────────
section "Writing config"
mkdir -p "$CONFIG_DIR"
chmod 700 "$CONFIG_DIR"
cat > "$CONFIG_FILE" <<EOF
BOT_TOKEN=$BOT_TOKEN
CHAT_ID=$CHAT_ID
MTG_SECRET=$MTG_SECRET
EOF
chmod 600 "$CONFIG_FILE"
info "Config written to $CONFIG_FILE (not tracked by git)"

# ── ngrok auth ────────────────────────────────────────────────────────────────
section "Authorizing ngrok"
"$HOME/.local/bin/ngrok" config add-authtoken "$NGROK_TOKEN"
info "ngrok authorized"

# ── Install scripts ───────────────────────────────────────────────────────────
section "Installing scripts"
mkdir -p "$HOME/.local/bin"
for script in ngrok-notify.sh bore-mtg.sh; do
    cp "$SCRIPT_DIR/scripts/$script" "$HOME/.local/bin/$script"
    chmod +x "$HOME/.local/bin/$script"
    info "Installed ~/.local/bin/$script"
done

# ── Systemd services ──────────────────────────────────────────────────────────
section "Installing systemd services"
mkdir -p "$HOME/.config/systemd/user"
cp "$SCRIPT_DIR/scripts/ngrok.service" "$HOME/.config/systemd/user/ngrok.service"
info "Installed ngrok.service"

if [[ "$SNI_DOMAIN" != "none" && -n "$SNI_DOMAIN" ]]; then
    cp "$SCRIPT_DIR/scripts/bore-mtg.service" "$HOME/.config/systemd/user/bore-mtg.service"
    info "Installed bore-mtg.service"

    mkdir -p "$HOME/.config/mtg"
    cat > "$HOME/.config/mtg/config.toml" <<EOF
secret = "$MTG_SECRET"
bind-to = "0.0.0.0:443"
EOF
    info "MTG config written to ~/.config/mtg/config.toml"

    info "Starting MTG Docker container"
    docker rm -f mtg 2>/dev/null || true
    docker run -d --name mtg --restart unless-stopped \
        -v "$HOME/.config/mtg/config.toml:/etc/mtg.toml:ro" \
        -p 443:443 \
        ghcr.io/9seconds/mtg:2 run /etc/mtg.toml
    info "MTG container started"
fi

# ── Enable services ───────────────────────────────────────────────────────────
section "Enabling services"
systemctl --user daemon-reload
systemctl --user enable --now ngrok.service
info "ngrok.service enabled and started"

if [[ "$SNI_DOMAIN" != "none" && -n "$SNI_DOMAIN" ]]; then
    systemctl --user enable --now bore-mtg.service
    info "bore-mtg.service enabled and started"
fi

loginctl enable-linger "$USER"
info "Linger enabled — services survive logout and start on boot"

# ── Summary ───────────────────────────────────────────────────────────────────
section "Done"
TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "<run: tailscale ip -4>")
echo ""
echo "Your Tailscale IP: $TAILSCALE_IP"
echo ""
echo "On your phone (Termux):"
echo "  pkg install mosh openssh"
echo "  mosh $USER@$TAILSCALE_IP"
echo ""
echo "Telegram bot will send your SSH + mosh commands on next service start."
if [[ "$SNI_DOMAIN" != "none" && -n "$SNI_DOMAIN" ]]; then
    echo "Proxy 'Add to Telegram' button will appear when bore tunnel connects."
fi
