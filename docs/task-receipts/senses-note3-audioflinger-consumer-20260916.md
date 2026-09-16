# Senses receipt: Note3 AudioFlinger telemetry consumer — 2026-09-16

Implemented `scripts/mesh-note3-audioflinger`, a read-only consumer for
`adb -s 4d00553d61ab90d shell dumpsys media.audio_flinger`.

The consumer emits one timestamped JSON record with:

- `hardware_status`
- first output-thread `sample_rate`, `channel_count`, and human-readable `format`
- output-thread `track_count`
- `serial` and `source`

ADB loss, an empty dump, a missing capture, and missing individual fields emit `UNKNOWN`; an
unreadable live dump exits 2 and is still appended to the timestamped telemetry log. The live path
does not mutate the phone. `--parse FILE` supports durable capture replay without ADB, and `--test`
uses only private fixtures.

## Verification

`tests/test-mesh-note3-audioflinger.sh` passed. It covers all requested fields, missing fields,
missing capture, and UNKNOWN handling.

The supplied capture `/tmp/discover-note3-audioflinger-20260916.txt` parsed as:

```json
{"hardware_status":"0","sample_rate":"48000","channel_count":"2","format":"pcm16","track_count":"4"}
```

The live read at 2026-09-16T13:48:10Z encountered ADB loss and produced a fresh record in
`~/.mesh/note3-audioflinger.log` with every telemetry field set to `UNKNOWN`, exit 2. This is an
honest current failure state, not a green claim.

No scheduler or phone mutation was added. Retry after ADB transport recovery; run the consumer
again to append a fresh real record.
