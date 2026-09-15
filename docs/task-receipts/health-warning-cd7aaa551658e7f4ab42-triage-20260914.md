# Health roll-call triage: iMac path and incomplete doctor count

Task: `health-warning/cd7aaa551658e7f4ab42/triage`  
Source warning: 2026-09-12T16:52:20Z check-stream delta

## Current evidence at 2026-09-14 20:08–20:14Z

- The warning's imac-rozalia relay state is stale. Current `tailscale status` reports the peer
  active/direct at `5.227.24.249:42772`; a fresh ping returned in 4 ms. SSH authentication is a
  separate host-key issue and was not retried here.
- Current egress in the 20:08Z one-shot pane was `OK loss=0%`. Phaedra is still the selected
  single exit node, so the availability dependency remains a known risk. The current LAN prefix
  has changed since the old report: `mesh-card --exit-node-lan` reports `100.74.186.131/16`,
  target `100.74.0.1`, `enp42s0`, verdict `ok`; the FIB resolves the gateway on `enp42s0`.
- The 20:08Z doctor cache still reads `2026-09-14T19:32:22Z FAIL=0 WARN=33` (age 36 minutes).
  The latest completed quiet doctor receipt records `0 FAIL / 34 WARN` at 14:42Z. To check the
  stale warning, I confirmed the doctor lock was free and started `/home/mesh-home/.local/bin/
  mesh-doctor --quiet` at 20:12:06Z. It immediately identified the intentional exit-node consumer
  NOTE and mic DEFAULT warning, then expanded into many separate tool tests and remained active
  after 2m38s. I stopped only its dedicated process group; the command exited 143 without a final
  FAIL/WARN count. Therefore the present total remains **unconfirmed**; the stale cache and the
  earlier completed zero-FAIL runs are evidence, not a fresh completed result.
- DNS was consistent across system and public recursive resolvers in the 19:47Z check
  (`api.anthropic.com` A=`160.79.104.10`); the hostname completed TLS. `mesh-lan-presence --nodes`
  remains `UNKNOWN` because the host has no local `192.168.8.0/24` address and no known host
  answered ICMP.

## Disposition

Peer path and local gateway health have changed since the warning; egress works on the configured
exit-node path, whose single-node dependency remains. The broad doctor refresh did not finish, so
its total is still a named blind rather than a pass. Retry a policy-aware doctor run only in a
lower-load slot with an explicit 120-second outer bound; if it times out, capture the exact
unfinished subject before claiming a total. LAN/router presence remains a separate unknown. No
route, DNS, firewall, VPN, service, peer, or device state was changed.

## Verification

- `tailscale status` and `tailscale ping -c 3 imac-rozalia`: active direct; 4 ms pong.
- `mesh-dash --once check` at 20:08:50Z: egress loss 0%, doctor cache 0 FAIL/33 WARN, age 36m.
- `mesh-card --exit-node-lan` and `ip -4 route get 100.76.0.1`: current gateway `100.74.0.1`
  resolves via `enp42s0`, state OK.
- The doctor lock was free before the run. The 20:12Z `--quiet` run was stopped after 2m38s;
  its exit was 143 and no final total is claimed. Its separate process group was confirmed and
  terminated without signaling other mesh jobs.
- DNS system/public-resolver and TLS evidence is in
  `health-warning-dc221f87143bc683b504-triage-20260914.md`.
