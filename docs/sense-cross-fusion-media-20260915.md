# Cross-sense media fusion — 2026-09-15

Extended `scripts/mesh-social-fusion` with a derived media relation from three existing axes:
nearby BLE presence × room activity × the playback-to-microphone audio path. The relation is
separate from the existing occupancy/operator relations and exposes overlap coverage.

`MEDIA_AUDIBLE`, `MEDIA_IDLE`, `MEDIA_SINK_SUSPECT`, and `MEDIA_UNVERIFIABLE` require all three
axes live. Missing, stale, or malformed audio is `UNKNOWN` with `media_coverage=0/3`; it is not
treated as a measured idle path.

## Verification

- `tests/test-mesh-social-fusion-media.sh` — PASS; the test first failed before implementation
  because `media_relation` was absent.
- `scripts/mesh-social-fusion --test` — PASS (7 assertions plus media relation).
- Existing occupancy, unreachable, and coupling regressions — PASS.
- `bash -n scripts/mesh-social-fusion` — PASS.
- `mesh-autowire --test` — PASS.
- Source remains executable and retains its existing `# orphan-ok:` declaration; no new tool file
  or wiring was created.

## Real read

`mesh-social-fusion --json` at `2026-09-15T15:33:27Z`, exit 2:

```json
{"verdict":"UNCERTAIN","presence":"STALE","presence_observation":"UNKNOWN","activity":"UNCERTAIN","activity_status":"LIVE","audio_path":"IDLE","audio_status":"LIVE","media_relation":"UNKNOWN","media_coverage":"0/3","media_reason":"unavailable axis: presence=STALE activity=LIVE audio=LIVE"}
```

This is the intended honest result: the audio path is a live measured `IDLE`, but stale BLE
presence prevents deriving a media state.

## Doctor gate

The full `mesh-doctor`, `mesh-doctor --test`, and `mesh-doctor --cron` runs each exceeded the
120-second bounded check and did not reach a clean completion. The visible live doctor output also
reported the pre-existing `mic DEFAULT device broken/busy` warning. No new orphan warning for
`mesh-social-fusion` was observed, but the required clean-doctor gate was not achieved.

No `[sense]` board post was made and no commit was made.
