# Health warning triage: Redmi 10 SAF listing remains unreachable

Chain: `health-warning/75e5efedd377e46614e6/triage`  
Checked: 2026-09-12 (UTC)  
Source warning: health observed `/tmp/discover-phone-saf-ls-20260909T0335Z.txt` on 2026-09-09, but its recorded SSH probe timed out and `termux-saf-ls` was never driven.

## Current evidence

- The old `/tmp/discover-phone-saf-ls-20260909T0335Z.txt` artifact no longer exists.
- A fresh bounded SSH probe, `timeout 8 ssh -o BatchMode=yes -o ConnectTimeout=5 -p 8022 u0_a386@100.103.99.16 true`, timed out (exit 255).
- `tailscale status --json` identifies `100.103.99.16` as `Redmi 10` (`redmi-10.tail3e4555.ts.net`), `Online=false`, last seen `2026-09-03T09:53:36.1Z`.
- `tailscale ping --c 3 100.103.99.16` received no replies (exit 1).

## Disposition

The warning is current: the Redmi 10 has been offline on the tailnet since the recorded last-seen time, and its SSH service cannot be reached. There is no safe host-side repair while the phone is offline. The SAF read remains an explicit known blind; do not report SAF contents or device health from the stale find artifact. Retry SSH and then run `termux-saf-ls` only after the peer returns online. No routing, DNS, firewall, VPN, or other substrate state was changed.
