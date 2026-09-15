# Sense enrichment: webcam frame freshness in `mesh-light`

The webcam fallback already classified real frames and exposed `source_age_s` in JSON, but the
shared `.light-state` artifact omitted freshness. A consumer reading only that artifact could not
distinguish a current webcam substitute from a past one by its level and file mtime alone.

The webcam state line now appends `frame_age_s=N` after its existing source, scene, and spread fields.
This is the measured age of the frame file used for classification; it is named as frame age rather
than an independently timestamped sensor event. Existing leading fields and level vocabulary are
unchanged.

Live evidence on 2026-09-12:

```text
scripts/mesh-light --json -> rc=0
{"level":"DARK","lux":null,"ts":"2026-09-12T13:50:42Z","prev":"OFFLINE 2026-09-12T13:49:15Z","stable_s":null,"delta":null,"changes":null,"velocity":null,"smoothed":null,"change_class":"COARSE","direction":"FLAT","source":"webcam","coarse":true,"webcam_reason":"mean=76.3 median=32.0 stddev=85.9 p10=15 p90=247 spread=232 scene=localized","source_age_s":0,"webcam_spread_luma":232,"webcam_scene":"localized"}
~/.mesh/.light-state -> DARK|source=webcam|scene=localized|spread_luma=232|frame_age_s=0
```

Verification:

- The new state-artifact assertion failed first with the old line lacking `frame_age_s`, then passed
  after the write path was updated.
- `scripts/mesh-light --test`: pass, including a fresh real webcam frame and the regression checks.
- `MESH_CAM_FRAME=/definitely-missing-mesh-frame.jpg MESH_CAM_LIGHT_DIRECT=0 scripts/mesh-light --webcam`:
  exit 2, `n/a no-frame`, explicitly `NOT faked`.
- `bash -n scripts/mesh-light` and `git diff --check`: pass.
- No commit made.
