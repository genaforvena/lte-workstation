#!/usr/bin/env bash
# verify-note3.sh — prove the byte-identical lease-gate.rom runs on the Note3 (armeabi-v7a).
#
# The Note3 has no on-device compiler, so we cross-build a static armhf uxncli on the host,
# push it + the UNMODIFIED rom over adb, and run the same gate under su. The ROM is never
# rebuilt — only the emulator is per-platform. Requires: adb (Note3 on USB), and
# arm-linux-gnueabihf-gcc on the host. This IS the mesh's distribution model for every node
# without a compiler (which is all of them but mesh-home) — see build.sh's header.
#
# net.c IS IN THE CROSS-BUILD LINE, and steps 4-5 assert the pushed binary really carries the
# device. Omitting it produces a NET-BLIND emulator, and a net-blind emulator is not a loud
# failure: uxncli's emu_dei falls through to `return uxn.dev[addr]` = 0, and net state 0 is
# Disconnected — so a ROM on a device-less build answers `NA` rc=2, byte-identical on stdout
# to a genuine connection refused.
#
# Step 4 used to INFER presence from a refused connect, which is exactly the ambiguous byte
# the identify probe exists to replace. It now asks: action d0 Identify writes a magic into
# the length register that a bare memory page cannot fake, and the ROMs compare it as an
# ordering (device d0, step >= what the ROM needs). Three outcomes are now DISTINCT where
# they used to be one — measured on this phone 2026-07-24, all three seen:
#   NODEV rc3, stderr silent            → no device in this build at all
#   NODEV rc3, stderr 'net: unknown action' → device present but TOO OLD (pre-identify)
#   NA rc2, stderr 'net: …'             → device present, and it refused for a real reason
# Version SKEW therefore reads as no-usable-device — fail-closed — and the stderr line is the
# only thing separating absent from old, which is why this asserts both.
#
# Step 5 is the artifact for the step-2 half: the phone BINDS and this host dials it. Presence
# is not capability — a build can carry the device and still not listen — and the bind path is
# where a static armhf libc could plausibly differ from the host's.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"; cd "$here"
CROSS="${CROSS:-arm-linux-gnueabihf-gcc}"
NPORT="${NOTE3_NET_PORT:-47312}"
command -v "$CROSS" >/dev/null || { echo "need $CROSS (apt install gcc-arm-linux-gnueabihf)"; exit 2; }
adb get-state >/dev/null 2>&1 || { echo "no adb device"; exit 2; }
bind_ran=no; hop_ran=no   # a leg that did not run must not be claimed by the summary

# 0) WHAT THE PHONE WAS ALREADY CARRYING, measured before anything is pushed. This is the
#    only moment in this script when the on-device binary is not one we just installed, and
#    it is the only moment the fleet's version skew is observable at all: a node with no
#    compiler carries whatever was last pushed to it, through however many NET_IDENT bumps
#    happened since, and a ROM needing a later step reads that stale build as an ordinary
#    refusal — fail-closed, silent, and byte-identical to the far node saying no. Reported,
#    never asserted: this script REPAIRS the skew three lines below, and a check that fixes
#    what it measures can never be seen fail. The assertion is post-push, at step 2b.
D=/data/local/tmp
prev_ident=""
if adb push net-ident.rom "$D/net-ident.rom" >/dev/null 2>&1; then
  prev_ident="$(adb shell "su -c 'cd $D && ./uxncli net-ident.rom </dev/null'" 2>/dev/null | tr -dc '0-9a-fA-F' | tr 'A-F' 'a-f')"
fi
src_ident="$(grep -oE '#define[[:space:]]+NET_IDENT[[:space:]]+0x[0-9a-fA-F]{4}' src/devices/net.h \
             | grep -oiE '0x[0-9a-f]{4}' | head -1 | sed 's/^0[xX]//' | tr 'A-F' 'a-f')"
case "$prev_ident" in
  "")            echo "note3  pre-push: no emulator on the phone yet (or it would not run) — first install" ;;
  "$src_ident")  echo "note3  pre-push: the phone already carried $prev_ident, current with this source" ;;
  0000)          echo "note3  pre-push: the phone carried a NET-BLIND build (identify 0000) — no 0xd0 device at all" ;;
  *)             echo "note3  pre-push: SKEW — the phone carried $prev_ident, this source declares $src_ident (a ROM needing the later step read that as a refusal)" ;;
esac

# 1) static armhf emulator (bionic has no glibc loader; static = pure-syscall, runs under the
#    Android kernel). The compile line itself lives in cross-build.sh — ONE copy, shared with
#    build.sh's host build via emu-sources, because this file having its own copy is how a
#    device gets added to the emulator and silently never reaches the phone.
./cross-build.sh armhf /tmp/uxncli.armhf || { echo "verify-note3: cross-build failed"; exit 2; }

# 2) push the emulator + the UNMODIFIED rom
adb push /tmp/uxncli.armhf "$D/uxncli" >/dev/null
adb push lease-gate.rom    "$D/lease-gate.rom" >/dev/null
adb push net-echo.rom      "$D/net-echo.rom" >/dev/null
adb push net-listen.rom    "$D/net-listen.rom" >/dev/null
adb push net-dgram.rom     "$D/net-dgram.rom" >/dev/null
adb push gossip.rom        "$D/gossip.rom" >/dev/null   # the phone is the node the gossip
                           # lane exists for: with only uxncli it is a full participant, not
                           # something a node with a shell has to poll on its behalf
adb push hop-serve.rom     "$D/hop-serve.rom" >/dev/null
adb push rot13-net.rom     "$D/rot13-net.rom" >/dev/null
adb push arith64-test.rom  "$D/arith64-test.rom" >/dev/null
# prove byte-identity by pulling the on-device rom back and cmp'ing (Android shell has no sha1sum)
adb pull "$D/lease-gate.rom" /tmp/rom.fromnote3 >/dev/null 2>&1
if cmp -s lease-gate.rom /tmp/rom.fromnote3; then
  echo "rom byte-identical host<->note3: yes ($(wc -c <lease-gate.rom)b, sha1 $(sha1sum lease-gate.rom | awk '{print $1}'))"
else echo "rom DIFFERS host<->note3"; exit 1; fi

# 2b) THE PUSH LANDED AND IS WHAT RUNS. Asserted, not assumed: `adb push` reporting success
#     says a file was written, not that the binary the phone EXECUTES is that file — a stale
#     copy earlier on the path, a partial write, or a binary that will not start all leave
#     the push looking fine. The identify word comes from the device pokeing NET_IDENT into
#     the length register, so it is a claim about the running code and nothing else.
adb push net-ident.rom "$D/net-ident.rom" >/dev/null
now_ident="$(adb shell "su -c 'cd $D && ./uxncli net-ident.rom </dev/null'" 2>/dev/null | tr -dc '0-9a-fA-F' | tr 'A-F' 'a-f')"
if [ -z "$src_ident" ]; then
  echo "note3  NET_IDENT not parseable from src/devices/net.h — the version assertion did NOT run"; exit 1
elif [ "$now_ident" = "$src_ident" ]; then
  echo "note3  post-push: the phone now identifies $now_ident == source $src_ident"
else
  echo "note3  post-push: FAILED — the phone identifies '${now_ident:-<empty>}', source declares $src_ident; the push did not become the running binary"; exit 1
fi

# 3) run the SAME rom on-device, same truth table as the host (uxncli logs 'Loaded' to stderr;
#    adb merges streams, so extract just the trailing verdict token)
run(){ adb shell "su -c 'cd $D && chmod 755 uxncli && ./uxncli lease-gate.rom $1 $2'" 2>/dev/null | grep -oE 'OK|RED' | tail -1; }
rc=0
for t in "900 1800 OK" "900 900 RED" "900 1799 RED" "1800 3600 OK"; do
  set -- $t; got="$(run "$1" "$2")"
  [ "$got" = "$3" ] && echo "note3  cad=$1 lease=$2 -> $got  (ok)" \
                    || { echo "note3  cad=$1 lease=$2 -> $got  (WANT $3)"; rc=1; }
done
# 4) the pushed emulator really carries the net device (0xd0), AT THE STEP THIS ROM NEEDS.
#    Asserting the VERDICT alone would assert nothing: a net-blind build answers `NA` rc=2,
#    identical on stdout to a real refusal. So the ROM identifies the device FIRST (see the
#    header) and this step reads the three outcomes apart. Driven by net-listen.rom, which
#    demands step >= 2, against 203.0.113.1 (RFC5737 TEST-NET-3 — not an address on the
#    phone, so bind(2) answers EADDRNOTAVAIL by design and no far node is involved). One run
#    therefore asserts: device present · step >= 2 · and the bind REFUSAL path on armhf.
#    RED-first, watched 2026-07-24: merely DROPPING net.c does not exercise this step — it
#    fails at LINK ("undefined reference to net_dei"), because uxncli.c references the device
#    unconditionally. The mutant that actually isolates step 4 is a net-BLIND stub —
#    `Uint8 net_dei(Uint8 a){return 0;} void net_deo(Uint8 a){}` — i.e. exactly emu_dei's
#    fallthrough. Built against that, steps 1-3 stay green, the ROM stays byte-identical, and
#    step 4 goes red — now reporting NODEV, which is the point: the blind build NAMES itself
#    instead of impersonating a refusal.
#
#    KNOWN LIMIT (measured on-device, not inferred): the static armhf build cannot resolve
#    HOSTNAMES — glibc's getaddrinfo needs NSS shared libraries at runtime and bionic has no
#    glibc, hence the linker's warning. It fails LOUD and distinguishably, so it is a limit and
#    not a trap: `tcp:mesh-home.local:47101` -> "Temporary failure in name resolution", vs
#    `tcp:192.168.8.225:47101` -> "Connection refused". Address Note3 ROMs by NUMERIC IP.
netout="$(adb shell "su -c 'cd $D && ./uxncli net-listen.rom tcp:203.0.113.1:$NPORT'" 2>&1)"
case "$netout" in
  *NODEV*unknown\ action*|*unknown\ action*NODEV*)
    echo "note3  net device TOO OLD — it answered the identify probe with 'unknown action', so it predates step 2 (bind). Re-push: this script's step 1-2."; rc=1 ;;
  *NODEV*)
    echo "note3  net device MISSING — the ROM identified no 0xd0 device at all (got: $(printf '%.60s' "$netout"))"; rc=1 ;;
  *NA*)
    if printf '%s' "$netout" | grep -qi 'assign'; then
      echo "note3  net device present at step >= 2: yes (bind refused loudly: $(printf '%s' "$netout" | grep -o 'net:.*' | head -1))"
    else
      echo "note3  net device answered NA without naming a cause — refusal path is silent (got: $(printf '%.80s' "$netout"))"; rc=1
    fi ;;
  *) echo "note3  unexpected identify outcome (got: $(printf '%.80s' "$netout"))"; rc=1 ;;
esac

# 5) THE PHONE BINDS AND THIS HOST DIALS IT — presence is not capability.
#    Step 4 proves the device is there; only a real inbound connection proves the armhf build
#    can actually listen, and bind/accept is where a statically linked libc could plausibly
#    differ from the host's. The phone binds its OWN wlan address (numeric — see the known
#    limit above), we dial it over the LAN, and the reply must carry net-listen's 'uxn:' tag:
#    a bare echo, a stray listener, or our own buffer read back all produce the payload, and
#    only the ROM produces the tag. Unreachable phone address → n/a, never a silent pass.
PHONE_IP="${NOTE3_IP:-$(adb shell "ip -4 addr show wlan0" 2>/dev/null | grep -o 'inet [0-9.]*' | awk '{print $2}' | head -1)}"
if [ -z "$PHONE_IP" ]; then
  echo "note3  bind round trip: n/a — no wlan0 address on the phone (it did NOT run)"
  bind_ran=no
else
  expect="uxn:ping-from-$(hostname)"
  adb shell "su -c 'cd $D && UXN_NET_TIMEOUT=25 ./uxncli net-listen.rom tcp:$PHONE_IP:$NPORT'" >/tmp/note3-listen.out 2>&1 &
  lpid=$!
  sleep 3
  reply=""
  if exec 3<>"/dev/tcp/$PHONE_IP/$NPORT" 2>/dev/null; then
    printf 'ping-from-%s\n' "$(hostname)" >&3
    reply="$(timeout 15 head -c ${#expect} <&3)"
    exec 3<&-
  fi
  wait "$lpid" 2>/dev/null || true
  if [ "$reply" = "$expect" ]; then
    echo "note3  LIVE bind round trip: $(hostname) -> $PHONE_IP:$NPORT, the PHONE's uxncli answered '$reply'"
    bind_ran=yes
  else
    echo "note3  LIVE bind round trip FAILED: want '$expect', got '$reply' (phone said: $(head -2 /tmp/note3-listen.out | tr '\n' ' '))"; rc=1
  fi
fi

# 6) THE HOP'S NET LANE, ON THE PHONE: mesh-home ships a ROM this phone has never seen and
#    the phone's uxncli BECOMES it. hop-serve reads the packet off the socket, stages it at
#    4000, relocates a position-independent copier to 8000 and jumps — the emulator is then
#    running code that arrived a moment ago, still holding the caller's connection because
#    the socket lives in the DEVICE and not in the 64 KB that was overwritten.
#    This is the entire "the far node needs only uxncli" claim reduced to one artifact: no
#    shell, no ssh, no mesh-uxn-hop on the phone — a static binary and a socket.
#    The token is generated PER RUN, so a pass cannot come from a constant baked anywhere.
if [ -z "${PHONE_IP:-}" ]; then
  echo "note3  hop net lane: n/a — no wlan0 address (it did NOT run)"
  hop_ran=no
else
  HTOK="$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n')"
  hexp="$(printf 'Hello from mesh-home' | tr 'A-Za-z' 'N-ZA-Mn-za-m')"
  adb shell "su -c 'cd $D && UXN_NET_TIMEOUT=15 ./uxncli hop-serve.rom tcp:$PHONE_IP:$((NPORT + 1)) $HTOK </dev/null'" >/tmp/note3-hop.out 2>&1 &
  hpid=$!
  sleep 3
  printf 'Hello from mesh-home' | UXN_HOP_TOKEN="$HTOK" ./mesh-uxn-hop --pack-net rot13-net.rom >/tmp/note3-hop.pkt
  hgot="$(UXN_NET_TIMEOUT=6 timeout 40 ./mesh-uxn-hop --dial "tcp:$PHONE_IP:$((NPORT + 1))" </tmp/note3-hop.pkt 2>/dev/null || true)"
  wait "$hpid" 2>/dev/null || true
  if [ "$hgot" = "$hexp" ]; then
    echo "note3  HOP NET LANE: shipped rot13-net.rom over TCP and the PHONE's uxncli became it — '$hgot' (no shell on the far side)"
    hop_ran=yes
  else
    echo "note3  HOP NET LANE FAILED: want '$hexp', got '$hgot' (phone said: $(head -3 /tmp/note3-hop.out | tr '\n' ' '))"; rc=1
  fi
fi

# 7) THE 64-BIT ARITHMETIC, ON THE PHONE. The whole point of arith64 is that a verdict
#    computed from wide numbers means the same thing on both machines, and the place that
#    could plausibly differ is exactly here: the carry chain is unsigned-wrap comparisons,
#    and a 32-bit ARM libc/compiler is where a wrong-width intermediate would show up. The
#    ROM is unmodified and its byte-identity is proven at step 2 for lease-gate; this
#    re-proves it for arith64-test and then requires every row of the HOST's own truth
#    table to come back identical from the phone.
#    adb shell READS STDIN, so the row loop feeds from fd 3 and every adb call gets
#    </dev/null — otherwise adb swallows the table and one row masquerades as all of them.
adb pull "$D/arith64-test.rom" /tmp/rom64.fromnote3 >/dev/null 2>&1
if cmp -s arith64-test.rom /tmp/rom64.fromnote3; then
  a64ok=0; a64bad=0
  while read -r op a b want <&3; do
    [ -n "${op:-}" ] || continue
    printf '%s\n%s\n%s\n' "$op" "$a" "$b" > /tmp/in64.txt
    adb push /tmp/in64.txt "$D/in64.txt" >/dev/null 2>&1 </dev/null
    got="$(adb shell "su -c 'cd $D && ./uxncli arith64-test.rom < in64.txt'" 2>/dev/null </dev/null | tr -d '\r' | tail -1)"
    if [ "$got" = "$want" ]; then a64ok=$((a64ok+1)); else
      a64bad=$((a64bad+1)); [ "$a64bad" -le 3 ] && echo "note3  arith64 op=$op a=$a b=$b: host $want, phone $got"
    fi
  done 3< <(./test-arith64 --table)
  if [ "$a64bad" = 0 ] && [ "$a64ok" -ge 30 ]; then
    echo "note3  ARITH64: $a64ok/$a64ok rows identical on armeabi-v7a from the same $(wc -c <arith64-test.rom)b rom"
  else
    echo "note3  ARITH64 FAILED: $a64bad row(s) differ, $a64ok agreed (a table of $((a64ok+a64bad)) rows)"; rc=1
  fi
else
  echo "note3  arith64 rom DIFFERS host<->note3"; rc=1
fi

# The summary names only what ACTUALLY RAN. The net legs render n/a whenever the phone has no
# wlan0 address, and a fixed sentence that credits them anyway turns an honest skip into a
# false claim — the failure this whole file exists to make impossible.
if [ "$rc" = 0 ]; then
  summary="verify-note3: ok — identical ROM, matching verdicts on armeabi-v7a, net device live at step >= 2, and its 64-bit carry chain agrees with the host row for row"
  [ "$bind_ran" = yes ] && summary="$summary; the phone answered a real inbound connection"
  [ "$hop_ran"  = yes ] && summary="$summary; it ran a ROM that arrived over the socket"
  [ "$bind_ran" = yes ] || [ "$hop_ran" = yes ] || summary="$summary (the two net legs did NOT run — no wlan0 address)"
  echo "$summary"
else
  echo "verify-note3: FAIL"
fi
exit $rc
