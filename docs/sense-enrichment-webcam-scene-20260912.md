# Sense enrichment: webcam scene quality in `mesh-light`

`mesh-light` already derived `scene=uniform|localized` and `spread` (`p90-p10`) from the webcam
frame, but consumers of `.light-state` could only see the level and source. The fallback now appends
`scene=` and `spread_luma=` to that artifact and exposes `webcam_scene` in JSON. Existing level and
source fields stay first; if the webcam reading lacks either measured quality field, the fallback
records no value and degrades as `webcam=unreadable` rather than filling a plausible default.

The `--test` hardware gate now counts a fresh, decodable webcam feeder frame as a real light
vantage, alongside phone lux and the Note3 relay. It reports the frame's measured classification;
with the feeder absent/stale/unassessable and both remote vantages unavailable, it exits 2.

Live evidence on 2026-09-12:

```text
scripts/mesh-light --json  -> rc=0
{"level":"DARK","lux":null,"source":"webcam","coarse":true,"webcam_reason":"mean=56.0 median=34.0 stddev=45.0 p10=20 p90=127 spread=107 scene=localized","source_age_s":1,"webcam_spread_luma":107,"webcam_scene":"localized"}
~/.mesh/.light-state -> DARK|source=webcam|scene=localized|spread_luma=107
```

Verification:

- `bash -n scripts/mesh-light`: pass.
- `scripts/mesh-light --test`: rc=0 with a live webcam artifact (`DIM`, `scene=uniform`, spread 140)
  while phone and Note3 were unavailable.
- `MESH_CAM_FRAME=/tmp/mesh-light-no-frame-fixture.jpg scripts/mesh-light --test`: rc=2, explicitly
  n/a because phone/Note3 were unavailable and the webcam frame was not assessable.
- The regression test first failed on a missing scene field, then failed on the missing-quality
  degraded path; after implementation the complete offline suite plus live gate passed.
- `git diff --check`: pass. No commit made.
