# Wake model evaluation fixtures — 2026-09-09

Status: fixture/baseline definition for `wake-model-eval-20260909`; no model is wired into live wake.

## Reproduction

```bash
python3 scripts/wake_eval_fixtures.py --test
python3 scripts/wake_eval_fixtures.py \
  --root /home/mesh-home/.mesh \
  --out docs/wake-model-eval-fixtures-20260909.json
```

The JSON artifact is metadata-only: it records hashes, counts, time bounds and derived-series definitions,
never raw board text. Re-run it immediately before each benchmark because `chat.log` and sensor tapes are
rolling live sources.

## Inputs and derived series

| input | usable fixture | leakage/privacy rule |
|---|---|---|
| `~/.mesh/sensor-tape.tsv` | one-hot rates for categorical state columns; `NOLOG`, `STALE`, and `UNKNOWN` are missingness indicators, not zero | preserve timestamp order and do not impute from future rows |
| `~/.mesh/power.log` | watts, core watts where numeric | parse only timestamped numeric fields; retain gaps |
| `~/.mesh/wifi-quality.log`, `wifi-rf.log` | signal dBm, link percent, retry/missed counters | state words are labels, not numeric measurements |
| `~/.mesh/package-power.log`, `body-power-readings.log`, `wifiscan.log` | candidate numeric logs, included only when regex extraction yields timestamps and values | source hash and parser version are mandatory |
| `~/.mesh/chat.log` | hourly `all_rows`, `[task]`, `[taking]`, `[done]`, `[fyi]`, `[alert]`, `[idle]`, `[dispatch]` counts | raw text is never copied into fixtures; marker counts are not semantic truth |

The checked-in manifest records the live source inventory and hashes. The available sensor tape currently
contains aligned categorical state data; numeric logs are sparse/heterogeneous, so each candidate series must
report its own count, cadence, missingness, and denominator instead of being silently merged.

## Split and baselines

Use one chronological split over the union time range: 70% train, 15% validation, 15% final test, with a
six-hour embargo on both sides of each boundary for the maximum planned forecast horizon. Fit normalization,
seasonality, thresholds and prompt-selection decisions on train only; use validation once for selection; keep
the final test untouched until the chosen configuration is frozen. A series with too few post-embargo test
windows is `UNMEASURED`, not a zero score.

Every TimesFM numeric forecast is compared with persistence, seasonal-24-hour, and train-only drift baselines.
Report MAE, RMSE, MASE where a nonzero seasonal denominator exists, empirical interval coverage/width, horizon,
valid windows, skipped windows and abstentions. A wake signal is useful only if it beats the strongest baseline
with a confidence interval and does not turn missingness into a prediction.

## Wake use cases and budget

1. Forecast near-term sensor/state-event rates as an advisory “review soon” hint; it cannot actuate, suppress,
   or replace existing watchdogs.
2. Forecast board activity (`task`/`done`/`alert` counts) to decide whether to pre-warm an offline evaluation;
   it cannot dispatch work.
3. Run a fixed bilingual structured-output fixture against Spark-X2.5-4B and MiniCPM5-2B for local-mind triage;
   JSON-schema validity, refusal/abstention, task accuracy and prompt leakage are measured separately.

Budget per run: TimesFM 8 GB RAM / 4 GB VRAM, 120 s cold and 30 s warm; local minds 12 GB RAM / 8 GB VRAM,
180 s cold and 60 s warm; 30 minutes wall time and 12 GB disk. Record peak RSS/VRAM, load time, steady latency,
tokens per second, model revision, runtime versions, and any OOM/timeout. Network is model-download-only.

## Artifact schema

`wake-eval-fixtures/v1` requires: creation time; repository revision; source paths, byte counts and SHA-256;
row counts and time bounds; parser/schema version; series definitions and missingness; split cutoffs and embargo;
seed; model IDs/revisions; baseline definitions; per-series metrics with denominators; resource samples;
failure/abstention counts; and license status. The manifest also explicitly states that raw chat text is absent.

## Model cards and license constraints

- [Google TimesFM 3.0 PyTorch model card](https://huggingface.co/google/timesfm-3.0-pytorch) and its
  [TimesFM Non-Commercial License v1.0](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE):
  evaluation/research is allowed; production, commercial use, commercial decision-making, distribution and
  commercial derivatives are not. This lane therefore treats TimesFM as offline research only.
- [XHToken Spark-X2.5-4B model card](https://huggingface.co/XHToken/Spark-X2.5-4B) and the
  [upstream Apache-2.0 license](https://github.com/XHToken/Spark-X2.5/blob/main/LICENSE): preserve license/
  attribution and check model-card custom-code/runtime requirements before deployment.
- [OpenBMB MiniCPM5-2B model card](https://huggingface.co/openbmb/MiniCPM5-2B) and its
  [Apache-2.0 license](https://github.com/OpenBMB/MiniCPM/blob/main/LICENSE): preserve license/attribution,
  and treat the card’s safety/accuracy disclaimer as a benchmark limitation, not a deployment guarantee.

These licenses do not authorize exposing private board or sensor data. Any later public artifact must use a
scrubbed fixture and retain provenance; this local manifest intentionally contains only metadata.
