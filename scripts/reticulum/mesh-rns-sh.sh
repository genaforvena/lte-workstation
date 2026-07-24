#!/usr/bin/env bash
# mesh-rns-sh — ssh-FREE remote shell/exec over Reticulum. The "not-ssh" channel: an RNS Link,
# not a TCP ssh session, so it rides the LAN directly (no laggy tailscale/egress hop) and resumes
# across brief link drops instead of dying. rnsh = interactive shell (ssh replacement); rnx =
# one-shot command. Same E2E crypto, transport-agnostic — the SAME shell carries onto radio later.
#
#   mesh-rns-sh <node>            interactive shell on <node>            (rnsh)
#   mesh-rns-sh <node> <cmd...>   run one command on <node>, print out  (rnx)
#   mesh-rns-sh --serve           start THIS node's listeners (idempotent) + print its dest hashes
#   mesh-rns-sh --list            show the node registry
#
# Registry ~/.mesh/rns-nodes : lines "<node> <rnsh_hash> <rnx_hash>".
# Allowlist ~/.mesh/rns-allowed : client identity hashes permitted to connect (one per line).
# Needs an rnsd on the RNS network (mesh-reticulum.service on mesh-home; rns-up.sh joins a peer).
# orphan-ok: operator remote-access tool + node-local listener daemon — run on demand / kept up by
#            the shim's `--serve` reflex-cadence; the listener half is node-bound (each node serves
#            its own shell). Cadence lives on the deployed shim scripts/mesh-rns-sh (autowire scans
#            top-level scripts/, not this subdir).
set -uo pipefail
PY="${RNS_PY:-$HOME/.venv-rns/bin}"
REG="${MESH_RNS_NODES:-$HOME/.mesh/rns-nodes}"
ALLOW="${MESH_RNS_ALLOWED:-$HOME/.mesh/rns-allowed}"
EXID="$HOME/.mesh/rns-exec.id"

[ -x "$PY/rnx" ] || { echo "mesh-rns-sh: n/a — no rns venv at $PY" >&2; exit 2; }

allowed_flags(){  # emit "-a h1 -a h2 …" from the allowlist (empty => caller decides)
  [ -f "$ALLOW" ] || return 0
  while read -r h _; do case "$h" in ""|\#*) ;; *) printf ' -a %s' "$h";; esac; done < "$ALLOW"
}

serve(){
  [ -f "$EXID" ] || "$PY/rnid" -g "$EXID" >/dev/null 2>&1
  local af; af="$(allowed_flags)"
  # no allowlist yet → fail SAFE: refuse to open a no-auth shell to the whole RNS net
  [ -n "$af" ] || { echo "mesh-rns-sh --serve: REFUSING — $ALLOW empty (a listener with no -a is an open shell). Add trusted client identity hashes first." >&2; exit 2; }
  _up(){ local n="$1"; shift; local p="$HOME/.mesh/rns-$n.pid"
    if [ -f "$p" ] && kill -0 "$(cat "$p" 2>/dev/null)" 2>/dev/null; then return 0; fi
    nohup "$@" >"$HOME/.mesh/rns-$n.log" 2>&1 </dev/null & echo $! > "$p"; }
  # shellcheck disable=SC2086
  _up rnx  "$PY/rnx"  -l -i "$EXID" $af
  # shellcheck disable=SC2086
  _up rnsh "$PY/rnsh" -l $af
  sleep 3
  local rnxd rnshd
  rnxd=$("$PY/rnx" -i "$EXID" -p 2>/dev/null | awk '/Listening/{gsub(/[<>]/,"",$NF);print $NF}')
  rnshd=$("$PY/rnsh" -l -p 2>/dev/null | awk '/Listening/{gsub(/[<>]/,"",$NF);print $NF}')
  echo "$(hostname): rnsh=$rnshd rnx=$rnxd"
  echo "(add to peers' $REG:  $(hostname) $rnshd $rnxd)"
}

lookup(){ awk -v n="$1" '$1==n{print $2, $3; found=1} END{exit !found}' "$REG" 2>/dev/null; }

case "${1:-}" in
  ""|-h|--help) sed -n '2,14p' "$0"; exit 0 ;;
  --test)
    fails=0
    # 1) FAIL-SAFE contract: --serve must REFUSE (exit 2) on an empty allowlist (no open shell).
    _empty="$(mktemp)"; : > "$_empty"
    MESH_RNS_ALLOWED="$_empty" bash "$0" --serve >/dev/null 2>&1
    [ $? -eq 2 ] || { echo "test: FAIL (serve did not refuse empty allowlist — open-shell risk)"; fails=1; }
    rm -f "$_empty"
    # 2) allowed_flags emits one -a per non-comment entry
    _al="$(mktemp)"; printf 'aaaa\n# c\nbbbb\n' > "$_al"
    [ "$(ALLOW="$_al" allowed_flags)" = " -a aaaa -a bbbb" ] || { echo "test: FAIL (allowed_flags)"; fails=1; }
    rm -f "$_al"
    # 3) REAL-PATH: self-loop rnx round-trip through THIS node's own listener (needs rnsd+listener up).
    own_rnx="$(awk -v h="$(hostname)" '$1==h{print $3}' "$REG" 2>/dev/null)"
    if [ -n "$own_rnx" ] && [ -f "$HOME/.mesh/rns-rnx.pid" ] && kill -0 "$(cat "$HOME/.mesh/rns-rnx.pid" 2>/dev/null)" 2>/dev/null; then
      nonce="rnsselftest$$"
      out="$(timeout 25 "$PY/rnx" -i "$EXID" "$own_rnx" "echo $nonce" 2>/dev/null)"
      echo "$out" | grep -q "$nonce" || { echo "test: FAIL (self-loop rnx: no E2E round-trip through own listener)"; fails=1; }
    else
      [ "$fails" = 0 ] && { echo "test: n/a — no local rnsd/rnx listener or registry (honest exit 2)"; exit 2; }
    fi
    [ "$fails" = 0 ] && { echo "test: ok"; exit 0; } || exit 1 ;;
  --serve)  serve ;;
  --list)   { echo "node       rnsh_hash                         rnx_hash"; cat "$REG" 2>/dev/null; } ;;
  *)
    node="$1"; shift
    read -r rnsh_h rnx_h < <(lookup "$node") || { echo "mesh-rns-sh: unknown node '$node' (see --list; add to $REG)" >&2; exit 2; }
    if [ "$#" -eq 0 ]; then
      [ -n "${rnsh_h:-}" ] || { echo "mesh-rns-sh: no rnsh hash for $node" >&2; exit 2; }
      exec "$PY/rnsh" "$rnsh_h"                       # interactive shell
    else
      [ -n "${rnx_h:-}" ] || { echo "mesh-rns-sh: no rnx hash for $node" >&2; exit 2; }
      exec "$PY/rnx" -i "$EXID" "$rnx_h" "$*"         # one-shot command (identifies for -a auth)
    fi ;;
esac
