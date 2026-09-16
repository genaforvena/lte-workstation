#!/usr/bin/env bash
set -uo pipefail
exec "$(dirname "$0")/../scripts/mesh-claim-freshness" --test
