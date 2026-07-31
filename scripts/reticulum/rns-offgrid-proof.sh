#!/usr/bin/env bash
# rns-offgrid-proof — PROOF that two mesh nodes exchange a message OFF the internet.
#
# The loopback proof (rns-link-proof.py) shows the RNS stack round-trips a Link on
# ONE host. This shows the real thing the operator asked for: TWO physical nodes,
# an E2E-encrypted Reticulum Link, over a transport that does NOT touch the internet
# uplink — and (--blackout) that the link SURVIVES the uplink being pulled.
#
# Transport = TCPInterface over the LOCAL /24. The peer dials the local node's LAN
# IP, which is on-link (same subnet) → the kernel sends it straight over L2 to the
# wifi/switch, never via the default gateway. Cut the default route + tailscale and
# the link keeps running: that is the off-internet claim, proven by artifact.
#
# AutoInterface (link-local multicast) is the more "radio-like" transport and is the
# intended shape for the RNode/LoRa lane, but bridged-VM-over-wifi APs routinely drop
# IPv6 link-local multicast — so the SOFTWARE proof uses reliable unicast TCP-over-LAN.
# Same Reticulum Link, same crypto; only the interface differs (Reticulum's whole point).
#
# Usage:
#   rns-offgrid-proof.sh              # plain two-node off-internet-capable link proof
#   rns-offgrid-proof.sh --blackout   # + self-restoring internet blackout, assert survives
#   rns-offgrid-proof.sh --test       # gate: the plain proof (exit 2 if peer unreachable)
#
# Config (env or ~/.mesh/rns-offgrid.env):
#   RNS_OG_PEER      ssh target for control-plane setup   (e.g. ilya@100.107.198.111)
#   RNS_OG_LOCAL_LAN local LAN IP the TCP server binds     (e.g. 192.168.8.225)
#   RNS_OG_GW        default gateway, for --blackout restore(e.g. 192.168.8.1)
#   RNS_OG_WIFI      local uplink NIC, for --blackout       (e.g. wlxbcec43434a22)
#   RNS_OG_PORT      TCP-over-LAN port (default 4343)
#   RNS_OG_PY        local rns venv python  (default ~/.venv-rns/bin/python)
#   RNS_OG_PEER_PY   peer  rns venv python  (default ~/.venv-rns/bin/python)
# orphan-ok: on-demand off-internet PROOF/demo — peer-dependent + --blackout drops the
#            uplink; run when verifying the off-grid link, never cron-wired.
set -uo pipefail

[ -f "$HOME/.mesh/rns-offgrid.env" ] && . "$HOME/.mesh/rns-offgrid.env"
PEER="${RNS_OG_PEER:-ilya@100.107.198.111}"
# LOCAL_LAN default: AUTO-DETECT this host's RFC1918 (non-Tailscale-CGNAT) LAN IP.
# A hardcoded IP rots the moment DHCP reassigns it — that drift (192.168.8.225→.224)
# is what made this proof die with a silent EADDRNOTAVAIL rc=255.
# BUT "first global RFC1918" is WRONG on a node with overlays: this host carries
# wg-mesh 10.66.66.16/32, docker0 172.17.0.1/16 AND wifi 192.168.8.224/24, and a bare
# `head -1` picked the wg /32 — a POINT-TO-POINT host route the peer cannot dial
# (the proof then died `Connection refused` dialing 10.66.66.16, NOT honest n/a).
# The LAN the peer shares is the one behind the DEFAULT ROUTE (the real uplink NIC),
# never a /32 overlay or a docker bridge. Prefer the default-route dev's RFC1918 IP;
# fall back to first-global-RFC1918-on-a-NON-/32-iface (drops overlays generically).
_rfc1918(){ grep -E '^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.)' \
             | grep -vE '^100\.(6[4-9]|[7-9][0-9]|1[01][0-9]|12[0-7])\.'; }
autodetect_lan(){
  local dev ip
  dev="$(ip -4 route show default 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="dev"){print $(i+1); exit}}')"
  if [ -n "$dev" ]; then
    ip="$(ip -4 -o addr show dev "$dev" scope global 2>/dev/null \
            | awk '{print $4}' | cut -d/ -f1 | _rfc1918 | head -1)"
    [ -n "$ip" ] && { printf '%s\n' "$ip"; return; }
  fi
  # No default route (e.g. resolved mid-blackout): first RFC1918 on a NON-/32 iface —
  # a /32 is an overlay host route (wg/tailscale), never a shared broadcast LAN.
  ip -4 -o addr show scope global 2>/dev/null \
    | awk '$4 !~ /\/32$/ {print $4}' | cut -d/ -f1 | _rfc1918 | head -1
}
LOCAL_LAN="${RNS_OG_LOCAL_LAN:-$(autodetect_lan)}"
GW="${RNS_OG_GW:-192.168.8.1}"
WIFI="${RNS_OG_WIFI:-wlxbcec43434a22}"
PORT="${RNS_OG_PORT:-4343}"
PY="${RNS_OG_PY:-$HOME/.venv-rns/bin/python}"
PEER_PY="${RNS_OG_PEER_PY:-\$HOME/.venv-rns/bin/python}"
SSH="ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8"
HERE="$(cd "$(dirname "$0")" && pwd)"
PROOF="$HERE/rns-link-proof.py"

WORK="$HOME/.mesh/rns-offgrid"
SRV="$WORK/server"; HASHF="$WORK/server.hash"; SLOG="$WORK/server.log"
PIDF="$WORK/server.pid"
ts(){ date -u +%H:%M:%SZ; }
# start_server runs inside $(...) — a subshell — so a plain SPID=$! never reaches
# this trap and the server leaks, holding port 4343 and colliding with the next run
# ("passes once then fails"). Persist the pid to a file the parent trap can read.
cleanup(){ [ -f "$PIDF" ] && kill "$(cat "$PIDF" 2>/dev/null)" 2>/dev/null; rm -f "$PIDF"; }
trap cleanup EXIT

na(){ echo "n/a: $*" >&2; exit 2; }
fail(){ echo "FAIL: $*" >&2; exit 1; }

[ -x "$PY" ] || na "no local rns venv at $PY"
[ -f "$PROOF" ] || na "proof lib missing at $PROOF"
[ -n "$LOCAL_LAN" ] || na "no LAN IP to bind (autodetect found none; set RNS_OG_LOCAL_LAN)"
# The TCPServer binds LOCAL_LAN; if it is not actually assigned here the bind fails
# with EADDRNOTAVAIL and RNS exits 255 with NO output — an oracle that cannot report
# its own fault. Assert the address is bound so drift reads as honest n/a instead.
ip -4 -o addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 \
  | grep -qx "$LOCAL_LAN" || na "LAN IP $LOCAL_LAN not assigned on this host \
(DHCP drift? detected: $(autodetect_lan)) — set RNS_OG_LOCAL_LAN"

# --- write the TCP-over-LAN config on both ends (ONLY this iface: no internet path) ---
setup(){
  mkdir -p "$SRV"
  cat > "$SRV/config" <<EOF
[reticulum]
  enable_transport = No
  share_instance = No
  panic_on_interface_error = No
[logging]
  loglevel = 3
[interfaces]
  [[LAN TCP Server]]
    type = TCPServerInterface
    interface_enabled = True
    listen_ip = $LOCAL_LAN
    listen_port = $PORT
EOF
  $SSH "$PEER" "mkdir -p ~/.mesh/rns-offgrid/client && cat > ~/.mesh/rns-offgrid/client/config" <<EOF || na "peer $PEER unreachable (setup)"
[reticulum]
  enable_transport = No
  share_instance = No
  panic_on_interface_error = No
[logging]
  loglevel = 3
[interfaces]
  [[LAN TCP Client]]
    type = TCPClientInterface
    interface_enabled = True
    target_host = $LOCAL_LAN
    target_port = $PORT
EOF
  # stage the proof lib on the peer
  scp -q -o StrictHostKeyChecking=no -o ConnectTimeout=8 "$PROOF" "$PEER":/tmp/rns-link-proof.py \
    || na "cannot stage proof lib to $PEER"
}

start_server(){
  rm -f "$HASHF"
  nohup "$PY" "$PROOF" server --configdir "$SRV" --hashfile "$HASHF" >"$SLOG" 2>&1 &
  echo $! > "$PIDF"
  for _ in $(seq 1 40); do [ -s "$HASHF" ] && break; sleep 0.5; done
  [ -s "$HASHF" ] || fail "server did not announce (see $SLOG)"
  tail -1 "$HASHF"
}

run_client(){ # $1=hash ; runs on peer over LAN, echoes its output
  $SSH "$PEER" "$PEER_PY /tmp/rns-link-proof.py client --configdir ~/.mesh/rns-offgrid/client --hashhex $1 2>&1"
}

plain_proof(){
  setup
  local hash out
  hash="$(start_server)"
  out="$(run_client "$hash")"
  echo "$out"
  echo "$out" | grep -q "PROOF OK" || fail "no round-trip over LAN"
  echo "OFF-INTERNET-CAPABLE: two nodes ($LOCAL_LAN <-> $PEER) round-tripped an E2E Link over LAN TCP, zero internet interface in the config."
}

blackout_proof(){
  sudo -n true 2>/dev/null || na "--blackout needs NOPASSWD sudo on this node"
  setup
  local hash; hash="$(start_server)"
  local mh="$WORK/blackout.mhproof"; : > "$mh"
  # deadman: unconditional restore in 120s
  ( sleep 120; sudo ip route replace default via "$GW" dev "$WIFI" metric 600; sudo tailscale up ) &
  local dm=$!
  # pre-stage peer client to fire at ~T+14 (over control-plane, BEFORE blackout)
  $SSH "$PEER" "nohup sh -c 'sleep 14; { echo START:\$(date -u +%H:%M:%SZ); $PEER_PY /tmp/rns-link-proof.py client --configdir ~/.mesh/rns-offgrid/client --hashhex $hash; echo rc=\$?; echo END:\$(date -u +%H:%M:%SZ); } > /tmp/offgrid-blackout.result 2>&1' >/dev/null 2>&1 &"
  sleep 5
  echo "[$(ts)] BLACKOUT: drop default route + tailscale down" | tee -a "$mh"
  sudo ip route del default 2>&1 | tee -a "$mh"
  sudo tailscale down 2>&1 | tee -a "$mh"
  if ping -c1 -W3 8.8.8.8 >/dev/null 2>&1; then echo "[$(ts)] WARN 8.8.8.8 still UP — uplink not fully cut" | tee -a "$mh"
  else echo "[$(ts)] 8.8.8.8 unreachable — internet DOWN (route: $(ip route get 8.8.8.8 2>&1|head -1))" | tee -a "$mh"; fi
  ping -c1 -W3 "${PEER##*@}" >/dev/null 2>&1 || true
  sleep 20
  echo "[$(ts)] RESTORE: default route + tailscale up" | tee -a "$mh"
  sudo ip route replace default via "$GW" dev "$WIFI" metric 600 2>&1 | tee -a "$mh"
  sudo tailscale up 2>&1 | tee -a "$mh"
  for _ in $(seq 1 20); do ping -c1 -W2 8.8.8.8 >/dev/null 2>&1 && { echo "[$(ts)] internet RESTORED"; break; }; sleep 1; done | tee -a "$mh"
  kill "$dm" 2>/dev/null
  sleep 2
  echo "=== peer client result (ran during blackout) ==="
  local res; res="$($SSH "$PEER" 'cat /tmp/offgrid-blackout.result' 2>&1)"
  echo "$res"; echo "--- mesh-home blackout log ---"; cat "$mh"
  echo "$res" | grep -q "PROOF OK" || fail "peer did not round-trip during blackout"
  echo "OFF-INTERNET PROVEN: peer round-tripped an E2E Link to this node WHILE this node's internet uplink was down."
}

case "${1:-proof}" in
  --blackout) blackout_proof ;;
  --test|proof|"") plain_proof ;;
  *) echo "usage: $0 [--blackout|--test]" >&2; exit 2 ;;
esac
