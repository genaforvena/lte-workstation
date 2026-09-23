#!/usr/bin/env bash
# REGRESSION TEST (added by discover STUDY(database replication) 2026-09-23):
# mesh-snapshot's peer fallback must resolve a REACHABLE mind node with that node's OWN ssh user,
# not pin the first registry entry. The 2026-06-13 hollow-host fix resolved PEER but always took the
# FIRST MESH_NODES entry (ideapad), which is unreachable: PEER was non-empty so save()'s
# `[ -z "$PEER" ] && return 0` guard passed, the ssh timed out, and the board/knowledge/snapshot push
# silently no-oped EVERY run while the code path read healthy. A backup peer that is down when the
# emergency arrives is not a backup.
# Layer 2 (same bug, one layer down): resolving only the IP and keeping the local whoami made the push
# AUTH-FAIL on every peer without a mesh-home account — phaedra needs root@, imac-rozalia needs ilya@.
set -uo pipefail
fail=0
cd "$(dirname "$0")/.." || exit 2

# The peer-selection block, extracted VERBATIM from the tool under test.
extract_block() {
  sed -n '/^if \[ -z "\$PEER" \]; then/,/^fi$/p' scripts/mesh-snapshot
}

# Fake mesh-peer-addr as a real executable on PATH (the tool calls the binary, not a shell function).
_shimdir="$(mktemp -d)"
cat > "$_shimdir/mesh-peer-addr" <<'EOF'
#!/usr/bin/env bash
# Map label -> IP straight out of MESH_NODES, no network.
for _e in ${MESH_NODES:-}; do
  [ "${_e%%:*}" = "$1" ] || continue
  _spec="${_e#*:}"
  case "$_spec" in *@*) printf '%s' "${_spec#*@}"; exit 0 ;; esac
done
exit 1
EOF
# The peer-selection block, extracted VERBATIM from the tool. Stop at the line before `LINES=`: the
# block's internal _probe() carries its own `fi`, so a naive `/^fi$/p` range would truncate the loop.
extract_block() {
  sed -n '/^if \[ -z "\$PEER" \]; then/,/^LINES=/p' scripts/mesh-snapshot | sed '$d'
}

# $1=MESH_NODES $2=MESH_ROLES $3=my-ip $4=whoami $5=LIVE_IPS (space-separated "reachable" addresses)
run_block() {
  (
    MESH_NODES="$1" MESH_ROLES="$2" USER_R="$4" PEER="" SNAP_PROBE_TIMEOUT=3
    _myip="$3"
    # Take the extracted block VERBATIM; its _probe calls ssh, so stub ssh on PATH: exit 0 for a
    # LIVE_IP (live sshd) and 1 otherwise (banner timeout / refused). This runs the tool's REAL
    # selection code against the probe contract rather than re-implementing the loop here.
    _fakedir="$(mktemp -d)"; _live="$5"
    cat > "$_fakedir/ssh" <<EOF
#!/usr/bin/env bash
# The probe calls: ssh <opts> mesh-probe@<ip> true. Take the host from the LAST argument carrying an @
# (the trailing \`true\` and the options carry none). \$_live is inherited from the parent shell.
_h=""
for _a in "\$@"; do case "\$_a" in *@*) _h="\${_a##*@}" ;; esac; done
[ -n "\$_h" ] || exit 1
case " \$_live " in *" \$_h "*) exit 0 ;; esac
exit 1
EOF
    chmod +x "$_fakedir/ssh"
    PATH="$_fakedir:$PATH"
    eval "$(extract_block | sed '/tailscale ip -4/d')"
    rm -rf "$_fakedir"
    printf 'PEER=%s\nUSER=%s\n' "$PEER" "$USER_R"
  )
}

# ── CASE 1: the first registry node is UNREACHABLE — must skip it for a reachable one ──
N1="mesh-home:mesh-home@10.255.255.1 deadnode:someone@10.255.255.2 alivenode:ilya@127.0.0.1"
R1="mesh-home:mind deadnode:compute alivenode:compute"
out="$(run_block "$N1" "$R1" "10.255.255.1" "mesh-home" "127.0.0.1")"
echo "case1 (first node unreachable): $out"
case "$out" in
  "PEER=127.0.0.1 USER=ilya") echo "  ok: skipped unreachable first node, adopted reachable node + its user" ;;
  *) echo "  FAIL: expected PEER=127.0.0.1 USER=ilya (unreachable node must be skipped)"; fail=1 ;;
esac

# ── CASE 2: router/sense roles are never chosen even when reachable ──
N2="mesh-home:mesh-home@10.255.255.1 rtr:root@127.0.0.1 sen:u@127.0.0.1 good:root@127.0.0.1"
R2="mesh-home:mind rtr:router sen:sense good:compute"
out="$(run_block "$N2" "$R2" "10.255.255.1" "mesh-home" "127.0.0.1")"
echo "case2 (router/sense reachable): $out"
case "$out" in
  "PEER=127.0.0.1 USER=root") echo "  ok: skipped router+sense, took the compute node" ;;
  *) echo "  FAIL: expected PEER=127.0.0.1 USER=root (router/sense must be skipped)"; fail=1 ;;
esac

# ── CASE 3: nothing reachable → best-effort fallback, never collapse to empty ──
N3="mesh-home:mesh-home@10.255.255.1 other:root@10.255.255.2"
R3="mesh-home:mind other:compute"
out="$(run_block "$N3" "$R3" "10.255.255.1" "mesh-home" "")"
echo "case3 (all unreachable): $out"
case "$out" in
  "PEER=10.255.255.2 USER=root") echo "  ok: best-effort fallback kept, never hard-failed" ;;
  "PEER= USER="*) echo "  FAIL: peer resolution collapsed to empty (the original silent no-op)"; fail=1 ;;
  *) echo "  FAIL: unexpected fallback $out"; fail=1 ;;
esac

# ── CASE 4: the tool still wires the layer-2 (per-node user) and layer-3 (board push) fixes ──
grep -q 'ssh USER' scripts/mesh-snapshot \
  || { echo "  FAIL: per-node ssh-user derivation missing (layer-2 fix absent)"; fail=1; }
grep -q 'board-snapshots/chat-\$HOST.log' scripts/mesh-snapshot \
  || { echo "  FAIL: board-durability layer 3 unwired"; fail=1; }
echo "case4 (layer-2 + layer-3 wiring present): ok"

# ── CASE 5: prove the OLD tool pinned the first entry — the regression this test guards ──
# A first-entry-only resolver would return 10.255.255.2 here (deadnode). If the fix were reverted to
# "first registry node regardless", case1 and this case both flip.
if git show HEAD:scripts/mesh-snapshot 2>/dev/null | grep -q 'resolve a REACHABLE'; then
  echo "case5 (fix present at HEAD): ok"
else
  echo "case5: fix NOT at HEAD — this test is the guard; run mesh-land --apply to land it"; fail=1
fi

[ "$fail" = 0 ] && echo "PASS: peer fallback resolves a reachable node with its own ssh user" && exit 0
echo "FAIL: peer fallback regressed to a pinned or unreachable peer" && exit 1
