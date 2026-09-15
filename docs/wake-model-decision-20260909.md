# Wake model integration decision — 2026-09-09

Status: decision complete; no live wake wiring performed.

## Scope and live-state audit

The ledger was checked before execution. `wake-model-eval-20260909/decide-wake-integration`
was `open`; the fixture, TimesFM, and local-mind prerequisite steps were complete. The
instruction is therefore still live and correctly scoped.

Current implementation audit: `/home/mesh-home/finnegans-fake/wake/reflex.py` is the existing
`/wake` continuation reflex. Its pool is the existing Wake/English checkpoints and product
variants; it does not reference TimesFM, Spark-X2.5, or MiniCPM5. There is no integration point
to change safely from this evidence, so this artifact deliberately adds no wiring.

## Decision summary

| model | decision | evidence boundary | smallest reversible next step |
|---|---|---|---|
| `google/timesfm-3.0-pytorch` | keep as offline research only | Measured: useful on `power_watts`, not on chat activity; first cold load exceeded budget; non-commercial/non-production license | Generate a new dated offline benchmark after the corpus grows, with calibration and a holdout; keep output advisory in a separate artifact, never in the live reflex/watchdog path |
| `XHToken/Spark-X2.5-4B` | reject for this integration decision (UNMEASURED, not a quality claim) | No local weights/runtime; no prompt, latency, resource, bilingual, JSON, or isolation result exists | Download a pinned revision into an isolated cache and run the frozen local-mind fixture; do not register it with Ollama or wake until that artifact passes |
| `openbmb/MiniCPM5-2B` | reject for this integration decision (UNMEASURED, not a quality claim) | Requested 2B weights absent; only MiniCPM5-1B metadata was found; no runtime or task score exists | Download a pinned revision into an isolated cache and run the same frozen fixture; do not register it with Ollama or wake until that artifact passes |

No model is adopted. The local-mind rejects mean “not admissible for integration on this run,”
not “the model is bad”; benchmarking was blocked by availability and missing runtimes.

## Measured evidence

Artifacts and hashes at decision time:

```text
docs/wake-model-eval-fixtures-20260909.json
sha256 14a4a32c4e6d89bbc128b5bcad3837c292d27161194d75e45143d4687bb286fe
docs/wake-timesfm-bench-20260909.json
sha256 1fc18ecc17ac1858da48999cc9ab8bb3be4cb58a78d57ebee02b0dd0ab091124
docs/wake-local-minds-bench-20260909.json
sha256 4f78119ec8ed9c8021c7394d97022992f9610f05a0425f50bad6a155a7daba1f
```

TimesFM run: 6-hour forecast, chronological split with six-hour embargo, CUDA on RTX 3060
12 GiB, package `timesfm 3.0.1`, model revision
`18456be234a0c45f9540616b7a4c40e015daccb3`. First cold load: 137.765 s (over the 120 s
budget); cached load: 2.963 s; peak RSS 3044.3 MiB; CUDA allocated 1269.9 MiB; warm
forecast mean 75–79 ms and p95 below 98 ms on measured series.

Final-test results (the run’s reported denominators, not a general model claim):

* `power_watts`, 55 valid windows / 330 targets: TimesFM MAE/RMSE 1.803/2.517 versus
  persistence 2.401/3.349; p10–p90 empirical coverage 0.852. This supports further offline
  research, not an actionable wake signal yet.
* `chat_all_rows`, 307 valid windows / 1842 targets: TimesFM 33.038/66.651 versus
  persistence 32.470/66.573; coverage 0.765. It loses to persistence, so reject it for
  chat-activity pre-warming on this run.
* `package_power_watts`: 0 valid windows, `UNMEASURED`.

Local-mind run: `ollama list` contained neither requested model; cache inspection found no
Spark weights and only MiniCPM5-1B metadata; importing `torch`, `transformers`, `llama_cpp`,
and `vllm` failed. `nvidia-smi` reported an RTX 3060 with 12288 MiB and `free -h` reported
31 GiB RAM, but no model resource measurement may be inferred from capacity alone.

Failure modes carried forward: TimesFM is not calibrated by the empirical interval coverage,
small power/test sample limits generalisation, sparse package-power data is unknown rather than
zero, chat counts are not semantic truth, and cold-start latency can miss a wake budget. For
the local minds, the only honest output is unavailable/UNMEASURED; fabricating quality or
latency would turn absence into a score. Any future tool-calling result must also be treated as
untrusted text until schema validation, timeout, resource isolation, and fail-open wake behavior
are separately demonstrated.

## Exact reproduction commands

Fixture and benchmark artifacts:

```bash
python3 scripts/wake_eval_fixtures.py --test
python3 scripts/wake_eval_fixtures.py \
  --root /home/mesh-home/.mesh \
  --out docs/wake-model-eval-fixtures-20260909.json

/home/mesh-home/.venv-ai/bin/python -m pip install 'timesfm[torch]'
/home/mesh-home/.venv-ai/bin/python scripts/wake_timesfm_bench.py \
  --root /home/mesh-home/.mesh \
  --fixture docs/wake-model-eval-fixtures-20260909.json \
  --out docs/wake-timesfm-bench-20260909.json
```

Local-mind availability evidence:

```bash
ollama list
find /home/mesh-home/.cache /home/mesh-home -maxdepth 5 -type d \
  \( -iname '*Spark*' -o -iname '*MiniCPM*' -o -iname '*XHToken*' \)
python3 -c "import torch, transformers, llama_cpp, vllm"
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader
free -h
```

The exact frozen fixture and its future local-mind invocation contract are in
`docs/wake-model-eval-fixtures-20260909.md`; the local-mind artifact intentionally records
UNMEASURED rather than inventing a command that could not run. A future run must add the pinned
download command, revision, runtime versions, and resource sampler to its own dated artifact.

Verification performed for this decision:

```bash
python3 -m py_compile scripts/wake_eval_fixtures.py scripts/wake_timesfm_bench.py
/home/mesh-home/.venv-ai/bin/python scripts/wake_eval_fixtures.py --test
sha256sum docs/wake-model-eval-fixtures-20260909.json \
  docs/wake-timesfm-bench-20260909.json docs/wake-local-minds-bench-20260909.json
```

The first two checks passed; the final command produced the hashes above. No live wake wiring,
Ollama registration, download, or model change was performed.

## Licensing and deployment caveats

* TimesFM’s [model card](https://huggingface.co/google/timesfm-3.0-pytorch) and
  [TimesFM Non-Commercial License v1.0](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE)
  limit this checkpoint and derivatives to non-commercial, non-production purposes. The license
  also restricts commercial decision-making and distribution; it requires privacy, regulatory,
  and safeguards compliance. This rules out live wake deployment under the current evaluation
  terms even where the metric looks promising.
* Spark’s [upstream repository](https://github.com/XHToken/Spark-X2.5) states Apache-2.0.
  A later deployment still needs license/NOTICE preservation, pinned weights, dependency and
  custom-code review, prompt/data privacy review, and an isolated runtime.
* MiniCPM5-2B’s [model card](https://huggingface.co/openbmb/MiniCPM5-2B) states Apache-2.0.
  Preserve attribution and notices, review dependencies and the card’s safety/accuracy limits,
  and do not treat the upstream benchmark claims as evidence for this wake workload.
* Apache-2.0 does not grant rights to private board/sensor data. This evaluation’s fixture is
  metadata-only and contains no raw chat text or model weights.

## Final gate

The only permissible next integration is a reversible offline artifact-producing experiment:
TimesFM gets a larger-corpus/calibration rerun; each local mind gets an isolated pinned download
and the frozen fixture. Until those artifacts show a task-specific advantage, bounded resources,
valid structured output, and safe failure behavior, the live `/wake` reflex and watchdogs remain
unchanged.
