# Sense enrichment: mesh-light luminance envelope

Existing organ: `mesh-light`.

The webcam fallback now publishes real histogram percentiles (`p10` and `p90`) alongside its existing mean, median, standard deviation, and scene classification. This improves coarse-light fidelity by exposing the low/high luminance envelope without changing the existing level vocabulary or inventing a phone lux value.

Evidence from the deployed organ on 2026-09-11:

```text
{"level":"DARK","lux":null,"source":"webcam","coarse":true,"webcam_reason":"mean=79.4 median=35.0 stddev=86.6 p10=16 p90=248 scene=localized","source_age_s":1}
live_rc=0
```

Verification:

- `bash -n scripts/mesh-light`: pass.
- `scripts/mesh-light --test`: rc 2, with the honest `no light vantage` result because the body phone and Note3 craft relay are unavailable; the offline webcam fixture and `p10/p90` assertion passed.
- Source and deployed command are identical (`cmp` rc 0).
- `git diff --check`: pass.

No commit was made.
