#!/usr/bin/env bash
# cc-rom.sh — C source → uxn ROM via the vendored chibicc (uxn-chibicc-vendor, spec 2026-07-23 §4).
#
#   host cc -P -E  (chibicc has no preprocessor)  →  chibicc -O1  →  uxnasm  →  <out.rom>
#
# usage: cc-rom.sh <src.c> <out.rom>
# Include path: chibicc/ (varvara.h, uxn.h) + chibicc/lib (ctype.h, string.h). Builds the
# toolchain pieces it is missing (one-time, host cc only). The emitted ROM is portable and
# byte-identical across nodes; only this build step is per-platform.
set -euo pipefail
src="${1:?usage: cc-rom.sh <src.c> <out.rom>}"
out="${2:?usage: cc-rom.sh <src.c> <out.rom>}"
src="$(realpath "$src")"; out_dir="$(cd "$(dirname "$out")" && pwd)"; out="$out_dir/$(basename "$out")"
cd "$(dirname "$0")"
[ -x bin/chibicc ] || ./build.sh --chibicc >/dev/null
[ -x bin/uxnasm ]  || ./build.sh >/dev/null
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
"${HOSTCC:-cc}" -I chibicc -I chibicc/lib -P -E -x c "$src" -o "$tmp/pp.c"
./bin/chibicc -O1 "$tmp/pp.c" > "$tmp/rom.tal"
./bin/uxnasm "$tmp/rom.tal" "$out" 2>/dev/null
echo "cc-rom: $src → $out ($(wc -c <"$out")b)"
