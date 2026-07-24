#!/usr/bin/env bash
# build.sh — build the uxn-packet-gate unit: the rule ROM + the NFQUEUE harness.
#
#   ./build.sh            build packet-gate.rom (via the sibling chibicc) AND the nfq-gate binary
#   ./build.sh --rom      build only packet-gate.rom
#   ./build.sh --bin      build only the nfq-gate binary
#
# The ROM is byte-identical across platforms; only this build step is per-arch. NFQUEUE support is
# compiled in when libnetfilter_queue is present (WITH_NFQUEUE); without it the binary still runs
# --one and --pps (the ROM decision path), so a node lacking the lib is honestly degraded, not broken.
set -euo pipefail
cd "$(dirname "$0")"
HERE="$(pwd)"
CC="${CC:-cc}"

build_rom() {
	# The rule compiles through the vendored chibicc in the sibling uxn lane (cc-rom.sh). That
	# toolchain is itself sha256-pinned (../uxn/chibicc/VENDOR-MANIFEST); we vendor the RUNTIME
	# emulator (emu/, our VENDOR-MANIFEST), the sibling provides the build-time compiler.
	local ccrom=../uxn/cc-rom.sh
	[ -x "$ccrom" ] || { echo "build: no $ccrom (need the sibling uxn lane to compile the ROM)" >&2; return 2; }
	"$ccrom" packet-gate.c packet-gate.rom
}

build_bin() {
	local src="nfq-gate.c emu/uxn.c emu/devices/system.c emu/devices/console.c"
	local def="" lib=""
	if echo '#include <libnetfilter_queue/libnetfilter_queue.h>
int main(){return 0;}' | "$CC" -xc - -lnetfilter_queue -o /dev/null 2>/dev/null; then
		def="-DWITH_NFQUEUE"; lib="-lnetfilter_queue -lnfnetlink"
		echo "build: libnetfilter_queue present -> NFQUEUE mode compiled in"
	else
		echo "build: libnetfilter_queue ABSENT -> binary limited to --one/--pps (honest degrade)" >&2
	fi
	# shellcheck disable=SC2086
	"$CC" -O2 -Wall -Iemu $def $src $lib -o nfq-gate
	echo "build: nfq-gate ($(wc -c <nfq-gate)b)"
}

case "${1:-all}" in
	--rom) build_rom ;;
	--bin) build_bin ;;
	all)   build_rom; build_bin ;;
	*) echo "usage: $0 [--rom|--bin]" >&2; exit 2 ;;
esac
