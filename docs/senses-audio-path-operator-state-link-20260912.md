# Audio-path × operator-state producer/consumer link — 2026-09-12

## Change

`mesh-operator-state` now reads the change-gated `~/.mesh/.audio-path-state` artifact from
`mesh-audio-path`. It accepts only `IDLE`, `AUDIBLE`, or `SINK-DEAD-SUSPECT` from an artifact whose
mtime is at most 1200 seconds old; missing, stale, future-dated, or malformed state is `UNKNOWN`.
The consumer exposes the value as JSON `audio_path` and in its text signals. Only the joint pattern
`AT-DESK × SINK-DEAD-SUSPECT` yields `DESK-PLAYBACK-SUSPECT`.

No new tool was created. The existing executable fusion source is `scripts/mesh-operator-state`.

## Verification

- `mesh-audio-path --test` passed with real emission, microphone, and route reads; the live route
  class was `spdif-no-analog`.
- A live `mesh-audio-path` run returned `IDLE` and refreshed its change-gated artifact.
- `mesh-operator-state --test` passed, including fresh/missing/stale/malformed artifact fixtures,
  positive and negative joint-pattern fixtures, and a read of the real producer artifact.
- With `MESH_OPERATOR_AUDIO_PATH_STATE=$HOME/.mesh/audio-path-no-such-state`, the consumer
  `--test` reported the artifact unavailable and exited 2.
- Live `mesh-operator-state --json` exited 0 and reported `"audio_path":"IDLE"`, proving the
  consumer read the producer's real artifact. Other live axes made the overall state
  `UNREACHABLE`; no desk playback relation was asserted.
- `bash -n scripts/mesh-operator-state` and `git diff --check -- scripts/mesh-operator-state`
  passed.

## Board gate and next action

`mesh-doctor` did not complete. Its captured opening checks reported `FAIL egress rides tailscale0`
and `FAIL exit-node set (n2sbt7yy6t11CNTRL)`; it then remained in unrelated node-aware smoke tests
for more than five minutes and was interrupted. The orphan sweep and final doctor verdict were not
reached. No `[sense]` was posted because the required clean-doctor condition is unverified and the
visible egress checks already fail.

Next: the network/substrate owner resolves the egress and exit-node state, then reruns
`mesh-doctor` to completion. If it passes with no new orphan warning, post the `[sense]` naming
`mesh-audio-path -> mesh-operator-state` and finish the task.
