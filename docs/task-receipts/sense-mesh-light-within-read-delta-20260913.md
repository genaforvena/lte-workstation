# Sense enrichment: mesh-light within-read delta

Date: 2026-09-13  
Sense: `mesh-light`

`mesh-light` already requested two `tmd2755_l` samples and classified from the later valid sample,
but discarded the earlier sample. The phone tier now retains their signed difference as
`sample_delta_lux`, an additive short-interval signal distinct from the existing between-run
`delta` and `velocity`. The existing latest-sample classification is unchanged. The new field is
emitted in phone JSON/text and appended to `.light-state`; beacon and webcam tiers omit it because
they do not produce a phone sample pair.

## Verification

- `bash -n scripts/mesh-light`: pass.
- `scripts/mesh-light --test`: pass. The parser fixtures assert both rising (`250|250`) and falling
  (`125|-275`) pairs; the JSON emitter asserts `sample_delta_lux`; the live phone gate now validates
  the same pair format when the phone is reachable.
- The test also produced a real live webcam frame: `DARK`, median luma 17, spread 3, uniform scene.
- `scripts/mesh-light --json`: exit 0 with a fresh real webcam artifact:
  `{"level":"DARK","lux":null,"ts":"2026-09-13T02:07:07Z","prev":"DARK","stable_s":null,"delta":null,"changes":null,"velocity":null,"smoothed":null,"change_class":"COARSE","direction":"FLAT","source":"webcam","coarse":true,"webcam_reason":"mean=17.2 median=17.0 stddev=2.1 p10=16 p90=18 spread=2 scene=uniform","source_age_s":1,"webcam_spread_luma":2,"webcam_scene":"uniform"}`

The live run used the webcam tier, so it correctly emitted no phone `sample_delta_lux`. This verifies
that the normal path still yields a real, fresh artifact without pretending webcam luma is phone lux.
The phone is currently unreachable on this node; the live phone-pair branch remains to be verified
when reachability returns. No commit was made.

## Follow-up: varied webcam scenes

The webcam scene field previously called every non-localized frame `uniform`. A broad high-contrast
scene can have balanced mean and median, so that rule hid visible variation. The classifier now
labels such a frame `varied` when its robust p90-p10 luma spread reaches the corpus-calibrated
threshold of 100; the coarse light-level decision remains median-based. Calibration used 32 live
rows: the highest low-spread row was 77 and the lowest high-spread row was 140, with eight earlier
high-spread rows labeled uniform.

Verification on 2026-09-13: `scripts/mesh-light --test` passes its balanced-scene regression and
produces a fresh webcam frame (`scene=uniform`, spread 99), correctly below the varied threshold.
The balanced high-contrast fixture is classified `varied`, and the JSON fixture carries
`webcam_scene=varied`. The missing-frame path exits 2 without fabricating a reading. An earlier live
frame at 13:29Z measured spread 148 and was classified `varied` (board artifact at
`~/.mesh/chat.log`, row 59229). The phone sample-pair arm remains unavailable because the phone is
unreachable; its parser, signed rise/fall, JSON, and state-format fixtures pass in the same full test.
