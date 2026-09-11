#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT

file=$td/sample.txt
printf 'before\n' >"$file"
set +e
"$repo/scripts/mesh-edit-validate" --file "$file" \
  --replace before after --receipt "$td/pass.json" \
  --validator sh -- -c 'test "$(cat "$1")" = after' sh '{file}'
rc=$?
set -e
test "$rc" -eq 0
test "$(cat "$file")" = after
python3 - "$td/pass.json" "$file" <<'PY'
import hashlib, json, pathlib, sys
r = json.loads(pathlib.Path(sys.argv[1]).read_text())
f = pathlib.Path(sys.argv[2])
assert r["status"] == "validated"
assert r["validator"]["rc"] == 0
assert r["edit"]["replacements"] == 1
assert r["edit"]["before_sha256"] == hashlib.sha256(b"before\n").hexdigest()
assert r["edit"]["after_sha256"] == hashlib.sha256(f.read_bytes()).hexdigest()
assert "-before" in r["edit"]["diff"] and "+after" in r["edit"]["diff"]
assert r["validator"]["command"][-1] == str(f)
PY

printf 'before\n' >"$file"
set +e
"$repo/scripts/mesh-edit-validate" --file "$file" \
  --replace before broken --receipt "$td/fail.json" \
  --validator sh -- -c 'test "$(cat "$1")" = expected' sh '{file}'
rc=$?
set -e
test "$rc" -eq 1
test "$(cat "$file")" = broken
python3 - "$td/fail.json" "$file" <<'PY'
import json, pathlib, sys
r = json.loads(pathlib.Path(sys.argv[1]).read_text())
assert r["status"] == "validation-failed"
assert r["success"] is False
assert r["validator"]["rc"] != 0
assert r["recovery"]["action"] == "mesh-edit-validate --recover"
assert r["recovery"]["file"] == sys.argv[2]
assert "broken" in r["edit"]["diff"]
PY

"$repo/scripts/mesh-edit-validate" --recover "$td/fail.json"
test "$(cat "$file")" = before
python3 - "$td/fail.json" <<'PY'
import json, pathlib, sys
r = json.loads(pathlib.Path(sys.argv[1]).read_text())
assert r["recovery"]["status"] == "restored"
assert r["recovery"]["restored_sha256"] == r["edit"]["before_sha256"]
PY

echo 'test-mesh-edit-validate: PASS (exact edit, validator pass, forced failure receipt, recovery)'
