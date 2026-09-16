# unblock/adint/288b9c87ec742046/resolve — 2026-09-16

## Result

BLOCKED: the required real UVC metadata read from `/dev/video1` still fails on the
fresh retry at 2026-09-16T09:03:55Z.

## Evidence

- Fresh command: `timeout 45s mesh-uvc-metadata --test`
- Fresh result: 10 metadata reads timed out after 2s; `smoke-test: FAIL (real metadata read from /dev/video1)`
- Fresh exit status: 1
- Prior captured output: `/tmp/adint-uvc-test-20260916T0829Z.log`
- Prior capture SHA-256: `4005b7a030fe0290d637dfe6d67452f791b29385d2a4b78af85d2f498c87d94b`
- Fresh terminal evidence: command output observed directly in the adint pane at
  `2026-09-16T09:03:55Z` (10 timeout lines, smoke-test FAIL).

No production refresh was attempted because its real-read prerequisite did not pass.

## Exact retry edge

After camera/USB stream recovery or the next keepalive cycle, rerun
`mesh-uvc-metadata --test`. Only after exit 0, run `mesh-uvc-metadata` and verify
fresh timestamps plus non-empty `latest.bin` and `latest.jsonl`.
