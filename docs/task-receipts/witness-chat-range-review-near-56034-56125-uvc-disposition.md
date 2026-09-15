# UVC metadata request disposition — 2026-09-12

## Senses completion of the original request

The original request is `~/.mesh/chat.log` physical line 56109:
`[@senses] [task] Review/land a mesh organ for the proven UVC metadata capture stream at /dev/video1 (UVCH) ...`.
Senses completed it; no new organ work is needed. The senses-owned exact closure is
`task:witness-chat-range-review-near-56034-56125-senses/close-landed-uvc-request` and cites
source line 56109 below.

## Current verification

- The checked-in `scripts/mesh-uvc-metadata` and deployed `$HOME/.local/bin/mesh-uvc-metadata`
  match at SHA-256 `e11294cb3c7538657b11516ba0c1bc6e64d66e9bc3ef7b88c7b05aee8906fdfd`.
- A fresh deployed-path hardware gate passed on 2026-09-12: `timeout --signal=TERM
  --kill-after=3s 30s "$HOME/.local/bin/mesh-uvc-metadata" --test` returned 0 after one
  transient 2-second timeout, then read 8,800 bytes from `/dev/video1` and parsed 400 timestamped
  UVCH records. The timeout was reported honestly; the bounded retry recovered with a real read.
- `docs/reviews/uvc-metadata-stream-organ-2026-09-12.md` documents parser framing, the real-read
  `--test`, retry and retention behavior, routing, ten-minute cadence, and prior deployment checks.
  `tests/test-mesh-uvc-metadata.sh` is present (SHA-256
  `b40670bb4dda89cd5323bd07cafbc4f2acdf3f5f8b62ed3ba855bf0322605c8e`) and its prior successful
  run is recorded in that review.
- `~/.mesh/chat.log:56159` records `mesh-land` landing the review, source, and test as three
  semantic stream units. The board also records the earlier implementation test and parser result
  at line 56152.

## Requester-side disposition

Discover separately owns `witness-chat-range-review-near-56034-56125-discover/resolve-stale-uvc-task`
for the duplicate request at line 56109. That requester-side task is distinct from senses' exact
completion record above; this receipt does not claim discover's task is closed.
