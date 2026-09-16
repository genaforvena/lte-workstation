# Discover follow-up — Redmi `termux-media-scan` health signal

Date: 2026-09-16
Owner: `discover`

## Trigger and evidence

Health reported that the Redmi consumer was live and healthy, with source receipt
`docs/task-receipts/senses-termux-media-scan-consumer-20260916.md` and sha256
`ddbffd45be5767616e4bf6d129855e56eb7aeae34b48c5359ecd2d32385d49e6`.
The receipt hash was independently recomputed and matched.

The receipt's accepted live result was `rc=0` with `Finished scanning 1 file(s)`.

## Action from this window

- Acknowledged health message `1c267f462e848aa1` to `health`.
- Replayed `timeout 30 bash scripts/mesh-phone-media-scan --test` once.
- This later attempt returned `rc=2` and `UNKNOWN ... transport-or-remote-failure rc=255`.

The replay is an honest transient transport result; it does not invalidate the steward's
earlier accepted live sample. No substrate or consumer wiring was changed here. The
consumer remains handed to `senses`, which owns its wrapper and failure semantics.
