#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$(readlink -f "$0")")/.." || exit 1
exec scripts/mesh-doctrine-lint --test
