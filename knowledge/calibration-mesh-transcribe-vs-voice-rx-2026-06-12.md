# Calibration: mesh-transcribe vs mesh-voice-rx (trusted ref)
Date: 2026-06-12
Idea: reflex-checks-reflex

## Setup
- **Trusted reference**: mesh-voice-rx — Telegram voice → ffmpeg → whisper → 3-stage filter → voice-in.log
- **New sense**: mesh-transcribe — arecord mic → whisper → inline filter → transcript.log
- Both use the same whisper.cpp binary (`~/.mesh/whispercpp/main`)

## Findings

### Model mismatch (ROOT CAUSE)
| Property | mesh-voice-rx | mesh-transcribe |
|---|---|---|
| Model | `ggml-large-v3-turbo.bin` (1.6GB) | `ggml-base.bin` (147MB) |
| Selection | `_best_model()` — auto-picks largest | `$TR_MODEL` env or hard-coded base |
| Quality | Excellent (Russian transcriptions clean) | Poor (hallucinated Japanese, gibberish) |

### Filter pipeline mismatch
| Property | mesh-voice-rx | mesh-transcribe |
|---|---|---|
| Filter | mesh-whisper-filter (3-stage: energy + boilerplate + repetition) | Inline regex (weaker, 15-line filter) |
| Hallucination catch | Comprehensive (27+ known hallucination strings) | Partial (6 Japanese phrases + basic repetition) |
| Energy gate | Yes (RMS silence detection) | No |
| Low-entropy gate | Yes (char entropy check) | Partial |

### Output quality comparison
- **voice-in.log**: 130 entries, all clean and accurate. Russian voice notes transcribed correctly.
- **transcript.log**: 3114 lines, majority are noise:
  - `ご視聴ありがとうございました` (hallucinated Japanese — whisper's #1 hallucination on silence)
  - `JANUJANUJANU` (single-word repetition, low entropy)
  - Gibberish in Russian/Turkish/Portuguese/Polish (background noise transcribed as speech)
  - Very few genuine transcriptions

### Calibration verdict
**mesh-transcribe is miscalibrated** — it uses a model 11x smaller than the reference and a weaker filter. The result is high noise, high hallucination, low signal. The tool works (whisper runs, audio captures), but the output is not actionable.

## Fix applied
1. Model: changed default from `ggml-base.bin` to `_best_model()` logic (matches voice-rx)
2. Filter: replaced inline filter with `mesh-whisper-filter --text` (3-stage pipeline)
3. Both changes bring mesh-transcribe to parity with the trusted reference

## Regression check
- `mesh-transcribe --test`: PASS (whisper + model + consent + audio tools)
- `mesh-whisper-filter --test`: PASS
- `mesh-voice-rx --test`: PASS
