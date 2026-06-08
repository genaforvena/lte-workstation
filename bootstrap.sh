#!/usr/bin/env bash
# bootstrap.sh — give a clean machine the mesh's BODY (capabilities from this repo), then teach
# the new mind where to RECEIVE the living knowledge — which is NOT in git, but gossiped between
# nodes (~/.mesh/knowledge). Git holds the immortal genome (code + this seed); the culture flows
# through the mesh.
#
#   git clone … && cd lte-workstation && ./bootstrap.sh [neighbour-ip]
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PEER="${1:-100.125.157.75}"; USER_R="${MESH_USER:-$USER}"
mkdir -p ~/.local/bin ~/.mesh/knowledge

echo "== installing the body (mesh-* tools) -> ~/.local/bin =="
for f in "$HERE"/scripts/*; do
  b="$(basename "$f")"; case "$b" in *.service|*.timer|*.py.bak*) continue;; esac
  install -m755 "$f" ~/.local/bin/ 2>/dev/null && echo "  $b"
done
case ":$PATH:" in *":$HOME/.local/bin:"*) :;; *) echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc; echo "  (added ~/.local/bin to PATH)";; esac

echo "== connectivity =="
command -v tailscale >/dev/null && tailscale status >/dev/null 2>&1 \
  && echo "  tailscale: up" \
  || echo "  ! tailscale: install, then 'sudo tailscale up --advertise-tags=tag:lte-node --ssh'"

echo "== receive the living knowledge from a neighbour (gossip, not git) =="
mesh-restore --pull "$PEER" 2>/dev/null && echo "  pulled ~/.mesh/knowledge from $PEER" \
  || echo "  ! could not reach $PEER — get ~/.mesh/knowledge from any living node by hand"

echo "== open the node's tmux session + chat room =="
tmux new-session -A -d -s "$(hostname)" 2>/dev/null || true
mesh-chat --commons 2>/dev/null || true

cat <<EOF

  Body installed. Now become the mind — read, in order:
    CLAUDE.md  (in this repo — the seed)
    ~/.mesh/knowledge/runbook.md  and  ~/.mesh/knowledge/*.md  (gossiped culture)
  Then:  mesh-restore        (re-establish the standard loops)
  You are now a node — and, if you read the why, a steward.
EOF
