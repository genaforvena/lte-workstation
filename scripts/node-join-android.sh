#!/usr/bin/env bash
# node-join-android.sh - Register an Android (Termux) phone as an lte-node
# Usage: ./node-join-android.sh <tailscale-ip> [ssh-user] [ssh-port]
# Must be run from a machine that already has passwordless SSH access to the phone.

set -euo pipefail

# --- smoke test: deps + dry-run arg-guard, NO phone contact -------------------
# Real check (was: no --test at all). Two load-bearing deps the join flow needs:
#   ssh     — every step reaches the phone over it; absent => the script is inert.
#   python3 — steps 4 tags the device via the Tailscale API in inline python3.
# Plus a dry-run of the arg-guard: re-invoke self with no args, assert it exits
# nonzero AND prints Usage (catches a broken guard that would SSH to "" or "--test").
# Prove: `node-join-android.sh --test` PASSes; same on a PATH without ssh FAILs.
if [ "${1:-}" = --test ]; then
    fail=0
    for d in ssh python3; do
        command -v "$d" >/dev/null 2>&1 || { echo "smoke-test: FAIL (missing dep: $d)"; fail=1; }
    done
    # the public key step 3 installs on the phone
    [ -f "$HOME/.ssh/id_ed25519.pub" ] || echo "smoke-test: WARN (no ~/.ssh/id_ed25519.pub — key-copy step is a no-op)"
    if out="$(bash "$0" 2>&1)"; then
        echo "smoke-test: FAIL (no-args arg-guard should exit nonzero, exited 0)"; fail=1
    else
        printf '%s' "$out" | grep -q 'Usage:' || { echo "smoke-test: FAIL (no-args path did not print Usage)"; fail=1; }
    fi
    [ "$fail" = 0 ] && { echo "smoke-test: ok (ssh+python3 present, arg-guard works)"; exit 0; }
    exit 1
fi

if [ $# -lt 1 ]; then
    echo "Usage: $0 <tailscale-ip> [ssh-user] [ssh-port]"
    echo "  tailscale-ip  IP of the Android device on Tailscale"
    echo "  ssh-user      SSH username (Termux user, default: u0_a386)"
    echo "  ssh-port      SSH port (default: 8022)"
    exit 1
fi

DEVICE_IP="$1"
SSH_USER="${2:-u0_a386}"
SSH_PORT="${3:-8022}"
NODE_TAG="tag:lte-node"
SSH_HOST="$SSH_USER@$DEVICE_IP"
SSH_OPTS="-p $SSH_PORT -o StrictHostKeyChecking=no -o ConnectTimeout=10"
API_KEY="${TS_API_KEY:-}"

RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'
info()  { echo -e "${GREEN}→${NC} $*"; }
error() { echo -e "${RED}✗${NC} $*" >&2; }
warn()  { echo -e "${RED}!${NC} $*" >&2; }

# 1. Verify SSH access
info "Checking SSH access to $SSH_HOST:$SSH_PORT..."
if ! ssh $SSH_OPTS "$SSH_HOST" "echo OK" 2>/dev/null; then
    error "Cannot SSH to $SSH_HOST:$SSH_PORT — set up key auth first"
    exit 1
fi
info "SSH access OK"

# 2. Check prerequisites on device
info "Checking prerequisites..."
ssh $SSH_OPTS "$SSH_HOST" "which mosh-server && echo mosh: OK || echo mosh: not found" </dev/null
ssh $SSH_OPTS "$SSH_HOST" "echo 'Termux user: \$(whoami)'" </dev/null

# 3. Copy our public key if not already there
if ! ssh $SSH_OPTS -o BatchMode=yes "$SSH_HOST" "echo keyless" 2>/dev/null; then
    info "Copying SSH public key to device..."
    cat ~/.ssh/id_ed25519.pub | ssh $SSH_OPTS "$SSH_HOST" \
        "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && echo KEY_INSTALLED"
fi

# 4. Tag via Tailscale API (Android can't run tailscale CLI in Termux)
if [ -n "$API_KEY" ]; then
    info "Tagging device $DEVICE_IP with $NODE_TAG via API..."
    DEVICE_ID=$(python3 -c "
import urllib.request, base64, json
api_key = '$API_KEY'
url = 'https://api.tailscale.com/api/v2/tailnet/ilyailiilia@gmail.com/devices'
credentials = base64.b64encode(f'{api_key}:'.encode()).decode()
req = urllib.request.Request(url)
req.add_header('Authorization', f'Basic {credentials}')
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())
    for d in data.get('devices', []):
        if '$DEVICE_IP' in d.get('addresses', []):
            print(d['id'])
            break
")
    if [ -n "$DEVICE_ID" ]; then
        python3 -c "
import urllib.request, base64, json
api_key = '$API_KEY'
url = f'https://api.tailscale.com/api/v2/device/$DEVICE_ID/tags'
credentials = base64.b64encode(f'{api_key}:'.encode()).decode()
req = urllib.request.Request(url, method='POST')
req.add_header('Authorization', f'Basic {credentials}')
req.add_header('Content-Type', 'application/json')
req.data = json.dumps({'tags': ['$NODE_TAG']}).encode()
with urllib.request.urlopen(req) as r:
    print('Tagged:', r.status)
"
        info "Device tagged with $NODE_TAG"
    else
        error "Could not find device $DEVICE_IP in Tailscale API"
    fi
else
    warn "TS_API_KEY not set. Tag the device manually in Tailscale admin console."
    warn "Go to: https://login.tailscale.com/admin/machines/$DEVICE_IP"
fi

# 5. Summary
echo ""
echo "=== Node Registration Complete ==="
echo "Hostname:     $(ssh $SSH_OPTS "$SSH_HOST" 'hostname' </dev/null)"
echo "Tailscale IP: $DEVICE_IP"
echo "User:         $SSH_USER"
echo "Port:         $SSH_PORT"
echo "Tag:          $NODE_TAG"
echo ""
echo "Connect: ssh -p $SSH_PORT $SSH_USER@$DEVICE_IP"
echo "         mosh --ssh=\"ssh -p $SSH_PORT\" $SSH_USER@$DEVICE_IP"
echo ""
