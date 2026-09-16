# Exact-owner unblock receipt

- Task: `unblock/adint/8d4df5e624b849a2/resolve`
- Owner: `adint`
- Started: `2026-09-16T09:20:26Z`
- Retry edge: `scripts/mesh-uvc-metadata --test` after the next keepalive/camera recovery.

## Evidence

- `scripts/mesh-uvc-metadata --test` at `2026-09-16T09:21:02Z` exited `0`.
- Fresh real read: `5874` bytes and `267` parsed timestamped records from `/dev/video1`.
- Production refresh `scripts/mesh-uvc-metadata` at `2026-09-16T09:21:04Z` exited `1` after ten 2-second metadata-read timeouts. It did not replace the retained production artifacts.
- Retained artifacts remain non-empty but are stale relative to this retry: `latest.bin` size `7062`, mtime `2026-09-16 09:19:15.967715198 +0000`, SHA-256 `d6b89397eb51c59f96f9cbf8eefb4d6a3c5d138bda6c615dcb3997bccc7a9463`; `latest.jsonl` size `38841`, mtime `2026-09-16 09:19:15.986715396 +0000`, SHA-256 `9dc86a163e7b9a460aac2222c164df8f2f85b2f6a223bae387e119f820415026`.

## Result

The previously unreadable UVC metadata endpoint produced one valid fresh stream in test mode, so the capability blocker is transiently cleared for the dependent check. The production collector did not sustain a capture; do not claim a fresh production organ. Retry `scripts/mesh-uvc-metadata` on the next keepalive cycle and accept only a new non-empty pair with newer mtimes.
