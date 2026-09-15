#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-route-failures"
td="$(mktemp -d)"
trap 'rm -rf "$td"' EXIT

cat >"$td/snmp" <<'EOF'
Ip: Forwarding DefaultTTL InReceives InHdrErrors InAddrErrors ForwDatagrams InUnknownProtos InDiscards InDelivers OutRequests OutDiscards OutNoRoutes ReasmTimeout ReasmReqds ReasmOKs ReasmFails FragOKs FragFails FragCreates
Ip: 2 64 100 0 0 0 0 0 100 80 0 7 0 0 0 0 0 0 0
EOF
cat >"$td/snmp6" <<'EOF'
Ip6InReceives                    20
Ip6OutNoRoutes                   11
EOF

out="$(MESH_SNMP_FILE="$td/snmp" MESH_SNMP6_FILE="$td/snmp6" "$tool")"
grep -q 'ROUTE-FAILURES' <<<"$out"
grep -q 'ipv4=7' <<<"$out"
grep -q 'ipv6=11' <<<"$out"

if MESH_SNMP_FILE="$td/missing" MESH_SNMP6_FILE="$td/missing6" "$tool" >/dev/null 2>&1; then
  echo "missing proc inputs must exit 2" >&2
  exit 1
else
  rc=$?
  [ "$rc" -eq 2 ]
fi

echo "test-mesh-route-failures: ok"
