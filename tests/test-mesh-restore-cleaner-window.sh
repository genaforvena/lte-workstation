#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
restore="$root/scripts/mesh-restore"

grep -qE '^ensure_uniform_channel cleaner cleaner ' "$restore" \
  || { echo 'FAIL: mesh-restore uniform manifest does not plant the cleaner window' >&2; exit 1; }

echo 'mesh-restore cleaner window: manifest wiring present'
