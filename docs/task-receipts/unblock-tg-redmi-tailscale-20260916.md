# `tg` blocker resolution — Redmi Tailscale reconnect

- Task: `unblock/tg/6fcdcbcef6e5bd0f/resolve`
- Owner: `tg`
- Observed: 2026-09-16T02:50:50Z
- Result: blocked by external GUI state; no substrate mutation made.

## Live evidence

`tailscale status --json` identifies exactly one canonical Redmi peer:

```text
HostName: Redmi 10
TailscaleIPs: 100.103.99.16, fd7a:115c:a1e0::133b:6310
Online: false
Active: true
LastSeen: 2026-09-03T09:53:36.1Z
Tags: tag:lte-node
```

`mesh-health --once` simultaneously reports:

```text
LAN   Redmi 10  192.168.8.203 — reachable off-tailnet
```

The LAN SSH control path is live and identifies the expected Termux user:

```text
ssh -p 8022 u0_a380@192.168.8.203 'printf "ssh-ok\\n"; ...'
ssh-ok
/data/data/com.termux/files/usr/bin/termux-battery-status
```

This separates the remaining blocker from LAN power/SSH reachability: the phone is reachable,
but the Tailscale app's GUI-controlled peer has not reconnected. No duplicate identity, route,
DNS, firewall, VPN, or Tailscale state was changed. The retry event is a Redmi-side Tailscale
app reconnect; after that event rerun `tailscale status --json` and `mesh-health --once`, then
resume the onboarding completion task only if `Redmi 10` is `Online: true` with the canonical
tag and identity.
