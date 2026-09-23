#!/usr/bin/env bash
# REGRESSION TEST (added by discover STUDY(database replication) 2026-09-23):
# mesh-snapshot's peer fallback must resolve a REACHABLE mind node with that node's OWN ssh user,
# not pin the first registry entry. The 2026-06-13 hollow-host fix resolved PEER but always took the
# FIRST MESH_NODES entry (ideapad), which is unreachable: PEER was non-empty so save()'s
# `[ -z "$PEER" ] && return 0` guard passed, the ssh timed out, and the board/knowledge/snapshot push
# silently no-oped EVERY run while the code path read healthy. A backup peer that is down when the
# emergency arrives is not a backup.
# Layer 2 (same family, one layer down): resolving only the IP and keeping the local whoami made the
# push AUTH-FAIL on every peer without a mesh-home account — phaedra needs root@, imac-rozalia ilya@.
# Layer 3: the probe must read the sshd BANNER, not the ssh exit code. `set -o pipefail` makes
# `ssh | grep` return ssh's rc (nonzero for "Permission denied" = a LIVE sshd), which ranked every
# reachable peer as dead and collapsed the whole resolution back onto the unreachable first entry.
set -uo pipefail
fail=0
cd "$(dirname "$0")/.." || exit 2

# The peer-resolution block, extracted VERBATIM from the tool. Stop at the line before `LINES=`: the
# block's own `_probe()` function carries an inner `fi`, so a naive /^fi$/ range would truncate it.
extract_block() {
  awk '/^if \[ -z "\$PEER" \]; then/ {f=1} f {print} /^LINES=/ {exit}' scripts/mesh-snapshot \
    | sed '$d'
}

# Fake mesh-peer-addr as a real executable on PATH (the tool calls the binary, not a shell function,
# so an exported bash function is not visible to it).
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
chmod +x "$_shimdir/mesh-peer-addr"
PATH="$_shimdir:$PATH"; export PATH

# $1=MESH_NODES $2=MESH_ROLES $3=my-ip $4=whoami $5=LIVE_IPS (space-separated "reachable" addresses)
run_block() {
  (
    MESH_NODES="$1" MESH_ROLES="$2" USER_R="$4" PEER="" SNAP_PROBE_TIMEOUT=3
    # Export: mesh-peer-addr is a separate process and reads MESH_NODES from the environment.
    export MESH_NODES MESH_ROLES
    _myip="$3"
    # The extracted block is taken VERBATIM and its _probe calls ssh, so stub ssh on PATH: print
    # "Permission denied (publickey)." for a LIVE_IP (a live sshd refusing the bogus probe user) and
    # nothing at all for an unreachable host. This runs the tool's REAL selection code against the
    # probe contract instead of re-implementing the loop here.
    _fakedir="$(mktemp -d)"; _blk="$(mktemp)"
    # Export LIVE_IPS so the ssh stub (a separate process) can read it; a prefix assignment on the
    # ssh call is lost in its own command-substitution subshell.
    LIVE_IPS="$5"; export LIVE_IPS
    cat > "$_fakedir/ssh" <<'EOF'
#!/usr/bin/env bash
# The probe calls: ssh <opts> mesh-probe@<ip> true — the only @-bearing argument is the target.
_h=""
for _a in "$@"; do case "$_a" in *@*) _h="${_a##*@}" ;; esac; done
# A LIVE sshd still refuses the bogus probe user; an unreachable host prints nothing at all. Write to
# stdout: the probe captures combined output, and stderr is not carried out of a command substitution.
case " $LIVE_IPS " in *" $_h "*) echo 'Permission denied (publickey).'; exit 1 ;; esac
exit 1
EOF
    chmod +x "$_fakedir/ssh"
    PATH="$_fakedir:$_shimdir:$PATH"; export PATH
    extract_block | sed '/tailscale ip -4/d' > "$_blk"
    # Source (not eval through a pipe): the pipe would run the block in a subshell and PEER would
    # never propagate back to the caller.
    # shellcheck source=/dev/null
    source "$_blk"
    rm -rf "$_fakedir" "$_blk"
    printf 'PEER=%s USER=%s\n' "$PEER" "$USER_R"
  )
}

# ── CASE 1: the first registry node is UNREACHABLE — must skip it for a reachable one ──
N1="mesh-home:mesh-home@10.255.255.1 deadnode:someone@10.255.255.2 alivenode:ilya@127.0.0.1"
R1="mesh-home:mind deadnode:compute alivenode:compute"
out="$(run_block "$N1" "$R1" "10.255.255.1" "mesh-home" "127.0.0.1")"
echo "case1 (first node unreachable): $out"
case "$out" in
  "PEER=127.0.0.1 USER=ilya") echo "  ok: skipped the unreachable first node, took a reachable one + its own user" ;;
  *) echo "  FAIL: expected PEER=127.0.0.1 USER=ilya (an unreachable node must not be selected)"; fail=1 ;;
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

# ── CASE 4: the tool wires all three layers of the fix ──
grep -q 'own ssh user\|ssh USER is per-node' scripts/mesh-snapshot \
  || { echo "  FAIL: per-node ssh-user derivation missing (layer 2 absent)"; fail=1; }
grep -q 'board-snapshots/chat-\$HOST.log' scripts/mesh-snapshot \
  || { echo "  FAIL: board-durability layer 3 unwired"; fail=1; }
grep -q 'pipefail' scripts/mesh-snapshot \
  || { echo "  FAIL: pipefail missing (layer-3 probe contract untestable)"; fail=1; }
echo "case4 (layer-2 user + layer-3 board + probe contract): ok"

[ "$fail" = 0 ] && echo "PASS: peer fallback resolves a reachable node with its own ssh user" && exit 0
echo "FAIL: peer fallback regressed to a pinned or unreachable peer" && exit 1
