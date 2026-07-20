#!/usr/bin/env bash
# verify-note3.sh — prove the byte-identical lease-gate.rom runs on the Note3 (armeabi-v7a).
#
# The Note3 has no on-device compiler, so we cross-build a static armhf uxncli on the host,
# push it + the UNMODIFIED rom over adb, and run the same gate under su. The ROM is never
# rebuilt — only the ~26KB emulator is per-platform. Requires: adb (Note3 on USB), and
# arm-linux-gnueabihf-gcc on the host.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"; cd "$here"
CROSS="${CROSS:-arm-linux-gnueabihf-gcc}"
command -v "$CROSS" >/dev/null || { echo "need $CROSS (apt install gcc-arm-linux-gnueabihf)"; exit 2; }
adb get-state >/dev/null 2>&1 || { echo "no adb device"; exit 2; }

# 1) static armhf emulator (bionic has no glibc loader; static = pure-syscall, runs under the Android kernel)
"$CROSS" -std=c89 -O2 -static -DNDEBUG -o /tmp/uxncli.armhf \
    src/uxncli.c src/uxn.c src/devices/system.c src/devices/file.c src/devices/datetime.c
echo "cross-built /tmp/uxncli.armhf ($(wc -c </tmp/uxncli.armhf)b, $(file -b /tmp/uxncli.armhf | cut -d, -f1-2))"

# 2) push the emulator + the UNMODIFIED rom
D=/data/local/tmp
adb push /tmp/uxncli.armhf "$D/uxncli" >/dev/null
adb push lease-gate.rom    "$D/lease-gate.rom" >/dev/null
# prove byte-identity by pulling the on-device rom back and cmp'ing (Android shell has no sha1sum)
adb pull "$D/lease-gate.rom" /tmp/rom.fromnote3 >/dev/null 2>&1
if cmp -s lease-gate.rom /tmp/rom.fromnote3; then
  echo "rom byte-identical host<->note3: yes ($(wc -c <lease-gate.rom)b, sha1 $(sha1sum lease-gate.rom | awk '{print $1}'))"
else echo "rom DIFFERS host<->note3"; exit 1; fi

# 3) run the SAME rom on-device, same truth table as the host (uxncli logs 'Loaded' to stderr;
#    adb merges streams, so extract just the trailing verdict token)
run(){ adb shell "su -c 'cd $D && chmod 755 uxncli && ./uxncli lease-gate.rom $1 $2'" 2>/dev/null | grep -oE 'OK|RED' | tail -1; }
rc=0
for t in "900 1800 OK" "900 900 RED" "900 1799 RED" "1800 3600 OK"; do
  set -- $t; got="$(run "$1" "$2")"
  [ "$got" = "$3" ] && echo "note3  cad=$1 lease=$2 -> $got  (ok)" \
                    || { echo "note3  cad=$1 lease=$2 -> $got  (WANT $3)"; rc=1; }
done
[ "$rc" = 0 ] && echo "verify-note3: ok — identical ROM, matching verdicts on armeabi-v7a" || echo "verify-note3: FAIL"
exit $rc
