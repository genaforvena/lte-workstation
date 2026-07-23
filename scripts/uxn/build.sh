#!/usr/bin/env bash
# build.sh — compile the vendored Uxn toolchain (uxnasm + uxncli) for THIS platform.
# The emulator is per-platform (~30KB C); the ROM it runs is portable and byte-identical
# everywhere. Run this once per node (x86 workstation, aarch64 Note3/Termux, …).
#   ./build.sh          → bin/uxnasm, bin/uxncli
#   ./build.sh --rom    → also re-assemble lease-gate.tal + band-gate.tal → .rom
#
# Toolchain provenance (vendor-swapped 2026-07-23, modern post-2022 ISA — JCI/JMI/JSI):
#   https://git.sr.ht/~rabbits/uxn — uxnasm.c from archive/ (archived at 64e9f46);
#   uxncli + uxn core + devices from src/ at 43453d7 (last pre-archive emulator state;
#   the successor uxn11 needs X11, unusable headless). MIT, see src/LICENSE.
# The pre-2022-ISA toolchain this replaced lives in git history (chibicc-eval/EVAL.md).
set -eu
cd "$(dirname "$0")"
CC="${CC:-cc}"
mkdir -p bin
$CC -std=c89 -O2 -DNDEBUG -o bin/uxnasm src/uxnasm.c
$CC -std=c89 -O2 -DNDEBUG -o bin/uxncli \
    src/uxncli.c src/uxn.c \
    src/devices/system.c src/devices/console.c src/devices/file.c src/devices/datetime.c
echo "built bin/uxnasm ($(wc -c <bin/uxnasm)b) bin/uxncli ($(wc -c <bin/uxncli)b)"
if [ "${1:-}" = --rom ]; then
  ./bin/uxnasm lease-gate.tal lease-gate.rom
  ./bin/uxnasm band-gate.tal band-gate.rom
fi
