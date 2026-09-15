#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-nic-multicast"
test -x "$tool"

out="$("$tool" --test)"
grep -q 'REAL .*rx_nohandler' <<<"$out"

echo 'test-mesh-nic-multicast: PASS (source --test exercised fixture and live rx_nohandler read)'
