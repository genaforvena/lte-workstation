#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
bash -n "$ROOT/scripts/mesh-dash"
grep -q 'note3-netpolicy.state' "$ROOT/scripts/mesh-dash"
grep -q 'netpolicy .*_n3policytxt' "$ROOT/scripts/mesh-dash"
printf '%s\n' 'PASS: mesh-dash Note3 netpolicy mobile-link row'
