#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="$ROOT/scripts/mesh-note3-step-listener"

fixture=$'SENSOR|Significant Motion|17|1|0|0|1001\nSENSOR|Step Detector|18|1|0|0|1002\nSENSOR|Step Counter|19|42|0|0|1003\nSENSOR|Magnetic Field|2|10.5|-2.0|40.0|1004'
out="$(MESH_NOTE3_STEP_RAW_OVERRIDE="$fixture" "$TOOL" --json)"

python3 - "$out" <<'PY'
import json, sys
rows = json.loads(sys.argv[1])
assert {row["type"] for row in rows} == {2, 17, 18, 19}, rows
assert rows[[row["type"] for row in rows].index(19)]["values"][0] == 42.0
assert rows[[row["type"] for row in rows].index(2)]["values"] == [10.5, -2.0, 40.0]
PY

echo "test-mesh-note3-step-listener: fixture PASS (types 2,17,18,19)"
