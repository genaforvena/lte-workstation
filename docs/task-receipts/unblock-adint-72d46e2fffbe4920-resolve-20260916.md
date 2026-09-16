# unblock/adint/72d46e2fffbe4920/resolve — 2026-09-16

## Result

BLOCKED: the required real UVC metadata read from `/dev/video1` remains
unreadable. No mesh-owned repair is safe while the camera/USB stream is not
producing a buffer.

## Evidence

- Owner eligibility check: `mesh-task check dispatch unblock/adint/72d46e2fffbe4920/resolve adint` — exit 0.
- Owner take: `MESH_TASK_ACTOR=adint mesh-task take unblock/adint/72d46e2fffbe4920 resolve` — `already active`, exit 0.
- Device presence: `/dev/video1` exists as `crw-rw---- root:video` (mtime `2026-09-16 05:47 UTC`).
- Command: `timeout 45s mesh-uvc-metadata --test`
- Started: `2026-09-16T08:41:19Z` (window-local execution)
- Result: ten metadata reads each timed out after 2s; `smoke-test: FAIL (real metadata read from /dev/video1)`.
- Exit status: 1.

The device node's presence is not evidence of a readable stream. No
production refresh was attempted because the real-read prerequisite failed.

## Exact retry edge

After camera/USB stream recovery or the next keepalive cycle, rerun
`mesh-uvc-metadata --test`. If it exits 0, run `mesh-uvc-metadata` and verify
fresh organ timestamps plus non-empty `latest.bin` and `latest.jsonl` before
resuming the dependent task. Until then this remains a capability block, not an
operator-approval block.
