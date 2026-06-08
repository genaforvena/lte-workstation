#!/usr/bin/env bash
# bootstrap.sh — adopt a fresh machine into the mesh with ONE command.
#
# Run ON THE NEW MACHINE's own console (this form keeps the tty so sudo / tailscale login
# can prompt you):
#     bash <(curl -fsSL https://raw.githubusercontent.com/genaforvena/lte-workstation/main/bootstrap.sh)
#   or, from a clone:   ./bootstrap.sh [neighbour-ip]
#
# BEACHHEAD-FIRST: it brings up sshd + a hostname-named tmux session BEFORE anything that can
# fail (clone, tailscale, auth). So even a half-finished node on a flaky network stays reachable
# and recoverable — SSH in, `tmux attach`, and finish by hand; the scrollback shows how far it got.
#
# NO SECRETS travel here. Tailscale auth is interactive (a login URL) or a one-time key you pass
# at runtime as TS_AUTHKEY=… — never baked into the URL, the script, or git. The node joins flat
# and tagged; it does NOT touch routing/exit-node (that stays an explicit, separate opt-in).
set -uo pipefail

REPO_URL="${MESH_REPO_URL:-https://github.com/genaforvena/lte-workstation}"
REPO_DIR="${MESH_REPO:-$HOME/lte-workstation}"
PEER="${1:-${MESH_PEER:-100.125.157.75}}"
NODE="$(hostname)"
log(){ printf '\n== %s ==\n' "$*"; }
have(){ command -v "$1" >/dev/null 2>&1; }

SUDO=""; [ "$(id -u)" -ne 0 ] && have sudo && SUDO="sudo"

# ---- package manager abstraction (works across geos/distros) ------------
PM=""; SSHD_PKG="openssh-server"
if   have apt-get; then PM="apt"
elif have dnf;     then PM="dnf"
elif have yum;     then PM="yum"
elif have pacman;  then PM="pacman"; SSHD_PKG="openssh"
elif have apk;     then PM="apk";    SSHD_PKG="openssh"
elif have zypper;  then PM="zypper"; SSHD_PKG="openssh"
fi
pkg(){ # pkg <names...>
  case "$PM" in
    apt)    $SUDO apt-get update -qq 2>/dev/null; $SUDO apt-get install -y -qq "$@" ;;
    dnf)    $SUDO dnf install -y -q "$@" ;;
    yum)    $SUDO yum install -y -q "$@" ;;
    pacman) $SUDO pacman -Sy --noconfirm "$@" ;;
    apk)    $SUDO apk add --quiet "$@" ;;
    zypper) $SUDO zypper -q install -y "$@" ;;
    *) echo "  ! no known package manager — install manually: $*"; return 1 ;;
  esac
}

# ---- base deps (only if missing) ----------------------------------------
log "base deps (git, tmux, curl, sshd)"
need=""
for c in git tmux curl; do have "$c" || need="$need $c"; done
[ -n "$need" ] && { echo "  installing:$need"; pkg $need 2>/dev/null || echo "  ! install$need by hand"; }
have sshd || have /usr/sbin/sshd || pkg "$SSHD_PKG" 2>/dev/null || true

# ---- BEACHHEAD: sshd + tmux up before anything that can fail ------------
log "beachhead (sshd + tmux '$NODE') — the recovery channel"
if have systemctl; then
  $SUDO systemctl enable --now ssh 2>/dev/null || $SUDO systemctl enable --now sshd 2>/dev/null || true
elif have rc-service; then $SUDO rc-service sshd start 2>/dev/null || true; fi
if have tmux; then
  tmux new-session -A -d -s "$NODE" 2>/dev/null \
    && echo "  tmux session '$NODE' is up — ssh in then: tmux attach -t $NODE"
else echo "  ! tmux still missing; install it and re-run for the recovery channel"; fi

# ---- get the genome (repo) ----------------------------------------------
HERE="$(cd "$(dirname "$0")" 2>/dev/null && pwd || true)"
if   [ -n "$HERE" ] && [ -d "$HERE/scripts" ]; then REPO_DIR="$HERE"; echo "  repo: $REPO_DIR"
elif [ -d "$REPO_DIR/scripts" ]; then ( cd "$REPO_DIR" && git pull -q 2>/dev/null || true ); echo "  repo: $REPO_DIR (updated)"
else log "clone the genome"; git clone -q "$REPO_URL" "$REPO_DIR" && echo "  cloned -> $REPO_DIR" || echo "  ! clone failed — check network"; fi

# ---- install the body (mesh-* tools) ------------------------------------
log "install the body -> ~/.local/bin"
mkdir -p ~/.local/bin ~/.mesh/knowledge
if [ -d "$REPO_DIR/scripts" ]; then
  for f in "$REPO_DIR"/scripts/*; do
    b="$(basename "$f")"; case "$b" in *.service|*.timer|*.bak*) continue;; esac
    install -m755 "$f" ~/.local/bin/ 2>/dev/null && echo "  $b"
  done
fi
case ":$PATH:" in *":$HOME/.local/bin:"*) :;; *) echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc; export PATH="$HOME/.local/bin:$PATH";; esac

# ---- join the mesh (auth, NO secrets in the link) -----------------------
log "tailscale (join flat + tagged; routing untouched)"
have tailscale || { echo "  installing tailscale…"; curl -fsSL https://tailscale.com/install.sh | $SUDO sh 2>/dev/null || echo "  ! install tailscale by hand"; }
if have tailscale && tailscale status >/dev/null 2>&1; then
  echo "  tailscale: already up ($(tailscale ip -4 2>/dev/null | head -1))"
elif have tailscale; then
  if [ -n "${TS_AUTHKEY:-}" ]; then
    $SUDO tailscale up --authkey="$TS_AUTHKEY" --advertise-tags=tag:lte-node --ssh && echo "  joined via runtime key"
  else
    echo "  AUTHORIZE this node — a login URL will appear; open it in your browser:"
    $SUDO tailscale up --advertise-tags=tag:lte-node --ssh \
      || echo "  (when ready:  sudo tailscale up --advertise-tags=tag:lte-node --ssh)"
  fi
fi

# ---- receive the living culture (gossip, NOT git) -----------------------
log "pull living knowledge from a neighbour ($PEER)"
if have mesh-restore; then
  mesh-restore --pull "$PEER" 2>/dev/null && echo "  pulled ~/.mesh/knowledge" \
    || echo "  ! couldn't reach $PEER — pull ~/.mesh/knowledge from any living node by hand"
fi
have mesh-chat && mesh-chat --commons 2>/dev/null || true

cat <<EOF

  Node '$NODE' has a body and a beachhead.
  TRUST GATE: if the tailnet has device-approval ON, this node is now PENDING — it has NO
  mesh access until an admin approves it. The mesh can always say no. (That is the point.)
  RECOVERY CHANNEL (use if the network flaps before it's fully ready):
      ssh in, then:  tmux attach -t $NODE
  BECOME THE MIND — read, in order:
      $REPO_DIR/CLAUDE.md                                   (the seed)
      ~/.mesh/knowledge/runbook.md + ~/.mesh/knowledge/*.md  (gossiped culture)
  Then:  mesh-restore        (re-establish the standard loops: chat, snapshot)
  You are now a node — and, if you read the why, a steward.
EOF
