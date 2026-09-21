#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
bash -n "$ROOT/scripts/mesh-dash"
grep -q 'netstats-delta.state.txt' "$ROOT/scripts/mesh-dash"
grep -q 'netstats .*_n3nettxt' "$ROOT/scripts/mesh-dash"
printf 'ok: mesh-dash Note3 netstats row\n'
