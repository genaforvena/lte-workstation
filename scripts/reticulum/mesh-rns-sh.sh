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
PIDDIR="${MESH_RNS_PIDDIR:-$HOME/.mesh}"   # pid/log dir for the listeners (overridable so --test can drive _up)

# --- reconnect (interactive shell) tuning; overridable + injectable for --test ---
RNSH_BIN="${MESH_RNSH_BIN:-$PY/rnsh}"   # the wrapped binary (a stub in --test)
RNS_SLEEP="${MESH_RNS_SLEEP:-sleep}"    # replaced by `true` in --test to skip the countdown
RNS_MAX="${MESH_RNS_RECONNECT_MAX:-20}" # reconnect budget after a drop before giving up
RNS_STABLE="${MESH_RNS_STABLE_SECS:-30}" # a session that ran >= this long earns a FRESH budget
# far-side default command for served rnsh: a persistent tmux so the shell (and any running
# job) SURVIVES a link drop — reconnect re-attaches the same session, not a fresh shell.
# Set MESH_RNS_TMUX="" to serve a plain login shell instead.
RNS_TMUX="${MESH_RNS_TMUX-rns}"

[ -x "$PY/rnx" ] || { echo "mesh-rns-sh: n/a — no rns venv at $PY" >&2; exit 2; }

# new attempt counter for a session that just ended: a stable (long) session resets the budget to
# 0, so a normally-solid link that drops now and then never exhausts its retries; a session that
# died fast bumps the counter toward the cap. Pure + testable: echoes the new attempt number.
_reconnect_attempt(){ # elapsed prev_attempt
  if [ "${1:-0}" -ge "$RNS_STABLE" ]; then echo 0; else echo $(( ${2:-0} + 1 )); fi
}
# backoff seconds for an attempt: 1,2,4,8,16 (capped). Pure + testable.
_backoff(){ local a="${1:-0}"; [ "$a" -gt 4 ] && a=4; echo $(( 1 << a )); }

# the interactive shell as a reconnect LOOP (not exec): rnsh has no resume, and a dropped link
# and a clean exit both surface as rc 0, so the ONLY trustworthy "the human wants out" signal is
# them aborting the reconnect countdown (Ctrl-C) — everything else is treated as a recoverable
# drop and re-dialled, bounded by the budget+backoff. Uses $RNSH_BIN/$RNS_SLEEP so --test can
# drive the REAL loop against a controllable stub.
_interactive_loop(){ # node rnsh_hash
  local node="$1" hash="$2" attempt=0 start end elapsed rc d
  while :; do
    start="$(date +%s)"
    "$RNSH_BIN" -i "$EXID" "$hash"; rc=$?
    end="$(date +%s)"; elapsed=$(( end - start ))
    attempt="$(_reconnect_attempt "$elapsed" "$attempt")"
    if [ "$attempt" -ge "$RNS_MAX" ]; then
      echo "mesh-rns-sh: link to $node ended (rc=$rc) — reconnect budget exhausted ($RNS_MAX). Giving up." >&2
      return "$rc"
    fi
    d="$(_backoff "$attempt")"
    echo "mesh-rns-sh: link to $node ended (rc=$rc) — reconnecting in ${d}s [attempt $attempt/$RNS_MAX] (Ctrl-C to quit)…" >&2
    trap 'echo; echo "mesh-rns-sh: reconnect cancelled — bye." >&2; return 0' INT
    "$RNS_SLEEP" "$d"
    trap - INT
  done
}

allowed_flags(){  # emit "-a h1 -a h2 …" from the allowlist (empty => caller decides)
  [ -f "$ALLOW" ] || return 0
  while read -r h _; do case "$h" in ""|\#*) ;; *) printf ' -a %s' "$h";; esac; done < "$ALLOW"
}

# IDEMPOTENT ON THE ARGUMENTS, NOT JUST ON A LIVE PID (2026-07-24 incident, task reticulum-rns-sh).
# `--serve` used to return early whenever the pid file's process was alive. So when the listener's
# command line CHANGED in the code — the persistent far-side tmux (`-- tmux new-session -A -s rns`)
# landed at 13:48 — every 5-minute keepalive pass on a peer kept the OLD 10:12 listener alive
# instead: a permanently green reflex tending an outdated organ, plain-shell far side, so a dropped
# link had nothing to re-attach to and the operator's "still disconnects, no re-attach" was true on
# a node whose keepalive said everything was fine. Liveness is not correctness. Compare the RUNNING
# cmdline to the one we would start and restart on drift.
# The comparison is a SUFFIX match, not equality: rnsh/rnx are python entry points, so /proc shows
# `…/python3 …/rnsh -l -a …` while we invoke `…/rnsh -l -a …` — an equality test would never match
# and would restart the listener on every single pass (a restart storm dressed as a fix).
_up(){ local n="$1"; shift; local p="$PIDDIR/rns-$n.pid" pid have want
  want="$*"
  if [ -f "$p" ] && pid="$(cat "$p" 2>/dev/null)" && kill -0 "$pid" 2>/dev/null; then
    have="$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null | sed 's/ *$//')"
    case "$have" in
      *"$want") return 0 ;;                       # running exactly what we would start → leave it
      "") return 0 ;;                             # cmdline unreadable → do NOT churn a live listener
      *) echo "mesh-rns-sh --serve: RESTARTING $n listener — its args are stale (running: $have)" >&2
         kill "$pid" 2>/dev/null; sleep 1 ;;
    esac
  fi
  nohup "$@" >"$PIDDIR/rns-$n.log" 2>&1 </dev/null & echo $! > "$p"; }

serve(){
  [ -f "$EXID" ] || "$PY/rnid" -g "$EXID" >/dev/null 2>&1
  local af; af="$(allowed_flags)"
  # no allowlist yet → fail SAFE: refuse to open a no-auth shell to the whole RNS net
  [ -n "$af" ] || { echo "mesh-rns-sh --serve: REFUSING — $ALLOW empty (a listener with no -a is an open shell). Add trusted client identity hashes first." >&2; exit 2; }
  # shellcheck disable=SC2086
  _up rnx  "$PY/rnx"  -l -i "$EXID" $af
  # rnsh listener serves a PERSISTENT tmux by default (survives link drops → reconnect re-attaches
  # the same shell). The rnx one-shot listener above is untouched — commands still run directly.
  if [ -n "$RNS_TMUX" ]; then
    # shellcheck disable=SC2086
    _up rnsh "$PY/rnsh" -l $af -- tmux new-session -A -s "$RNS_TMUX"
  else
    # shellcheck disable=SC2086
    _up rnsh "$PY/rnsh" -l $af
  fi
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
    # 3a) RECONNECT decision logic (pure): stable session resets budget, fast death bumps it.
    [ "$( RNS_STABLE=30; _reconnect_attempt 40 5 )" = 0 ]  || { echo "test: FAIL (_reconnect_attempt: stable session must reset budget to 0)"; fails=1; }
    [ "$( RNS_STABLE=30; _reconnect_attempt 2 5 )"  = 6 ]  || { echo "test: FAIL (_reconnect_attempt: fast death must bump budget)"; fails=1; }
    [ "$(_backoff 0)" = 1 ] && [ "$(_backoff 3)" = 8 ] && [ "$(_backoff 9)" = 16 ] || { echo "test: FAIL (_backoff: expected 1,8,16 capped)"; fails=1; }
    # 3b) RECONNECT LOOP (real control flow, stubbed binary): a stub that always "drops" (rc 1) must
    #     be RE-INVOKED until the budget caps — exercising the actual loop, backoff-skip, and give-up,
    #     not a mock of them. Asserts the wrapper re-dialled exactly RNS_MAX times then exited (no hang).
    _cnt="$(mktemp)"; _stub="$(mktemp)"
    printf '#!/usr/bin/env bash\necho x >> "%s"\nexit 1\n' "$_cnt" > "$_stub"; chmod +x "$_stub"
    MESH_RNSH_BIN="$_stub" MESH_RNS_SLEEP=true MESH_RNS_RECONNECT_MAX=3 MESH_RNS_STABLE_SECS=999 \
      timeout 10 bash "$0" --_loop testnode deadbeef >/dev/null 2>&1
    _got="$(wc -l < "$_cnt" | tr -d ' ')"
    [ "$_got" = 3 ] || { echo "test: FAIL (reconnect loop: stub re-invoked $_got times, expected 3=RNS_MAX)"; fails=1; }
    rm -f "$_cnt" "$_stub"
    # 2c) ARGS-DRIFT RESTART (the 2026-07-24 incident gate). A keepalive that returns early on a LIVE
    #     pid keeps an outdated listener forever — that is how a peer served a plain-shell far side all
    #     day while its 5-minute timer stayed green. Drive the REAL _up against a stub listener:
    #       · same args      → the pid must NOT change (no restart storm; this is the falsifier for a
    #                          naive equality check, since /proc prepends the interpreter path)
    #       · changed args   → the pid MUST change and the old process MUST be dead
    _pd="$(mktemp -d)"; _stub="$_pd/fakelistener"
    printf '#!/usr/bin/env bash\nsleep 120   # NOT exec: exec would replace the cmdline and the drift check would read "sleep 120"\n' > "$_stub"; chmod +x "$_stub"
    # start it the way python entry points appear in /proc: interpreter first, then the script+args
    nohup bash "$_stub" -l -a AAAA -- tmux new-session -A -s rns >/dev/null 2>&1 </dev/null &
    _p1=$!; echo "$_p1" > "$_pd/rns-fake.pid"; sleep 0.3
    PIDDIR="$_pd" _up fake bash "$_stub" -l -a AAAA -- tmux new-session -A -s rns
    _p2="$(cat "$_pd/rns-fake.pid")"
    [ "$_p2" = "$_p1" ] || { echo "test: FAIL (args-drift: identical args RESTARTED the listener — suffix match broken, every keepalive pass would churn it)"; fails=1; }
    PIDDIR="$_pd" _up fake bash "$_stub" -l -a AAAA   # the OLD (pre-tmux) arg set = a drift
    _p3="$(cat "$_pd/rns-fake.pid")"
    [ "$_p3" != "$_p2" ] || { echo "test: FAIL (args-drift: a STALE-args listener was left running — the incident's root cause)"; fails=1; }
    kill -0 "$_p2" 2>/dev/null && { echo "test: FAIL (args-drift: old listener still alive after restart)"; fails=1; }
    kill "$_p3" 2>/dev/null; pkill -f "$_stub" 2>/dev/null; rm -rf "$_pd"

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
  --_loop)  _interactive_loop "${2:-testnode}" "${3:-deadbeef}" ;; # hidden: --test drives the real loop
  --serve)  serve ;;
  --list)   { echo "node       rnsh_hash                         rnx_hash"; cat "$REG" 2>/dev/null; } ;;
  *)
    node="$1"; shift
    read -r rnsh_h rnx_h < <(lookup "$node") || { echo "mesh-rns-sh: unknown node '$node' (see --list; add to $REG)" >&2; exit 2; }
    # ONE client identity for both channels: rnsh must identify with the SAME EXID as rnx, else the
    # interactive shell presents rnsh's default (un-allowlisted) identity → "Identity not allowed"
    # while one-shot rnx (which passes -i) works — the exact split the operator hit (2026-07-24).
    [ -f "$EXID" ] || "$PY/rnid" -g "$EXID" >/dev/null 2>&1
    if [ "$#" -eq 0 ]; then
      [ -n "${rnsh_h:-}" ] || { echo "mesh-rns-sh: no rnsh hash for $node" >&2; exit 2; }
      _interactive_loop "$node" "$rnsh_h"; exit $?   # interactive shell w/ auto-reconnect on drop
    else
      [ -n "${rnx_h:-}" ] || { echo "mesh-rns-sh: no rnx hash for $node" >&2; exit 2; }
      exec "$PY/rnx" -i "$EXID" "$rnx_h" "$*"         # one-shot command (identifies for -a auth)
    fi ;;
esac
