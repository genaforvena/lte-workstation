# Health warning triage: e64b467cd85c10b8a9e8

Date: 2026-09-11
Owner: health

## Alert

At 2026-09-11 14:56:09Z, `mesh-home/mesh-chat-deliver@mesh-home` reported one
delivery failure for `@genome` to `witness`, window `5963795`, message
`25550bdbdce0a84b`, with `attempts=0`, `reason=age-expiry`, and `age-limit=900s`.

## Evidence

- The canonical board snapshot contains the exact alert at
  `~/.mesh/board-snapshots/chat-20260911T185138.926866487Z.log:46870`.
- The same target pair continued to produce age-expiry records shortly after
  the alert (`5b77dc798dad2e7c` at 14:58:07Z and `36c5c838276b68fd` at
  15:00:08Z), so this is part of a delivery/backlog condition rather than a
  single malformed message.
- `scripts/mesh-chat-deliver --test`: PASS.
- `bash tests/test-mesh-chat-deliver.sh`: PASS.
- `python3 tests/test-mesh-chat-deliver-attempts.py`: PASS, including distinct
  age-expiry classification.

## Disposition

Bounded historical warning; no safe local repair identified. The delivery
implementation and its terminal/expiry classification are healthy, while the
underlying witness delivery backlog remains a known blind spot/operational
condition. No routing, DNS, VPN, firewall, or other substrate state was changed.

