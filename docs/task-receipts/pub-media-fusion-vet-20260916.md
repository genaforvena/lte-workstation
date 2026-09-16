# Pub media-fusion vet receipt — 2026-09-16

## Source and provenance

- Source: `docs/sense-cross-fusion-media-20260915.md`
- Source SHA-256: `35e1f5e73894d483a9f46bd9939591ee0a06edb04f5118ee0268a2de19deaaf5`
- Repository HEAD observed: `bc22409c3e7f1ac60c0252a273acc08ea592635c`
- Worktree: dirty; unrelated staged and untracked changes were present.

## Evidence personally inspected

- `tests/test-mesh-social-fusion-media.sh` — exit 0; `ok: media fusion distinguishes audible playback from unreachable audio`.
- `scripts/mesh-social-fusion --test` — exit 0; `7 assertions + joint relation/coverage contract + media relation`.
- `bash -n scripts/mesh-social-fusion` — exit 0.
- Fresh `scripts/mesh-social-fusion --json` at `2026-09-16T01:42:40Z` — exit 0; live result was `media_relation=MEDIA_IDLE`, `media_coverage=3/3`, `audio_path=IDLE`, with `presence=9`, `ambient=MODERATE`, and `activity=UNCERTAIN`.

The source case also records the earlier honest boundary: stale BLE presence produced
`media_relation=UNKNOWN` and `media_coverage=0/3`; it did not convert missing evidence into idle.

## Disposition

**DEFER external publication.** The result is a credible internal measured case and the focused
behavioral checks pass, but the source records that full `mesh-doctor`, `mesh-doctor --test`, and
`mesh-doctor --cron` exceeded the bounded check, with a pre-existing mic warning, and no clean
commit/provenance snapshot is available. No pre-push board notice and no `mesh-devto-publish` call
were made. Revisit after a clean provenance choice and a completed doctor gate, while preserving
both the stale-input UNKNOWN result and a fresh covered live read.
