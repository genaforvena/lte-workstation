# Local-mind benchmark — 2026-09-09

Status: **UNMEASURED**. This is a dated failure artifact, not a quality result.

The requested candidates, `XHToken/Spark-X2.5-4B` and `openbmb/MiniCPM5-2B`, were not locally
available. `ollama list` showed neither model. The Hugging Face cache contained only metadata for
`openbmb/MiniCPM5-1B` (9.7 MiB, no usable model weights for this task), not the requested 2B model,
and no Spark cache was found. System Python had no `torch`, `transformers`, `llama_cpp`, or `vllm`.

Therefore no prompt fixture was executed and no latency, tokens/s, RAM/VRAM, context, bilingual,
structured-output, refusal, or Ollama-isolation score is reported. Nulls in the JSON artifact mean
UNMEASURED, never zero.

Evidence commands and observed results:

```text
ollama list
# neither XHToken/Spark-X2.5-4B nor openbmb/MiniCPM5-2B
find /home/mesh-home/.cache /home/mesh-home -maxdepth 5 -type d \\
  \( -iname '*Spark*' -o -iname '*MiniCPM*' -o -iname '*XHToken*' \)
# only .../models--openbmb--MiniCPM5-1B
python3 -c "import torch, transformers, llama_cpp, vllm"
# ModuleNotFoundError: torch (and the other runtimes are absent)
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader
# NVIDIA GeForce RTX 3060, 12288 MiB, 9809 MiB
free -h
# 31Gi total RAM
```

The frozen fixture remains `docs/wake-model-eval-fixtures-20260909.json`; its local-mind budget is
180 s cold / 60 s warm, 12 GiB RAM, and 8 GiB VRAM. A future run must first record the exact model
revision, runtime versions, and download provenance, then execute the same bilingual structured
fixture. No live wake wiring is authorized by this artifact.

Artifact: `docs/wake-local-minds-bench-20260909.json`.
