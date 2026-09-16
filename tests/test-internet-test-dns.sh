#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$ROOT/scripts/internet-test-dns.ps1"

[[ -f "$SCRIPT" ]] || { echo "FAIL: DNS diagnostic script is missing"; exit 1; }
for token in Resolve-DnsName DnsServer 1.1.1.1 8.8.8.8 failure_reason; do
    rg -Fq "$token" "$SCRIPT" || { echo "FAIL: missing DNS probe token: $token"; exit 1; }
done
rg -Fq 'timestamp_utc,elapsed_s,gateway,internet,router_dns,cloudflare_dns,google_dns,system_dns,failure_reason' "$SCRIPT" \
    || { echo "FAIL: CSV does not expose per-resolver results and failure reason"; exit 1; }
echo "ok: DNS diagnostic script exposes comparative probes and reasons"
