# Health warning triage: `health-warning/13cf565351c60fb48a81/triage`

This is a separate warning key from `health-warning/21b83e4337b01ec10b67/triage`. It compares the 2026-09-11 06:23 doctor artifact with the 05:26 check stream and says the egress failures persist while several warning categories were added. The exact owner row passed `mesh-task check dispatch` (exit 0) and was claimed by `health`.

## Fresh verification

- The live `mesh-doctor` run reproduced the two egress failures (`tailscale0`; exit node `n2sbt7yy6t11CNTRL`) and `mic DEFAULT device broken/busy`; its explicit `plughw:1,0` capture passed.
- The newer doctor output also reproduced each newly named static warning:
  - `mesh-load-audit` has peer SSH without `ConnectTimeout`; this is a possible hang on an unreachable peer, not evidence that an SSH call is currently hung.
  - `mesh-song-verify` has six `librosa-analysis` bypasses of its declared sole-path funnel at lines 94, 95, 102, 109, 111, and 114.
  - Five sites collapse probe absence into a negative verdict: `mesh-body-backup` (zero size → FAIL), `mesh-clear-health` (missing/old reactor age → FAIL), `mesh-random-track-grind` (timeout → FAILED), `mesh-revive` (zero rows → OFFLINE), and `mesh-say` (timeout → FAILED). These are static detector findings; the doctor output does not show that these failure arms fired during this check.
- The full doctor command was still in its node-aware smoke-test section when inspected. This receipt records the warning lines actually emitted and does not claim the entire doctor run completed.
- Fresh `mesh-health` passed `mesh-home` and `phaedra`; it skipped `imac-rozalia` because SSH authentication was refused. Current Tailscale status now reports `imac-rozalia` online and active via relay `hel`, so the task text's “imac remains offline” is stale. GL-MT3000 remains offline, while `phaedra` remains the active exit node via relay `tor`.
- The separate LAN sensor still returns `UNKNOWN` because there is no local address in `192.168.8.0/24` and its router is unreachable. The route lookup still sends `100.76.0.1` through `tailscale0` in table 52; `213.87.2.89` and `217.66.16.35` remain the physical-link DNS servers.
- The VPN-owned `exit-node-lan-cgnat-repair-20260912` chain is active at step 1; health's independent route verification is step 4 and is not yet eligible. Health made no substrate change.

## Disposition

The egress/exit-node and mic-default alarms remain live. The added doctor warnings are reproducible source-level risks with exact affected tools and sites, but they were not repaired by this triage; they remain visible as known software-health findings. The iMac-offline clause is stale, and its SSH-authentication failure remains a reachability blind spot rather than proof of an offline peer. Inward LAN/router presence also remains unknown until the VPN-owned route repair completes and health can run its queued independent verification.
