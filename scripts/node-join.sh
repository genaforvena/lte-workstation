#!/usr/bin/env bash
# node-join.sh - Register this machine as an LTE Workstation node
# Run on any Linux machine with Tailscale to make it discoverable and connectable.
# Usage: ./node-join.sh [--accept-risk=lose-ssh]
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${GREEN}→${NC} $*"; }
warn()    { echo -e "${YELLOW}!${NC} $*"; }
error()   { echo -e "${RED}✗${NC} $*" >&2; }
section() { echo -e "\n${BLUE}── $* ──${NC}"; }

NODE_TAG="tag:lte-node"
RISK_FLAG="${1:-}"

# ── Prerequisites ─────────────────────────────────────────────────────────────
section "Checking prerequisites"

if ! command -v tailscale &>/dev/null; then
    error "Tailscale not found. Install: https://tailscale.com/download"
    exit 1
fi
info "Tailscale: OK"

if ! command -v mosh-server &>/dev/null && ! command -v mosh &>/dev/null; then
    warn "Mosh not found. Install: sudo apt install mosh"
else
    info "Mosh: OK"
fi

if ! tailscale status &>/dev/null; then
    error "Tailscale is not running. Run: sudo tailscale up"
    exit 1
fi
info "Tailscale: connected"

# ── Enable Tailscale SSH ─────────────────────────────────────────────────────
section "Enabling Tailscale SSH"

if tailscale debug prefs 2>&1 | grep -q '"RunSSH": true'; then
    info "Tailscale SSH already enabled"
else
    info "Enabling Tailscale SSH..."
    if [ "$RISK_FLAG" = "--accept-risk=lose-ssh" ]; then
        sudo tailscale set --ssh --accept-risk=lose-ssh
    else
        sudo tailscale set --ssh
    fi
    info "Tailscale SSH enabled"
fi

# ── Tag this node ─────────────────────────────────────────────────────────────
section "Tagging node"

CURRENT_TAGS=$(tailscale status --json | python3 -c "import json,sys; print(' '.join(json.load(sys.stdin).get('Self',{}).get('Tags',[])))" 2>/dev/null || echo "")

if echo "$CURRENT_TAGS" | grep -q "tag:lte-node"; then
    info "Node already tagged with $NODE_TAG"
else
    info "Tagging this machine with $NODE_TAG..."
    warn "Make sure your Tailscale ACL has this tag defined:"
    echo ""
    echo '  "tagOwners": { "tag:lte-node": ["autogroup:member"] }'
    echo '  "ssh": [{ "action": "accept", "src": ["tag:lte-node"], "dst": ["tag:lte-node"], "users": ["autogroup:nonroot", "root"] }]'
    echo ""

    TAILSCALE_UP_FLAGS="--ssh --advertise-tags=$NODE_TAG"
    if [ "$RISK_FLAG" = "--accept-risk=lose-ssh" ]; then
        TAILSCALE_UP_FLAGS="$TAILSCALE_UP_FLAGS --accept-risk=lose-ssh"
    fi

    info "Running: sudo tailscale up $TAILSCALE_UP_FLAGS"
    echo "Note: this may disconnect your current session as Tailscale SSH takes over."
    echo ""

    if [ -t 0 ]; then
        read -rp "Press Enter to continue (or Ctrl+C to cancel)..."
    fi

    sudo tailscale up $TAILSCALE_UP_FLAGS
    info "Tag advertised. Approve in Tailscale admin console if prompted."
fi

# ── Tailscale-only (no central VPN hub — vpn-hub retired 2026-06-07) ────────
TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "unknown")
HOSTNAME=$(hostname)

# ── Summary ───────────────────────────────────────────────────────────────────
section "Node registered"

USER=$(whoami)

echo ""
echo "This machine is now an LTE Workstation node"
echo ""
echo "Node info:"
echo "  Hostname:     $HOSTNAME"
echo "  Tailscale IP: $TAILSCALE_IP"
echo "  User:         $USER"
echo "  Tag:          $NODE_TAG"
echo ""
echo "Other nodes can connect via:"
echo "  mosh $USER@$TAILSCALE_IP"
echo "  ssh $USER@$TAILSCALE_IP"
echo ""
echo "Discover other nodes:"
echo "  tailscale status --json | jq -r '\''.Peer[] | select(.Tags // [] | index(\"tag:lte-node\")) | \"\(.HostName) - \(.TailscaleIPs[0]) (online: \(.Online))\"'\''"
echo ""
