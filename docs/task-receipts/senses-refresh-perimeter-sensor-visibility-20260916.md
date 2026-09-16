# Senses receipt: refresh perimeter sensor visibility — 2026-09-16

Task: `witness-sensor-visibility-20260916/refresh-perimeter-sensor-visibility`
Owner: `senses`
Source ask: `witness-chat-range-review-near-60513-60582-review`

## Fresh live reads

Commands were run from `/home/mesh-home/lte-workstation` at 2026-09-16T02:34–02:35Z.

- `mesh-ambient-level --json` → rc 0: `MODERATE`, shared `overhear-tap@plughw:CARD=Camera,DEV=0`, rms `-26.4dB`, coverage `0.977`, age `4s`.
- `mesh-wifi-motion --json` → no result within the 20s bounded probe (`timeout`, rc 124). This is UNKNOWN/unavailable for this turn, not STILL; the attempted refresh did not produce a fresh motion verdict.
- `mesh-wifi-link --json` → rc 2: phone offline / SSH transport unreachable; no Wi-Fi-link sense.
- `mesh-gateway-identity --json` → rc 0: `STABLE`, gateway `192.168.8.1`, MAC `94:83:c4:68:07:66`, device `enp42s0`.
- `mesh-lan-newdevice --status` → rc 0: DHCP unavailable, LAN-side ARP fallback produced 9 current leases, all known against 16 baseline MACs.
- `mesh-perimeter` → rc 0: fused `CALM`; OUTSIDE `CALM` (HTTP reach observed), NETWORK `CALM` via ARP fallback with stable gateway, PHYSICAL `CALM` with 8 BLE devices and named devices.
- `mesh-perimeter --edge` → rc 0 with no emitted edge line (no fused verdict transition).

The perimeter result is partial in the epistemic sense: phone Wi-Fi-link is unreachable, Wi-Fi-motion did not complete a live read, and DHCP was replaced by lower-confidence ARP. No unavailable input was treated as a clear reading.

## Verification

All exited 0:

```text
tests/test-mesh-wifi-motion-test-real-read.sh
  mesh-wifi-motion --test live-artifact gate: PASS
tests/test-mesh-wifi-link-integration-slice.sh
  Wi-Fi integration: manifest, cadence owner, and real-read/unavailable result pass
tests/test-mesh-note3-sensor-family-integration-slice.sh
  Note 3 sensor family: manifest, compatibility paths, cadence owners, and serial real-read gates pass
```

## Delegation evidence

Delegated read-only audit to `senses-visibility-audit`. I inspected its worker turn and independently verified the task cache (`~/.mesh/task-chains/witness-sensor-visibility-20260916.json`), canonical references in `~/.mesh/chat.log`, and the live commands above. The worker made no claims, edits, board posts, or substrate changes.

## Retry edge

Retry `mesh-wifi-motion --json` when the node-side Wi-Fi scan can complete within its bounded probe; retry `mesh-wifi-link --json` when the phone SSH transport is reachable; retry DHCP observation when router lease access returns. Until then retain UNKNOWN/partial coverage.
