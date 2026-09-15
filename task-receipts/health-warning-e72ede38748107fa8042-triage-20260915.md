# Health warning triage — Redmi Termux prior-art claim — 2026-09-15

Task: `health-warning/e72ede38748107fa8042/triage`

## Evidence

- Read the cited receipt `task-receipts/health-loop-baton-verify-discover-20260914T1529Z.md`.
  It records that `termux-saf-ls` was prior art, with no command-level sample, and that
  the Redmi 10 tailnet peer was offline.
- Read the cited knowledge artifact
  `/home/mesh-home/.mesh/knowledge/frontier-dry-phone-termux-uncatalogued-20260912.md`
  (1364 bytes; SHA-256 `676002fe0e6d7d3ac5316b8169625d4d3bbca29a740e9e00eb7d2dfedc16cb5c`).
- Read the independent verification receipt
  `docs/task-receipts/health-verify-discover-termux-20260913.md`. The task's shortened
  path omitted the `-20260913` filename suffix; the full receipt exists at that path.
- Read the fresh discovery artifact `/tmp/discover-saf-ls-20260915.txt` (285 bytes;
  SHA-256 `e14177f390dfb42a0f2132ebc9e214ea52f6a9e635e4928e7c7d27fefdbed93a`). Its three
  SSH attempts all returned `rc=255`: `192.168.8.203` refused, `192.168.8.146` timed out,
  and `100.103.99.16` timed out.
- A live `tailscale status --json` read at 20:32Z reports `Redmi 10 100.103.99.16
  online=false`, last seen `2026-09-03T09:53:36Z`.
- The live pane reports local load high, so broad reachability non-answers remain
  probe-unreliable. Doctor evidence is also not a current Redmi capability signal:
  the 20:23Z run reports `1 FAIL, 33 WARN`, including `dispatch.log` failure and an
  untimed peer-SSH warning; the pane cache is stale relative to the live state.

## Disposition

Report-only: the prior-art result is supported, but no live Redmi transport or
command-level `termux-saf-ls` evidence is available. This remains a known Redmi SSH
reachability blind spot, not a new capability, device fault, or authorization for a
network/substrate change. Retry only after a changed endpoint reachability signal.

## Verification

The cited artifacts, live Tailscale status, bounded three-endpoint SSH recheck, and
doctor log were read. No routing, DNS, firewall, VPN, device, service, or privilege
state changed.
