# Sensor visibility receipt — 2026-09-16

Task: `sound-audit-sensor-visibility-20260916/refresh-perimeter-sensor-visibility`
Owner: `senses`
Source: `docs/chat-range-reviews/witness-chat-range-review-near-60513-60582.md` lines 60568–60569
Observed: 2026-09-16T06:45:42Z–2026-09-16T06:47:24Z UTC

## Fresh live reads

- `mesh-ambient-level --json` — rc 0; `QUIET`, device `overhear-tap@plughw:CARD=Camera,DEV=0`, RMS `-31.8dB`, peak `-17.9dB`, coverage `0.979`, age `3s`, timestamp `2026-09-16T06:45:42Z`.
- `mesh-wifi-motion --json` — bounded by `timeout 25s`; rc 124 and no output. Wi-Fi motion is UNKNOWN, not STILL.
- `mesh-wifi-link --json` — rc 2; no output. Phone Wi-Fi-link is unreachable/UNKNOWN.
- `mesh-gateway-identity --json` — rc 0; `STABLE`, gateway `192.168.8.1`, MAC `94:83:c4:68:07:66`, device `enp42s0`, timestamp `2026-09-16T06:46:10Z`.
- `mesh-lan-newdevice --status` — rc 0; DHCP unavailable, explicitly using LAN-side ARP fallback. Seven current ARP entries were emitted; the command reports 16 known LAN devices. This is lower-confidence LAN evidence, not DHCP proof.
- `mesh-perimeter` — bounded by `timeout 20s`; rc 124 and no fused output.
- `mesh-perimeter --edge` — bounded by `timeout -k 2s 10s`; rc 124 and no edge output.
- `mesh-dash --once senses` — bounded by `timeout -k 2s 10s`; rc 124 and no pane output.

## Honest result

The fresh evidence proves a live QUIET acoustic read and a stable local gateway. Wi-Fi motion,
phone Wi-Fi-link, DHCP, and the fused perimeter read are unavailable in this observation window.
The fused perimeter state is therefore `UNKNOWN`/partial; no all-clear or CALM verdict is asserted.
No routing, DNS, firewall, VPN, or other substrate was changed.

## Exact retry edge

Retry `mesh-wifi-motion --json`, `mesh-wifi-link --json`, and `mesh-perimeter` when the bounded
sensor commands return before timeout; retry DHCP observation when router lease access returns.
Until then retain UNKNOWN/partial coverage. The already-complete
`witness-sensor-visibility-20260916/refresh-perimeter-sensor-visibility` receipt remains the
prior observation and is not reused as this fresh read.

## Verification

The commands and exit codes above were run live from `/home/mesh-home/lte-workstation`.
