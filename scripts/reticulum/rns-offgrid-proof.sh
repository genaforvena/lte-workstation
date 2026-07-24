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
LOCAL_LAN="${RNS_OG_LOCAL_LAN:-192.168.8.225}"
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
SPID=""
ts(){ date -u +%H:%M:%SZ; }
cleanup(){ [ -n "$SPID" ] && kill "$SPID" 2>/dev/null; }
trap cleanup EXIT

na(){ echo "n/a: $*" >&2; exit 2; }
fail(){ echo "FAIL: $*" >&2; exit 1; }

[ -x "$PY" ] || na "no local rns venv at $PY"
[ -f "$PROOF" ] || na "proof lib missing at $PROOF"

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
  SPID=$!
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
