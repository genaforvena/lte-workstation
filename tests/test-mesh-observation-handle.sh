#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT
store=$td/handles
mkdir -p "$store"

if "$repo/scripts/mesh-observation-handle" --store "$store" --retain 2 --page-bytes 7 \
    --label high-volume -- sh -c 'printf "stdout-0123456789"; printf "stderr-abcdefghij" >&2; exit 7' \
    >"$td/receipt.json"; then
  echo 'FAIL: command failure was reported as success' >&2
  exit 1
fi

python3 - "$td/receipt.json" "$store" <<'PY'
import hashlib, json, pathlib, sys
receipt = json.loads(pathlib.Path(sys.argv[1]).read_text())
store = pathlib.Path(sys.argv[2])
assert receipt["rc"] == 7
assert receipt["status"] == "command-failed"
assert receipt["truncation"]["stdout"] is False
assert receipt["overflow"]["stdout"] is False
assert receipt["streams"]["stdout"]["bytes"] == 17
assert receipt["streams"]["stderr"]["bytes"] == 17
for stream, expected in (("stdout", b"stdout-0123456789"), ("stderr", b"stderr-abcdefghij")):
    meta = receipt["streams"][stream]
    data = (store / meta["path"]).read_bytes()
    assert data == expected
    assert meta["sha256"] == hashlib.sha256(expected).hexdigest()
    pages = [p for p in receipt["pages"] if p["stream"] == stream]
    assert b"".join((store / p["path"]).read_bytes() for p in pages) == expected
    assert [p["start"] for p in pages] == list(range(0, len(expected), 7))
assert receipt["retention"]["keep"] == 2
assert receipt["retention"]["pruned"] == []
PY

for i in 1 2 3; do
  "$repo/scripts/mesh-observation-handle" --store "$store" --retain 2 --page-bytes 7 \
    --label retention -- sh -c "printf run$i" >/dev/null || true
done
test "$(find "$store" -maxdepth 1 -name '*.json' | wc -l)" -eq 2
test "$(find "$store" -maxdepth 1 -name '*.stdout' | wc -l)" -eq 2

set +e
"$repo/scripts/mesh-observation-handle" --store "$store" --timeout 0.05 -- \
  python3 -c 'import time; time.sleep(1)' >"$td/timeout.json"
rc=$?
set -e
test "$rc" -eq 124
python3 - "$td/timeout.json" <<'PY'
import json, pathlib, sys
r=json.loads(pathlib.Path(sys.argv[1]).read_text())
assert r["status"] == "timeout"
assert r["truncation"]["stdout"] is True
assert r["failure"] == "timeout"
PY

"$repo/scripts/mesh-observation-handle" --store "$store" --retain 2 --page-bytes 7 --max-bytes 3 \
  -- sh -c 'printf overflow' >"$td/overflow.json"
python3 - "$td/overflow.json" <<'PY'
import json, pathlib, sys
r=json.loads(pathlib.Path(sys.argv[1]).read_text())
assert r["status"] == "ok"
assert r["overflow"]["stdout"] is True
assert r["truncation"]["stdout"] is False
assert r["streams"]["stdout"]["bytes"] == 8
PY

echo 'test-mesh-observation-handle: PASS (identity, hashes, paging, retention, nonzero rc, timeout/truncation)'
