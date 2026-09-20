#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
tool="$repo/scripts/mesh-systemd-security"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/bin"

cat >"$tmp/bin/systemctl" <<'EOF'
#!/usr/bin/env bash
printf 'alpha.service loaded active running Alpha\nbeta.service loaded active running Beta\n'
EOF
cat >"$tmp/bin/systemd-analyze" <<'EOF'
#!/usr/bin/env bash
case "$2" in
  alpha.service) printf '%s\n' '→ Overall exposure level for alpha.service: 1.6 OK :-)' ;;
  beta.service) printf '%s\n' '→ Overall exposure level for beta.service: 9.6 UNSAFE :-{' ;;
  *) exit 1 ;;
esac
EOF
chmod +x "$tmp/bin/systemctl" "$tmp/bin/systemd-analyze"

out="$(PATH="$tmp/bin:/usr/bin:/bin" "$tool" --units 2>&1)"
grep -Fq 'systemd-security: units=2 ok=1 medium=0 unsafe=1' <<<"$out"
grep -Fq $'alpha.service\t1.6\tOK' <<<"$out"
grep -Fq $'beta.service\t9.6\tUNSAFE' <<<"$out"
PATH="$tmp/bin:/usr/bin:/bin" "$tool" --test >/dev/null

echo "PASS: parses running units and reports exposure bands"
