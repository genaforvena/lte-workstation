# UVC metadata steward landing — 2026-09-11

## Decision

Steward the proven UVC metadata capability with the existing
`scripts/mesh-uvc-metadata` wrapper. It reads one real V4L2 `UVCH` buffer from
`/dev/video1`, writes `~/.mesh/uvc-metadata/latest.bin` atomically, and leaves
the previous artifact untouched when the endpoint times out or returns empty.

The wrapper was already present and wired into `mesh-organ-keepalive`; the
node-local organ declaration was stale. `uvc-metadata` was removed from
`~/.mesh/organ-retired`, then `mesh-card --refresh` restored it to the live
senses list.

## Verification

- `tests/test-mesh-uvc-metadata.sh`: passed. The real `--test` had seven
  bounded timeouts followed by one successful 968-byte read; negative missing
  device and wedged-endpoint cases also passed.
- Production wrapper read: passed, captured 7,986 bytes from `/dev/video1` at
  `2026-09-11T12:42:01Z` into `~/.mesh/uvc-metadata/latest.bin`.
- `scripts/mesh-organ-keepalive uvc-metadata`: passed through the real wrapper.
- `mesh-card`: now advertises `uvc-metadata` under `senses`.

The endpoint remains intermittent, so this is a live/partial organ, not an
all-clear claim. `mesh-card --refresh` returned 2 because of the pre-existing
`exit-node-lan` SWALLOWED invariant; that unrelated routing fault was not
changed.

