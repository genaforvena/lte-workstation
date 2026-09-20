#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
bash -n "$ROOT/scripts/mesh-dash"
grep -q 'note3-activitymanager.state' "$ROOT/scripts/mesh-dash"
grep -q 'foreground .*_n3foregroundtxt' "$ROOT/scripts/mesh-dash"
printf '%s\n' 'PASS: mesh-dash Note3 foreground mobile-link row'
