#!/usr/bin/env bash
# build.sh — compile the vendored Uxn toolchain (uxnasm + uxncli) for THIS platform.
# The emulator is per-platform (26KB C); the ROM it runs is portable and byte-identical
# everywhere. Run this once per node (x86 workstation, aarch64 Note3/Termux, …).
#   ./build.sh          → bin/uxnasm, bin/uxncli
#   ./build.sh --rom    → also re-assemble lease-gate.tal → lease-gate.rom
set -eu
cd "$(dirname "$0")"
CC="${CC:-cc}"
mkdir -p bin
$CC -std=c89 -O2 -DNDEBUG -o bin/uxnasm src/uxnasm.c
$CC -std=c89 -O2 -DNDEBUG -o bin/uxncli \
    src/uxncli.c src/uxn.c src/devices/system.c src/devices/file.c src/devices/datetime.c
echo "built bin/uxnasm ($(wc -c <bin/uxnasm)b) bin/uxncli ($(wc -c <bin/uxncli)b)"
if [ "${1:-}" = --rom ]; then
  ./bin/uxnasm lease-gate.tal lease-gate.rom
fi
