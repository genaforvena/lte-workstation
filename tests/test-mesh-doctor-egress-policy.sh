#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
doctor="${MESH_DOCTOR_SCRIPT:-$repo/scripts/mesh-doctor}"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# Load the production policy/check functions without entering mesh-doctor's broad live scan.
awk '
  /^_sc_egress_policy_role\(\)[[:space:]]*\{/ || /^_sc_egress_fib_exclusion\(\)[[:space:]]*\{/ || /^_sc_egress_integrity\(\)[[:space:]]*\{/ { copying=1 }
  copying { print }
  copying && /^\}$/ { print ""; copying=0; found++ }
  END { if (found != 3) exit 1 }
' "$doctor" > "$tmp/egress-functions.sh" || {
  echo "FAIL: expected production egress policy functions in $doctor" >&2
  exit 1
}
. "$tmp/egress-functions.sh"

pass(){ printf 'PASS %s\n' "$*"; }
note(){ printf 'NOTE %s\n' "$*"; }
warn(){ printf 'WARN %s\n' "$*"; }
fail(){ printf 'FAIL %s\n' "$*"; }

mesh-card(){
  [ "${1:-}" = "--exit-node-lan" ] || return 2
  printf 'state: %s\n' "${MESH_TEST_FIB_STATE:-ok}"
  printf 'net: 192.168.8.0/24\ntable: 52\n'
  [ "${MESH_TEST_FIB_STATE:-ok}" != swallowed ]
}

cat > "$tmp/consumer.card" <<'EOF'
hostname: mesh-home
capabilities:
  compute: primary
  connectivity: shadowsocks
EOF
cat > "$tmp/provider.card" <<'EOF'
hostname: phaedra
capabilities:
  connectivity: exit-node
EOF
cat > "$tmp/direct.card" <<'EOF'
hostname: direct-node
capabilities:
  connectivity: (none)
EOF

assert_case(){
  local label="$1" card="$2" dev="$3" xid="$4" fib="${5:-ok}" want="$6" out
  out="$(MESH_TEST_FIB_STATE="$fib" _sc_egress_integrity "$card" "$dev" "$xid" 2>&1)"
  if ! grep -Fq -- "$want" <<<"$out"; then
    printf 'FAIL: %s\nexpected: %s\nactual:\n%s\n' "$label" "$want" "$out" >&2
    exit 1
  fi
  printf 'ok: %s\n' "$label"
}

assert_case "configured consumer accepts overlay egress and still checks LAN FIB" \
  "$tmp/consumer.card" tailscale0 exit-node-id ok \
  "PASS egress dev=tailscale0 via configured exit-node exit-node-id (consumer policy)"
consumer_ok="$(MESH_TEST_FIB_STATE=ok _sc_egress_integrity "$tmp/consumer.card" tailscale0 exit-node-id 2>&1)"
grep -Fq 'PASS exit-node LAN-prefix FIB exclusion: ok' <<<"$consumer_ok" || {
  printf 'FAIL: consumer path omitted the real LAN-prefix FIB check:\n%s\n' "$consumer_ok" >&2
  exit 1
}
grep -Fq 'NOTE configured exit-node exit-node-id is an intentional consumer dependency (single-node egress SPOF)' <<<"$consumer_ok" || {
  printf 'FAIL: consumer path hid the intentional single-node egress dependency:\n%s\n' "$consumer_ok" >&2
  exit 1
}
! grep -Fq 'FAIL ' <<<"$consumer_ok" || {
  printf 'FAIL: healthy consumer policy produced a failure:\n%s\n' "$consumer_ok" >&2
  exit 1
}
assert_case "consumer still fails when the LAN-prefix FIB is swallowed" \
  "$tmp/consumer.card" tailscale0 exit-node-id swallowed \
  "FAIL exit-node LAN-prefix FIB exclusion is swallowed"
assert_case "consumer fails when configured exit-node is not carrying public egress" \
  "$tmp/consumer.card" enp42s0 exit-node-id ok \
  "FAIL consumer policy configures exit-node exit-node-id but public FIB uses enp42s0"
assert_case "producer keeps clean-control-plane pass on LAN" \
  "$tmp/provider.card" enp42s0 '' ok \
  "PASS producer control-plane egress dev=enp42s0 (LAN)"
assert_case "producer keeps clean-control-plane failure on overlay" \
  "$tmp/provider.card" tailscale0 '' ok \
  "FAIL producer control-plane egress rides tailscale0"
assert_case "producer cannot itself consume a configured exit-node" \
  "$tmp/provider.card" enp42s0 exit-node-id ok \
  "FAIL producer policy has configured ExitNodeID exit-node-id"
assert_case "unknown policy cannot silently exempt a configured overlay" \
  "$tmp/missing.card" tailscale0 exit-node-id ok \
  "FAIL ExitNodeID exit-node-id is configured but declared connectivity policy is unknown"
assert_case "direct node keeps the no-exit-node verdict" \
  "$tmp/direct.card" enp42s0 '' ok \
  "PASS no exit-node configured"

echo "PASS: mesh-doctor egress policy regressions"
