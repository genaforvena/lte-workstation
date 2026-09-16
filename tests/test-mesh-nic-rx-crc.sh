#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-nic-rx-crc"
test -x "$tool"
out="$("$tool" --test)"
grep -q 'REAL .*rx_crc_errors' <<<"$out"
echo 'test-mesh-nic-rx-crc: PASS (source --test exercised fixture and live rx_crc_errors read)'
