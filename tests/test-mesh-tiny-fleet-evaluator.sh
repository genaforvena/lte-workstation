#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/a/src" "$tmp/b/src" "$tmp/b/generated"
printf '#!/bin/sh\necho old\n' >"$tmp/a/src/tool.sh"
cp "$tmp/a/src/tool.sh" "$tmp/b/src/tool.sh"
printf 'new architectural marker\n' >"$tmp/b/src/new.md"
printf 'generated noise\n' >"$tmp/b/generated/noise.py"

out="$tmp/result.json"
mutation_sha=$(sha256sum "$tmp/b/src/new.md" | awk '{print $1}')
"$root/scripts/mesh-tiny-fleet-evaluate" \
  --snapshot-a "$tmp/a" --snapshot-b "$tmp/b" \
  --commit-a 1111111 --commit-b 2222222 --mutation-file src/new.md \
  --mutation-sha256 "$mutation_sha" --output "$out" \
  --raw-manifest "$tmp/raw.json" --uncertainty-output "$tmp/uncertainty.json" \
  --controls-output "$tmp/controls.json"

python3 - "$out" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
assert d['schema'] == 'tiny-fleet-evaluator/v1'
assert d['provenance']['snapshot_a']['commit'] == '1111111'
assert d['provenance']['snapshot_b']['commit'] == '2222222'
assert d['metrics']['structural']['file_count']['delta'] == 1
assert d['metrics']['structural']['b']['excluded_generated'] == 1
assert d['controls']['same_snapshot_repeatability']['status'] == 'pass'
assert d['controls']['mutation']['status'] == 'pass'
assert d['controls']['leakage']['status'] == 'pass'
assert d['controls']['path_order_permutation']['status'] == 'pass'
assert d['controls']['swapped_labels']['status'] == 'pass'
assert d['controls']['shuffled_conditioning']['status'] == 'not_run'
assert d['measurement_schema'] == 'tiny-fleet-evaluator/v2'
assert d['metrics']['lexical']['js_divergence'] >= 0
assert d['uncertainty']['byte_delta']['n'] > 0
assert d['arms']['lora_qlora']['status'] == 'blocked'
PY
[ -s "$tmp/raw.json" ] && [ -s "$tmp/uncertainty.json" ] && [ -s "$tmp/controls.json" ]
python3 - "$tmp/raw.json" "$tmp/uncertainty.json" "$tmp/controls.json" <<'PY'
import json, sys
raw, uncertainty, controls = (json.load(open(p)) for p in sys.argv[1:])
assert raw['schema'] == 'tiny-fleet-raw-manifest/v1'
assert raw['a'] and raw['b']
assert uncertainty['byte_delta']['method'] == 'cluster-bootstrap'
assert controls['path_order_permutation']['status'] == 'pass'
PY

# Mutation gate: changing the added file must make the structural mutation control fail.
printf 'new architectural marker\nchanged\n' >"$tmp/b/src/new.md"
if "$root/scripts/mesh-tiny-fleet-evaluate" \
    --snapshot-a "$tmp/a" --snapshot-b "$tmp/b" \
    --commit-a 1111111 --commit-b 2222222 --mutation-file src/new.md \
    --mutation-sha256 "$mutation_sha" --output "$tmp/mutated.json"; then
  echo 'mutation control unexpectedly passed' >&2
  exit 1
fi
python3 - "$tmp/mutated.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
assert d['controls']['mutation']['status'] == 'fail'
PY

echo 'tiny-fleet evaluator: PASS (deterministic metrics, provenance, controls, blocked LoRA, mutation red gate)'
