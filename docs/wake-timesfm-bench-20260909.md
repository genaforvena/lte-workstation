# Wake TimesFM benchmark — 2026-09-09

Status: measured offline; no live wake wiring. Artifact: `wake-timesfm-bench-20260909.json`.

## Reproduction

```bash
/home/mesh-home/.venv-ai/bin/python -m pip install 'timesfm[torch]'
/home/mesh-home/.venv-ai/bin/python scripts/wake_timesfm_bench.py \
  --root /home/mesh-home/.mesh \
  --fixture docs/wake-model-eval-fixtures-20260909.json \
  --out docs/wake-timesfm-bench-20260909.json
```

Model: `google/timesfm-3.0-pytorch`, package `timesfm 3.0.1`, git revision
`18456be234a0c45f9540616b7a4c40e015daccb3`, CUDA on RTX 3060 12 GiB. The first cold
load measured 137.765 s (over the 120 s budget); the cached rerun loaded in 2.963 s.
Peak recorded RSS was 3044.3 MiB and CUDA allocated memory 1269.9 MiB.

## Final test results

Six-hour forecasts, chronological split and six-hour embargo from the fixture. `n` is the
number of scored hourly targets, not the number of windows.

| series | valid windows | TimesFM MAE / RMSE | strongest baseline MAE / RMSE | p10–p90 coverage | decision |
|---|---:|---:|---:|---:|---|
| chat all rows | 307 | 33.038 / 66.651 | persistence 32.470 / 66.573 | 0.765 | reject for wake signal |
| power watts | 55 | 1.803 / 2.517 | persistence 2.401 / 3.349 | 0.852 | retain offline candidate |
| package power watts | 0 | UNMEASURED | UNMEASURED | — | insufficient parsed fixture |

Warm forecast latency was 75–79 ms mean and below 98 ms p95 on the measured series.
TimesFM improved the validation and final-test power forecast over all three baselines,
but did not beat persistence on final-test chat activity. Coverage is empirical only and
does not establish calibrated uncertainty.

## Recommendation

Keep TimesFM offline research-only. It is a plausible advisory candidate for numeric power
series, subject to a larger live corpus and calibration check; do not wire it into wake or
use it to suppress/replace watchdogs. Reject it for chat-activity pre-warming on this run
because the untouched final test is slightly worse than persistence. The checkpoint is under
Google’s TimesFM Non-Commercial License, so this result does not authorize production or
commercial deployment: [model card](https://huggingface.co/google/timesfm-3.0-pytorch),
[license](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE).

## Verification

`python3 -m py_compile scripts/wake_eval_fixtures.py scripts/wake_timesfm_bench.py` — PASS.
`/home/mesh-home/.venv-ai/bin/python scripts/wake_eval_fixtures.py --test` — PASS.
Raw chat text is not copied into the result; only hourly counts are evaluated.
