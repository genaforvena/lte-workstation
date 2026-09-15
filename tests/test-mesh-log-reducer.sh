#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
td=$(mktemp -d)
trap 'rm -rf "$td"' EXIT
input=$td/input
mkdir -p "$input"

make_receipt() {
  "$repo/scripts/mesh-observation-handle" --store "$input" --retain 20 --page-bytes 5 \
    --label reducer-fixture -- sh -c 'printf alpha; printf beta >&2' >/dev/null
}
make_receipt
receipt=$(find "$input" -maxdepth 1 -name '*.json' -print -quit)

"$repo/scripts/mesh-log-reducer" --input "$input" --output "$td/reduced.json" \
  --max-receipt-bytes 65536 --max-pages 100 --max-stream-bytes 65536
python3 - "$td/reduced.json" "$receipt" <<'PY'
import hashlib, json, pathlib, sys
out = json.loads(pathlib.Path(sys.argv[1]).read_text())
source = json.loads(pathlib.Path(sys.argv[2]).read_text())
assert out["summary"] == {"accepted": 1, "rejected": 0, "handles": 1}
record = out["records"][0]
assert record["handle"] == source["handle"]
assert record["status"] == "ok"
assert record["source"]["receipt"] == pathlib.Path(sys.argv[2]).name
assert record["source"]["receipt_sha256"] == hashlib.sha256(pathlib.Path(sys.argv[2]).read_bytes()).hexdigest()
assert record["source"]["streams"]["stdout"] == source["streams"]["stdout"]["sha256"]
PY

# Replay the same receipt twice: the canonical output must be byte-identical.
cp "$td/reduced.json" "$td/first.json"
"$repo/scripts/mesh-log-reducer" --input "$receipt" --input "$receipt" --output "$td/replayed.json"
cmp "$td/first.json" "$td/replayed.json"

# Mutation of source evidence must fail closed and leave no accepted record.
stream=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["streams"]["stdout"]["path"])' "$receipt")
cp "$input/$stream" "$td/original.stream"
printf 'ALPHA' > "$input/$stream"
set +e
"$repo/scripts/mesh-log-reducer" --input "$receipt" --output "$td/mutated.json"
rc=$?
set -e
test "$rc" -eq 2
python3 - "$td/mutated.json" <<'PY'
import json, pathlib, sys
out = json.loads(pathlib.Path(sys.argv[1]).read_text())
assert out["summary"] == {"accepted": 0, "rejected": 1, "handles": 0}
assert out["rejections"][0]["reason"] == "stream-hash-mismatch"
PY
mv "$td/original.stream" "$input/$stream"

# Truncated/malformed receipts are represented as rejections, bounded by the parser.
printf '{"handle":"truncated"' > "$td/truncated.json"
set +e
"$repo/scripts/mesh-log-reducer" --input "$td/truncated.json" --output "$td/truncated-out.json"
rc=$?
set -e
test "$rc" -eq 2
python3 - "$td/truncated-out.json" <<'PY'
import json, pathlib, sys
out = json.loads(pathlib.Path(sys.argv[1]).read_text())
assert out["summary"]["rejected"] == 1
assert out["rejections"][0]["reason"] == "malformed-json"
PY

python3 - "$td/oversized.json" <<'PY'
import pathlib, sys
pathlib.Path(sys.argv[1]).write_bytes(b"{" + b"x" * 100 + b"\n")
PY
set +e
"$repo/scripts/mesh-log-reducer" --input "$td/oversized.json" --output "$td/oversized-out.json" --max-receipt-bytes 32
rc=$?
set -e
test "$rc" -eq 2
python3 - "$td/oversized-out.json" <<'PY'
import json, pathlib, sys
out = json.loads(pathlib.Path(sys.argv[1]).read_text())
assert out["rejections"][0]["reason"] == "receipt-too-large"
PY

echo 'test-mesh-log-reducer: PASS (bounded parse, replay/idempotence, mutation, malformed input, source traceability)'
