#!/usr/bin/env bash
set -euo pipefail

repo="$(cd -- "$(dirname -- "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/.mesh"

# The prune diagnostic keeps 60 visible characters. Put a multibyte glyph exactly at
# that boundary so a byte-counted cut leaves only its first byte in generate.log.
idea="$(printf '%059d' 0 | tr 0 a)я-suffix"
printf '[x] %s\n' "$idea" > "$tmp/.mesh/ideas-queue"
printf 'worker|TASK (auto from idea-queue): %s — do it. fixture\n' "$idea" > "$tmp/.mesh/backlog"

HOME="$tmp" MESH_BACKLOG_MIN=0 MESH_GEN_ASSUME_AVAIL=1 bash "$repo/scripts/mesh-generate" >/dev/null

python3 - "$tmp/.mesh/generate.log" <<'PY'
from pathlib import Path
import sys

log = Path(sys.argv[1]).read_text(encoding="utf-8", errors="strict")
expected_prefix = "a" * 59 + "я"
prune_rows = [line for line in log.splitlines() if " prune: " in line]
assert len(prune_rows) == 1, f"expected one prune diagnostic, got {prune_rows!r}"
assert f"prune: {expected_prefix} (idea [x])" in prune_rows[0], prune_rows[0]
PY

# Bash parameter slicing is byte-oriented under the C locale. Exercise the other
# generate.log preview with the same exact boundary, independent of host locale.
gen_home="$tmp/generated"
mkdir -p "$gen_home/.mesh"
printf '[ ] %s\n' "$idea" > "$gen_home/.mesh/ideas-queue"
: > "$gen_home/.mesh/backlog"
LC_ALL=C HOME="$gen_home" MESH_BACKLOG_MIN=1 MESH_GEN_ASSUME_AVAIL=1 bash "$repo/scripts/mesh-generate" >/dev/null

python3 - "$gen_home/.mesh/generate.log" <<'PY'
from pathlib import Path
import sys

log = Path(sys.argv[1]).read_text(encoding="utf-8", errors="strict")
expected_prefix = "a" * 59 + "я"
generated_rows = [line for line in log.splitlines() if " generated -> " in line]
assert len(generated_rows) == 1, f"expected one generated diagnostic, got {generated_rows!r}"
assert f"generated -> local:genome: {expected_prefix}" in generated_rows[0], generated_rows[0]
PY

# The board writer had the sibling fault: a summary was cut at 240 bytes. With
# only system tools on PATH, mesh-handoff takes its raw-append fallback into a
# temporary chat.log, exercising the real UTF-8-safe summary code without the
# live board or any external delivery.
chat_home="$tmp/chat-home"
mkdir -p "$chat_home"
state="$(printf '%0239d' 0 | tr 0 a)я-tail"
env -i HOME="$chat_home" PATH=/usr/bin:/bin bash "$repo/scripts/mesh-handoff" genome "$state" >/dev/null

python3 - "$chat_home/.mesh/chat.log" <<'PY'
from pathlib import Path
import sys

log = Path(sys.argv[1]).read_text(encoding="utf-8", errors="strict")
expected_prefix = "a" * 239 + "я"
assert expected_prefix in log, "handoff summary did not preserve the complete boundary character"
PY

printf '%s\n' 'test-mesh-chat-generate-utf8-boundaries: PASS (multibyte chat and generate log previews remain valid UTF-8)'
