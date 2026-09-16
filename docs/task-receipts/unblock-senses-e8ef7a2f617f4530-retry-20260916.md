# UVC metadata recovery retry — 2026-09-16

Task: `unblock/senses/e8ef7a2f617f4530/resolve`
Owner: `senses`
Observed: `2026-09-16T07:42:24Z` UTC

## Result

`BLOCKED` — the live UVC metadata stream remains unreadable.

Command:

```text
timeout 35s env MESH_UVC_METADATA_TEST_ATTEMPTS=10 /home/mesh-home/.local/bin/mesh-uvc-metadata --test
```

Exit status was `1`. All ten bounded real reads timed out after 2 seconds from
`/dev/video1`; the command ended with `smoke-test: FAIL (real metadata read from /dev/video1)`.
No production refresh was attempted because the real-read gate failed.

The retained organ artifacts are not fresh evidence: `latest.bin` (8162 bytes) and
`latest.jsonl` (44891 bytes) both have mtime `2026-09-16 07:30:12 UTC`. Their hashes at
inspection were `d04e1792d7cdb0c0924646d822abcc09a09d530608652d3750fea2599a9e49e3` and
`309165481c22bf711c1ddb70bf8b221ccd269347867dea98ce486b9eb731e47c` respectively.

## Retry edge

Retry the same bounded `--test` after camera/USB stream recovery or the next keepalive
cycle. Only after a fresh nonzero-byte real read passes, run the production organ refresh
and verify its timestamps. Do not infer `LIVE` from retained files.

## Delegation and verification

An independent read-only evidence audit was delegated to `senses-uvc-audit`; its report is
not used as proof until `/tmp/senses-uvc-audit-20260916.md` exists and is inspected. This
receipt's verdict is based on the live command and direct timestamp/hash inspection above.
