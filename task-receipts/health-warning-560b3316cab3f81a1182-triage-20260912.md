# Health warning triage: check-stream delta

Chain: `health-warning/560b3316cab3f81a1182/triage`  
Checked: 2026-09-12 06:00 UTC on `mesh-home`  
Source: the 2026-09-09 09:44Z check-stream delta reported a new `stress.log` doctor failure, `mesh-usb`/`mesh-wifi-*` smoke failures, unknown LAN/router presence, `imac-rozalia` changing from direct to relay, and egress through `tailscale0`.

## Current evidence

- The consumed `mesh-dash --once check` pane at 05:57Z showed load above the 16-core count and a cached doctor summary of 3 FAIL/33 WARN. Its displayed failures were egress on the overlay, an exit-node SPOF, and `scripts/tinyfleet_split_audit.py` lacking its execute bit. The fleet view had 8 nodes down; no substrate action was taken.
- `mesh-card --refresh` at 05:58Z confirmed default egress on `tailscale0`, exit node `phaedra`, and the declared invariant violation: table 52 sends the local LAN gateway through the overlay. This is an observed substrate fault; this triage made no route, DNS, firewall, or VPN changes.
- A fresh `mesh-doctor` run began at 05:58Z and was still running at 06:00Z, so no complete fresh doctor verdict is claimed. Its captured section repeated the two egress-integrity FAILs and showed supervised loops UP. The concurrent `mesh-reflex-health` invocation exited 1 and reported `lan-newdevice` and `wifi-link` as organ-blind, `router-watch` stale, and `wifi-rf` absent; its hand-run mode did not write the shared edge.
- `/home/mesh-home/.mesh/stress.log` still contains exactly two tail errors from `mesh-stress`: `note3_ambient_state: unbound variable` (line 436) and `clock_sync_state: unbound variable` (line 421). The file mtime is 2026-09-09 09:05:05Z, so these are retained historical errors, not evidence of a new occurrence during this pass.
- `mesh-usb --test` exited 1 with `live-xhci-blind-without-errno live-urb-blind-without-errno`. This is a current failing test with missing errno evidence; no USB repair was attempted.
- `mesh-wifi-quality --test` exited 1 with `no wireless iface`. The smoke path is currently failing; this alone does not establish whether a wireless organ is absent or malfunctioning.
- `mesh-lan-presence --nodes` exited 1 and reported `UNKNOWN`: no address in `192.168.8.0/24`, no ARP visibility into that segment, and no known ICMP responder. LAN/router health remains an explicit blind.
- `tailscale status` showed `imac-rozalia` active through DERP `hel`; `tailscale ping --c 1 100.121.88.110` returned a pong via `DERP(hel)` in 283 ms and exit 1 (`direct connection not established`). The peer is reachable over relay, not direct.
- `mesh-health` at 05:58Z showed `mesh-home` and `phaedra` reachable, most other peers offline, and the iMac SSH probe skipped for authentication refusal. These observations do not establish the unreachable peers' physical health.

## Disposition

The relay shift and overlay-egress condition remain observable. LAN/router state is still UNKNOWN. The USB and Wi-Fi quality smoke tests currently fail; the USB diagnostic remains blind on errno, while Wi-Fi reports no interface. The stress errors remain in a log last written on 2026-09-09 and were not reproduced here. A full fresh doctor verdict remains unavailable because its scan did not finish during this pass. No substrate state was changed. Follow-up belongs with the owners of the failing USB/Wi-Fi tests and stress producer; routing remediation stays under the health charter's claim and `mesh-dms` discipline.
