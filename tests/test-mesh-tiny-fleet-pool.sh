#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
pool="$root/scripts/mesh-tiny-fleet-pool"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

out="$($pool --test)"
printf '%s\n' "$out" | grep -Fq 'adapter inventory: 2/2'
printf '%s\n' "$out" | grep -Fq 'abstain/escalate contract: 3/3'

set +e
abstain="$($pool --prompt 'What is the capital of France?' 2>&1)"
rc=$?
set -e
[ "$rc" -eq 3 ]
printf '%s\n' "$abstain" | grep -Fq '[ABSTAIN]'
printf '%s\n' "$abstain" | grep -Fq 'escalate'

set +e
relay_abstain="$("$root/scripts/mesh-relay" --pool tiny-fleet 'What is the capital of France?' 2>&1)"
rc=$?
set -e
[ "$rc" -eq 3 ]
printf '%s\n' "$relay_abstain" | grep -Fq '[ABSTAIN]'

set +e
miss="$(MESH_TINY_FLEET_DIR="$tmp/absent" "$root/scripts/mesh-relay" --pool tiny-fleet 'Give me a beginner guitar chord progression.' 2>&1)"
rc=$?
set -e
[ "$rc" -eq 1 ]
printf '%s\n' "$miss" | grep -Fq 'tiny-fleet failed'

echo "tiny-fleet pool tests: OK (verified adapters, guarded abstain/escalate)"
