#!/bin/sh
# cross-build.sh — a static uxncli for a body that has no compiler.
#
# The mesh's distribution model is CROSS-BUILD HERE + PUSH THE BINARY (build.sh's header):
# measured 2026-07-24, mesh-home is the only node with a host compiler at all. This script
# is the single copy of that compile line; the translation units live in `emu-sources`,
# shared with build.sh, so a device added to the emulator reaches every platform at once.
#
#   ./cross-build.sh arm64 [out]   aarch64-linux-gnu-gcc    — Android 8+ bodies (Redmi 10, …)
#   ./cross-build.sh armhf [out]   arm-linux-gnueabihf-gcc  — armeabi-v7a (Note3, 2013)
#   --check                        after building, RUN the binary and assert it WORKS
#   CROSS=<gcc>                    override the compiler
#   default out: bin/uxncli.<arch> (bin/ is gitignored — the ROM is the portable artifact,
#                                   the emulator is per-platform and rebuilt, never committed)
#
# STATIC, always. Android's bionic has no glibc loader, so a dynamic cross-build cannot even
# start there; static is pure-syscall and runs under the Android kernel directly.
#
# KNOWN LIMIT inherited from static glibc, measured on-device (verify-note3.sh): NO HOSTNAME
# RESOLUTION under bionic — getaddrinfo needs NSS shared libraries that are not there. It
# fails loud and distinguishably ("Temporary failure in name resolution" vs "Connection
# refused"), so it is a limit and not a trap: address ROMs on these bodies by NUMERIC IP.
#
# WHY --check EXISTS: `file` says aarch64 and `-x` says executable, and neither is the claim.
# Executable and loadable are different claims (whisper.cpp, 974d864) — and a build that
# links fine can still be net-BLIND, which is the silent one: emu_dei falls through to 0,
# net state 0 is Disconnected, and the ROM answers `NA` rc=2 byte-identically to a real
# refusal. So --check drives the produced binary through three claims that a wrong build
# cannot fake: it COMPUTES (the lease-gate truth table, same four rows as on the host), it
# IDENTIFIES the net device (action d0, a write bare memory cannot forge), and it ACCEPTS a
# real inbound connection. Under qemu-user when the host is not this arch.
#
# What --check does NOT claim: the round trip is over LOOPBACK, so it asserts the MECHANISM
# (bind/accept/read/write in this libc) and says nothing about addressing or the tailnet —
# same labelling as test-net-device's local leg. The addressing claim belongs to the
# on-device script (verify-note3.sh step 5), where a real phone answers a real dial.
# No qemu and not this arch → exit 2, honest n/a. Never a pass by absence.
set -eu
cd "$(dirname "$0")"
. ./emu-sources

arch=""; out=""; check=0
while [ $# -gt 0 ]; do
  case "$1" in
    --check) check=1 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    --*) echo "cross-build: unknown flag: $1" >&2; exit 2 ;;
    *) if [ -z "$arch" ]; then arch="$1"
       elif [ -z "$out" ]; then out="$1"
       else echo "cross-build: too many arguments" >&2; exit 2; fi ;;
  esac
  shift
done
[ -n "$arch" ] || { echo "usage: cross-build.sh arm64|armhf [out] [--check]" >&2; exit 2; }

case "$arch" in
  arm64|aarch64)
    arch=arm64; TRIPLE=aarch64-linux-gnu; QEMU=qemu-aarch64-static; NATIVE=aarch64
    PKG=gcc-aarch64-linux-gnu ;;
  armhf|armv7|armeabi-v7a)
    arch=armhf; TRIPLE=arm-linux-gnueabihf; QEMU=qemu-arm-static;   NATIVE=armv7l
    PKG=gcc-arm-linux-gnueabihf ;;
  *) echo "cross-build: unknown arch '$arch' (want arm64|armhf)" >&2; exit 2 ;;
esac

CC="${CROSS:-${TRIPLE}-gcc}"
command -v "$CC" >/dev/null 2>&1 || {
  echo "cross-build: need $CC — apt install $PKG" >&2; exit 2; }

out="${out:-bin/uxncli.$arch}"
mkdir -p "$(dirname "$out")"
# shellcheck disable=SC2086  # EMU_SRC is a deliberate word list
$CC -std=c89 -O2 -static -DNDEBUG -o "$out" $EMU_SRC
echo "cross-built $out ($(wc -c <"$out")b, $(file -b "$out" | cut -d, -f1-2))"

[ "$check" = 1 ] || exit 0

# --- the produced binary is now driven, not described ------------------------------------
RUN=""
if [ "$(uname -m)" = "$NATIVE" ]; then
  RUN=""                       # the host IS this arch; run it directly
elif command -v "$QEMU" >/dev/null 2>&1; then
  RUN="$QEMU"
else
  echo "check: n/a — host is $(uname -m), not $NATIVE, and no $QEMU (apt install qemu-user-static)"
  echo "check: the binary was BUILT but has NOT been run; that is not a pass"
  exit 2
fi

rc=0
port=$(( 47420 + $$ % 60 ))
tok="$(head -c 6 /dev/urandom | od -An -tx1 | tr -d ' \n')"

# 1) it COMPUTES — the same four rows the host gives, from the byte-identical ROM.
for t in "900 1800 OK" "900 900 RED" "900 1799 RED" "1800 3600 OK"; do
  set -- $t
  got="$($RUN "./$out" lease-gate.rom "$1" "$2" 2>/dev/null || true)"
  if [ "$got" = "$3" ]; then echo "$arch   cad=$1 lease=$2 -> $got  (ok)"
  else echo "$arch   cad=$1 lease=$2 -> ${got:-<empty>}  (WANT $3)"; rc=1; fi
done

# 2) it carries the NET DEVICE, at the step net-listen.rom demands (>= 2). Driven against
#    203.0.113.1 (RFC5737 TEST-NET-3): not an address on this host, so bind(2) answers
#    EADDRNOTAVAIL by design and no far node is involved. Asserting the verdict alone would
#    assert nothing — a net-blind build says `NA` too — so the three outcomes are read apart.
netout="$($RUN "./$out" net-listen.rom "tcp:203.0.113.1:$port" 2>&1 || true)"
case "$netout" in
  *NODEV*unknown\ action*|*unknown\ action*NODEV*)
    echo "$arch   net device TOO OLD — answered the identify probe with 'unknown action' (pre-step-2)"; rc=1 ;;
  *NODEV*)
    echo "$arch   net device MISSING — no 0xd0 device in this build (got: $(printf '%.60s' "$netout"))"; rc=1 ;;
  *NA*)
    if printf '%s' "$netout" | grep -qi 'assign'; then
      echo "$arch   net device present at step >= 2: yes (bind refused loudly: $(printf '%s' "$netout" | grep -o 'net:.*' | head -1))"
    else
      echo "$arch   net device answered NA without naming a cause — refusal path is silent (got: $(printf '%.80s' "$netout"))"; rc=1
    fi ;;
  *) echo "$arch   unexpected identify outcome (got: $(printf '%.80s' "$netout"))"; rc=1 ;;
esac

# 3) it ACCEPTS — presence is not capability, and bind/accept is where a statically linked
#    libc could plausibly differ from the host's. The cross binary LISTENS; the known-good
#    host uxncli dials it with net-echo.rom. MECHANISM ONLY (loopback — see the header).
#    The payload carries a per-run token, so a pass cannot come from a constant baked
#    anywhere, and the reply must carry net-listen's `uxn:` tag: a stray listener or a
#    client reading back its own buffer both produce the payload, only the ROM tags it.
if [ ! -x bin/uxncli ]; then
  echo "$arch   accept round trip: n/a — no host bin/uxncli to dial with (run ./build.sh)"
else
  UXN_NET_TIMEOUT=12 $RUN "./$out" net-listen.rom "tcp:127.0.0.1:$port" >/tmp/uxn-xbuild-listen.$$ 2>&1 &
  lpid=$!
  sleep 2
  reply="$(printf 'tcp:127.0.0.1:%s\nping-%s\n' "$port" "$tok" \
           | UXN_NET_TIMEOUT=8 ./bin/uxncli net-echo.rom 2>/dev/null || true)"
  wait "$lpid" 2>/dev/null || true
  if [ "$reply" = "uxn:ping-$tok" ]; then
    echo "$arch   accept round trip: the $arch build BOUND :$port and answered '$reply' (mechanism only, loopback)"
  else
    echo "$arch   accept round trip FAILED: want 'uxn:ping-$tok', got '${reply:-<empty>}' (listener said: $(tr '\n' ' ' </tmp/uxn-xbuild-listen.$$ | cut -c1-120))"; rc=1
  fi
  rm -f /tmp/uxn-xbuild-listen.$$
fi

if [ "$rc" = 0 ]; then
  echo "cross-build $arch: ok — it computes the host's truth table, carries the net device at step >= 2, and accepted a real connection"
else
  echo "cross-build $arch: FAIL"
fi
exit "$rc"
