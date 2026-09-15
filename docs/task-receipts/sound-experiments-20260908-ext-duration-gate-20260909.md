# ext duration gate — measurement receipt

Task: `sound-experiments-20260908/ext-duration-gate`
Measured: 2026-09-09 UTC

## Live-state audit

The task was still open in the canonical board ledger at dispatch. The instruction matches the
current code:

- `scripts/mesh-random-track-pick:91-93` still admits audio only when `200_000 < size < 30_000_000`.
- `scripts/mesh-sound-reflex:363-368` still has no duration gate; its render budget is
  `max(300s, ceil(5s * source_duration))`.
- `scripts/mesh-sound-reflex:3096-3103,3118` bounds the child with `timeout "$CC"`, where `CC`
  is the render budget plus the live heavy-job queue budget.
- `scripts/mesh-records:63` retains the separate `MESH_REC_GRIND_REACH=900` pending-record reach
  window. This is a retention/shield interval, not evidence of render completion time.

## Corpus census

The live `~/.mesh/ext-inbox` contains 108 decoded MP3s, 1,508,485,172 bytes total, and 22 files
above the current 30 MB byte ceiling. `ffprobe` decoded all 108; 26 exceed 600 s and 24 exceed
900 s. This is inventory evidence only: the byte gate is still the admission gate, and the
out-of-band files were not rendered by this measurement.

## Completion evidence

The attached TSV joins the ext record duration in `~/.mesh/records.log` to the matching `src=ext/*`
start line in `~/.mesh/grainneukeln-attempts.log` and success line in
`~/.mesh/room-music-params.log`. It contains 14 paired completed ext renders:

- wall time: median 52.5 s, maximum 312 s;
- wall/source-second: median 0.252, maximum 0.417;
- no paired render exceeded the current `max(300, 5*duration)` render budget;
- the longest observed source was 1,290.21 s and completed in 312 s, below the named 900 s
  child/reach artifact, but this is not a ceiling test;
- no ext timeout completion artifact exists in the paired corpus. A timeout is therefore not an
  observed completion boundary, and queue delay is not separable from these wall stamps.

## Decision

Do not add a duration gate. The observed completed sample provides ample support for retaining the
current 5 s/source-second render budget, but it does not establish a real duration ceiling or a
named timeout failure artifact. Retain the current 200 KB–30 MB byte gate unchanged. A future gate
needs a controlled child-timeout artifact that records the timeout, source duration, recipe, and
whether rendering had begun; this receipt does not claim that evidence.

Verification: live board task lookup; current source inspection with numbered lines; 108-file
filesystem census; `ffprobe` decode census; timestamp join reproduced from the three live logs;
`git diff --check` and shell syntax checks after writing this receipt.
