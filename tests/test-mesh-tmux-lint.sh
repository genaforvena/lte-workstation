#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/mesh-tmux-lint" --test
echo 'tmux-lint: ok'
