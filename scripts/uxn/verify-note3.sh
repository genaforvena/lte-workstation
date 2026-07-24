#!/usr/bin/env bash
# verify-note3.sh — prove the byte-identical lease-gate.rom runs on the Note3 (armeabi-v7a).
#
# The Note3 has no on-device compiler, so we cross-build a static armhf uxncli on the host,
# push it + the UNMODIFIED rom over adb, and run the same gate under su. The ROM is never
# rebuilt — only the emulator is per-platform. Requires: adb (Note3 on USB), and
# arm-linux-gnueabihf-gcc on the host. This IS the mesh's distribution model for every node
# without a compiler (which is all of them but mesh-home) — see build.sh's header.
#
# net.c IS IN THE CROSS-BUILD LINE, and step 4 asserts the pushed binary really carries the
# device. Omitting it produces a NET-BLIND emulator, and a net-blind emulator is not a loud
# failure: uxncli's emu_dei falls through to `return uxn.dev[addr]` = 0, and net state 0 is
# Disconnected — so a ROM on a device-less build answers `NA` rc=2, byte-identical on stdout
# to a genuine connection refused. Only the loud `net:` stderr line tells them apart, which
# is why step 4 greps for it rather than for a verdict.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"; cd "$here"
CROSS="${CROSS:-arm-linux-gnueabihf-gcc}"
command -v "$CROSS" >/dev/null || { echo "need $CROSS (apt install gcc-arm-linux-gnueabihf)"; exit 2; }
adb get-state >/dev/null 2>&1 || { echo "no adb device"; exit 2; }

# 1) static armhf emulator (bionic has no glibc loader; static = pure-syscall, runs under the Android kernel)
"$CROSS" -std=c89 -O2 -static -DNDEBUG -o /tmp/uxncli.armhf \
    src/uxncli.c src/uxn.c src/devices/system.c src/devices/console.c src/devices/file.c \
    src/devices/datetime.c src/devices/net.c
echo "cross-built /tmp/uxncli.armhf ($(wc -c </tmp/uxncli.armhf)b, $(file -b /tmp/uxncli.armhf | cut -d, -f1-2))"

# 2) push the emulator + the UNMODIFIED rom
D=/data/local/tmp
adb push /tmp/uxncli.armhf "$D/uxncli" >/dev/null
adb push lease-gate.rom    "$D/lease-gate.rom" >/dev/null
adb push net-echo.rom      "$D/net-echo.rom" >/dev/null
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
# 4) the pushed emulator really carries the net device (0xd0).
#    Asserting the VERDICT here would assert nothing: a net-blind build answers `NA` rc=2,
#    identical on stdout to a real refusal. The loud `net:` stderr line is the only signal a
#    device-less build cannot produce, so that is what we grep. Target 127.0.0.1:1 on the
#    phone itself — nothing listens, so this is a refusal by design and needs no far node.
#    RED-first, watched 2026-07-24: merely DROPPING net.c does not exercise this step — it
#    fails at LINK ("undefined reference to net_dei"), because uxncli.c references the device
#    unconditionally. The mutant that actually isolates step 4 is a net-BLIND stub —
#    `Uint8 net_dei(Uint8 a){return 0;} void net_deo(Uint8 a){}` — i.e. exactly emu_dei's
#    fallthrough. Built against that, steps 1-3 stay green, the ROM stays byte-identical, and
#    step 4 goes red reporting `got: NA`: the plausible constant, with nothing else disturbed.
#
#    KNOWN LIMIT (measured on-device, not inferred): the static armhf build cannot resolve
#    HOSTNAMES — glibc's getaddrinfo needs NSS shared libraries at runtime and bionic has no
#    glibc, hence the linker's warning. It fails LOUD and distinguishably, so it is a limit and
#    not a trap: `tcp:mesh-home.local:47101` -> "Temporary failure in name resolution", vs
#    `tcp:192.168.8.225:47101` -> "Connection refused". Address Note3 ROMs by NUMERIC IP.
netout="$(adb shell "su -c 'cd $D && ./uxncli net-echo.rom tcp:127.0.0.1:1'" 2>&1)"
case "$netout" in
  *net:*) echo "note3  net device present: yes ($(printf '%s' "$netout" | grep -o 'net:.*' | head -1))" ;;
  *) echo "note3  net device MISSING — no loud 'net:' line, emulator is net-blind (got: $(printf '%.60s' "$netout"))"; rc=1 ;;
esac

[ "$rc" = 0 ] && echo "verify-note3: ok — identical ROM, matching verdicts on armeabi-v7a, net device live" || echo "verify-note3: FAIL"
exit $rc
