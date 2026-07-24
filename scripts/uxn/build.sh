#!/usr/bin/env bash
# build.sh — compile the vendored Uxn toolchain (uxnasm + uxncli) for THIS platform.
# The emulator is per-platform (~56KB with the net device); the ROM it runs is portable and
# byte-identical everywhere.
#
# THIS SCRIPT NEEDS A HOST COMPILER, AND MOST MESH NODES DO NOT HAVE ONE. Measured
# 2026-07-24: the Note3 is armeabi-v7a with no cc/gcc/clang and no Termux; phaedra (x86_64)
# has no cc either. build.sh has only ever run on mesh-home. The distribution model for
# every other node is therefore CROSS-BUILD HERE + PUSH THE BINARY, not a per-node build —
# see verify-note3.sh, which cross-builds a static armhf uxncli and adb-pushes it. Do not
# re-state the old "run this once per node (aarch64 Note3/Termux)" claim; it was never true.
#   ./build.sh            → bin/uxnasm, bin/uxncli
#   ./build.sh --rom      → also re-assemble lease-gate.tal + band-gate.tal → .rom
#   ./build.sh --chibicc  → also build the vendored C→uxntal compiler → bin/chibicc (host cc only)
#
# Toolchain provenance (vendor-swapped 2026-07-23, modern post-2022 ISA — JCI/JMI/JSI):
#   https://git.sr.ht/~rabbits/uxn — uxnasm.c from archive/ (archived at 64e9f46);
#   uxncli + uxn core + devices from src/ at 43453d7 (last pre-archive emulator state;
#   the successor uxn11 needs X11, unusable headless). MIT, see src/LICENSE.
# chibicc provenance (vendored 2026-07-23, uxn-chibicc-vendor):
#   https://github.com/lynn/chibicc at ba7944d876b4645b5531d6d98ea93327aca283a8
#   ("codegen: Add -nostartfiles to drop the hardcoded prelude (#35)") — src/, lib/, routines/,
#   uxn.h, varvara.h, tests vendored into chibicc/; MIT, see chibicc/LICENSE. Truth-table gate:
#   ./test-chibicc (rebuilds lease-gate-c.rom from chibicc-eval/lease-gate.c, 5-row contract).
# The pre-2022-ISA toolchain this replaced lives in git history (chibicc-eval/EVAL.md).
set -eu
cd "$(dirname "$0")"
. ./emu-sources          # EMU_SRC — shared with cross-build.sh so the platforms cannot drift
CC="${CC:-cc}"
mkdir -p bin
$CC -std=c89 -O2 -DNDEBUG -o bin/uxnasm src/uxnasm.c
# shellcheck disable=SC2086  # EMU_SRC is a deliberate word list
$CC -std=c89 -O2 -DNDEBUG -o bin/uxncli $EMU_SRC
echo "built bin/uxnasm ($(wc -c <bin/uxnasm)b) bin/uxncli ($(wc -c <bin/uxncli)b)"
if [ "${1:-}" = --rom ]; then
  ./bin/uxnasm lease-gate.tal lease-gate.rom
  ./bin/uxnasm band-gate.tal band-gate.rom
  ./bin/uxnasm sense-gate.tal sense-gate.rom
  ./bin/uxnasm spearman.tal spearman.rom
  ./bin/uxnasm series-stats.tal series-stats.rom
  ./bin/uxnasm arith32-test.tal arith32-test.rom
  ./bin/uxnasm net-echo.tal net-echo.rom
  ./bin/uxnasm fletcher16.tal fletcher16.rom
  ./bin/uxnasm permcheck.tal permcheck.rom
  ./bin/uxnasm net-listen.tal net-listen.rom
  ./bin/uxnasm hop-dial.tal hop-dial.rom
  ./bin/uxnasm hop-serve.tal hop-serve.rom
  ./bin/uxnasm rot13-net.tal rot13-net.rom
fi
if [ "${1:-}" = --chibicc ]; then
  $CC -std=c11 -O2 -fno-common -o bin/chibicc chibicc/src/*.c
  echo "built bin/chibicc ($(wc -c <bin/chibicc)b)"
fi
