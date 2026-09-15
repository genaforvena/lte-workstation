#!/usr/bin/env bash
set -u
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
tool="$ROOT/scripts/mesh-link-duplex"
[ -x "$tool" ] || { echo "FAIL: tool is not executable"; exit 1; }
"$tool" --test
