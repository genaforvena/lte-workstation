#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$ROOT/scripts/reticulum/rns-offgrid-proof.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
BIN="$TMP/bin"
mkdir -p "$BIN" "$TMP/home/.mesh" "$TMP/rns-venv"

cat > "$BIN/ip" <<'EOF'
#!/usr/bin/env bash
case "$*" in
  "-4 route show default")
    echo 'default via 10.0.0.1 dev eth7 proto dhcp metric 42'
    if [[ "${ROUTE_FIXTURE:-}" == ambiguous ]]; then
      echo 'default via 10.0.0.254 dev eth8 proto dhcp metric 42'
    elif [[ "${ROUTE_FIXTURE:-}" == missing-gateway ]]; then
      echo 'default dev tun0 scope link metric 10'
    else
      echo 'default via 10.0.0.254 dev eth8 proto dhcp metric 90'
    fi
    ;;
  "-4 -o addr show scope global") echo '2: eth7    inet 10.0.0.2/24 brd 10.0.0.255 scope global eth7' ;;
  *) exit 0 ;;
esac
EOF
cat > "$BIN/sudo" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$TEST_SUDO_LOG"
exit 0
EOF
cat > "$BIN/ssh" <<'EOF'
#!/usr/bin/env bash
case "$*" in
  *"cat /tmp/offgrid-blackout.result"*) echo 'PROOF OK' ;;
esac
exit 0
EOF
cat > "$BIN/scp" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat > "$BIN/ping" <<'EOF'
#!/usr/bin/env bash
case "${*: -1}" in
  peer.example) exit 0 ;;
  *) exit 1 ;;
esac
EOF
cat > "$BIN/tailscale" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat > "$BIN/sleep" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat > "$TMP/rns-venv/python" <<'EOF'
#!/usr/bin/env bash
if [[ "${2:-}" == "server" ]]; then
  while (($#)); do
    if [[ "$1" == "--hashfile" ]]; then
      printf '%s\n' 'fixture-server-hash' > "$2"
      break
    fi
    shift
  done
fi
exit 0
EOF
chmod +x "$BIN"/* "$TMP/rns-venv/python"
export PATH="$BIN:/usr/bin:/bin"
export TEST_SUDO_LOG="$TMP/sudo.log"
export RNS_OG_LOCAL_LAN=10.0.0.2
export RNS_OG_PY="$TMP/rns-venv/python"
export RNS_OG_PEER_PY="$TMP/rns-venv/python"

# Missing peer configuration must be an explicit n/a before local prerequisites
# can obscure the reason or any SSH target can be contacted.
set +e
missing_out="$(env -i HOME="$TMP/home" PATH="$PATH" bash "$SCRIPT" --test 2>&1)"
missing_rc=$?
set -e
[[ $missing_rc -eq 2 ]] || { echo "missing-peer rc=$missing_rc output=$missing_out" >&2; exit 1; }
[[ "$missing_out" == *"n/a: peer not configured"* ]] || { echo "missing-peer message: $missing_out" >&2; exit 1; }

# Run the blackout orchestration with every actuator replaced by a stub. The
# restore command must use this fixture's live route values, never baked-in ones.
# Keep all script-created configs, logs, and pid files inside the fixture HOME.
export HOME="$TMP/home"
export RNS_OG_PEER=peer.example
out="$(bash "$SCRIPT" --blackout 2>&1)"
if grep -q '^FAIL:' <<< "$out"; then { echo "blackout fixture hit a failure: $out" >&2; exit 1; }; fi
grep -q 'OFF-INTERNET PROVEN' <<< "$out" || { echo "blackout fixture failed: $out" >&2; exit 1; }
grep -qx 'ip route replace default via 10.0.0.1 dev eth7 metric 42' "$TEST_SUDO_LOG" || {
  echo "route restore did not use discovered gateway/interface/metric:" >&2
  cat "$TEST_SUDO_LOG" >&2
  exit 1
}
grep -qx 'ip route del default' "$TEST_SUDO_LOG" || {
  echo 'blackout fixture did not exercise route removal' >&2
  cat "$TEST_SUDO_LOG" >&2
  exit 1
}

# Equal-priority defaults are ambiguous: refuse before removing any route.
: > "$TEST_SUDO_LOG"
set +e
ambiguous_out="$(ROUTE_FIXTURE=ambiguous bash "$SCRIPT" --blackout 2>&1)"
ambiguous_rc=$?
set -e
[[ $ambiguous_rc -eq 2 ]] || { echo "ambiguous-route rc=$ambiguous_rc output=$ambiguous_out" >&2; exit 1; }
[[ "$ambiguous_out" == *"n/a: --blackout needs one unambiguous IPv4 default route"* ]] || {
  echo "ambiguous-route message: $ambiguous_out" >&2
  exit 1
}
if grep -qx 'ip route del default' "$TEST_SUDO_LOG"; then
  echo 'ambiguous route was removed before refusing blackout' >&2
  exit 1
fi

# A default route without a gateway cannot be faithfully restored by this tool.
: > "$TEST_SUDO_LOG"
set +e
incomplete_out="$(ROUTE_FIXTURE=missing-gateway bash "$SCRIPT" --blackout 2>&1)"
incomplete_rc=$?
set -e
[[ $incomplete_rc -eq 2 ]] || { echo "incomplete-route rc=$incomplete_rc output=$incomplete_out" >&2; exit 1; }
[[ "$incomplete_out" == *"n/a: --blackout needs one unambiguous IPv4 default route"* ]] || {
  echo "incomplete-route message: $incomplete_out" >&2
  exit 1
}
if grep -qx 'ip route del default' "$TEST_SUDO_LOG"; then
  echo 'route without a gateway was removed before refusing blackout' >&2
  exit 1
fi

if rg -n 'ilya@100\.107\.198\.111|192\.168\.8\.1|wlxbcec43434a22|8\.8\.8\.8' "$SCRIPT"; then
  echo 'operator-specific or fixed network endpoint remains in script' >&2
  exit 1
fi

echo 'PASS: missing peer is honest; blackout restore derives its route; no fixed endpoints remain'
