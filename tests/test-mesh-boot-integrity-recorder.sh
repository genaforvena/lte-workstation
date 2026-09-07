#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
RECORDER="$ROOT/scripts/mesh-boot-integrity-recorder"
TD=$(mktemp -d)
trap 'rm -rf "$TD"' EXIT

fake_tpm="$TD/fake-tpm2-pcrread"
cat >"$fake_tpm" <<'EOF'
#!/usr/bin/env bash
cat <<'PCR'
  sha256:
    0 : 0xF877AC537EEF3B5B131F7EDB7FC80C5AFBA3A5892D39D462392E171810BCF76B
    7 : 0x4F2FBE4E5AA58DBE0E2F83B30ACBF55E09B436A0FD69E6C67BF7A76126AF19CF
PCR
EOF
chmod +x "$fake_tpm"

HOME="$TD/home" \
MESH_BOOT_INTEGRITY_TPM_CMD="$fake_tpm" \
MESH_BOOT_INTEGRITY_OUTPUT="$TD/boot-integrity.jsonl" \
  "$RECORDER"

test -s "$TD/boot-integrity.jsonl"
row=$(tail -n 1 "$TD/boot-integrity.jsonl")
ROW="$row" python3 - <<'PY'
import json, os, re
row = json.loads(os.environ["ROW"])
assert row["schema"] == "mesh-boot-integrity/v1"
assert re.fullmatch(r"[0-9a-f-]{36}", row["boot_id"])
assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", row["ts"])
assert row["bank"] == "sha256"
assert set(row["pcr"]) == {"0", "7"}
assert all(re.fullmatch(r"[0-9A-Fa-f]{64}", row["pcr"][p]) for p in ("0", "7"))
PY

echo "test-mesh-boot-integrity-recorder: ok"
