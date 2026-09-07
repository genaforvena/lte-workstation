#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
export TINY_FLEET_DIR="$tmp/fleet"
export TINY_FLEET_PROTOCOL="$root/docs/tiny-fleet-protocol.md"

"$root/scripts/mesh-tiny-fleet" --test >"$tmp/test.out"
"$root/scripts/mesh-tiny-fleet" preflight >"$tmp/preflight.out"
artifact=$(find "$TINY_FLEET_DIR/preflight" -type f -name '*.json' -print -quit)
[ -s "$artifact" ]
python3 - "$artifact" <<'PY'
import json, sys
d=json.load(open(sys.argv[1]))
assert d['schema'] == 'tiny-fleet-preflight/v1'
assert d['protocol']['sha256']
assert d['arms']['lora_qlora']['status'] in {'ready', 'blocked'}
assert d['arms']['live_mesh_scheduler_routing']['status'] == 'not_in_scope'
if d['arms']['lora_qlora']['status'] == 'blocked':
    assert 'no proxy' in d['arms']['lora_qlora']['reason']
PY
# Mutation gate: a missing protocol must be visible and never produce a green hash.
bad="$tmp/missing-protocol.md"
export TINY_FLEET_PROTOCOL="$bad"
"$root/scripts/mesh-tiny-fleet" preflight >/dev/null
artifact=$(find "$TINY_FLEET_DIR/preflight" -type f -name '*.json' | sort | tail -1)
python3 - "$artifact" <<'PY'
import json, sys
d=json.load(open(sys.argv[1])); assert d['protocol']['sha256'] is None
PY
echo "tiny-fleet validation tests: OK (offline smoke, durable preflight, blocked LoRA, protocol mutation)"

# Frozen candidate manifest and deterministic fixture extraction are offline-only.
export TINY_FLEET_CANDIDATES="$root/docs/tiny-fleet-artifacts/corpus-candidates.tsv"
manifest="$TINY_FLEET_DIR/corpus-manifest.json"
"$root/scripts/mesh-tiny-fleet" corpus-manifest >"$tmp/corpus.out"
[ -s "$manifest" ]
python3 - "$manifest" "$root" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
assert d['schema'] == 'tiny-fleet-corpus-manifest/v1'
assert d['collection']['network'] == 'disabled'
assert d['candidates'], 'frozen candidate manifest is empty'
assert any(row['status'] == 'resolved-local' for row in d['candidates'])
assert all(row['snapshot']['commit'] for row in d['candidates'] if row['status'] == 'resolved-local')
PY

fixture_manifest="$TINY_FLEET_DIR/fixtures/manifest.tsv"
"$root/scripts/mesh-tiny-fleet" fixture-build >"$tmp/fixture.out"
[ -s "$fixture_manifest" ]
python3 - "$fixture_manifest" "$TINY_FLEET_DIR/fixtures" <<'PY'
import csv, hashlib, pathlib, sys
manifest, root = sys.argv[1:]
rows = list(csv.DictReader(open(manifest), delimiter='\t'))
assert rows
for row in rows:
    if row['status'] == 'excluded':
        continue
    p = pathlib.Path(root, row['fixture_path'])
    assert p.is_file()
    assert hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256']
    assert row['license_provenance'] == 'fixture-test-input; no redistribution claim'
assert any(row['case'] == 'generated-file' and row['status'] == 'excluded' for row in rows)
assert any(row['case'] == 'duplicate-blob' for row in rows)
assert any(row['case'] == 'empty-file' for row in rows)
PY
echo "tiny-fleet corpus fixtures: OK (frozen candidates, immutable hashes, exclusion case)"

# Corpus lock is clean-room reproducible and fails closed on a mutable source ref.
export TINY_FLEET_PROTOCOL="$root/docs/tiny-fleet-protocol.md"
lock_a="$tmp/lock-a"; lock_b="$tmp/lock-b"
TINY_FLEET_DIR="$lock_a" "$root/scripts/mesh-tiny-fleet" corpus-lock >/dev/null
TINY_FLEET_DIR="$lock_b" "$root/scripts/mesh-tiny-fleet" corpus-lock >/dev/null
cmp "$lock_a/corpus.lock.json" "$lock_b/corpus.lock.json"
cmp "$lock_a/source-manifest.tsv" "$lock_b/source-manifest.tsv"
cmp "$lock_a/fixture-report.json" "$lock_b/fixture-report.json"
python3 - "$lock_a/corpus.lock.json" "$lock_a/fixture-report.json" <<'PY'
import json, sys
lock, report = (json.load(open(p)) for p in sys.argv[1:])
assert lock['schema'] == 'tiny-fleet-corpus-lock/v1'
assert len(lock['sources']) >= 2
assert all(len(x['commit']) == 40 for x in lock['sources'])
assert report['controls']['exact_copy_groups']
assert report['controls']['adversarial_count'] >= 2
PY
bad_candidates="$tmp/bad-candidates.tsv"
cp "$root/docs/tiny-fleet-artifacts/corpus-candidates.tsv" "$bad_candidates"
sed -i '0,/e8f47364e5a0f224c1bd03331df592272a187df5/s//HEAD/' "$bad_candidates"
if TINY_FLEET_DIR="$tmp/bad-lock" TINY_FLEET_CANDIDATES="$bad_candidates" "$root/scripts/mesh-tiny-fleet" corpus-lock >/dev/null 2>&1; then
  echo 'corpus lock unexpectedly accepted mutable HEAD' >&2
  exit 1
fi
echo "tiny-fleet corpus lock: OK (repeatable lock, provenance/license evidence, leakage/adversarial report, mutable-ref red gate)"
