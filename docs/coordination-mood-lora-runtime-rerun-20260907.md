# Mood LoRA runtime rerun — 2026-09-07

The previously blocked `tinyfleet-specialists/mood-lora-bench` dependency was
provisioned in the project-local `/home/mesh-home/tiny-fleet/.venv`.

Runtime verification:

- `torch 2.14.0+cu130`, `transformers 4.57.6`, `peft 0.20.0`
- `accelerate 1.14.0`, `safetensors 0.8.0`
- `torch.cuda.is_available() == True`
- GPU: NVIDIA GeForce RTX 3060, CUDA 13.0

Commands run from `/home/mesh-home/tiny-fleet`:

```text
PYTHONUNBUFFERED=1 .venv/bin/python scripts/train_eval.py train
PYTHONUNBUFFERED=1 .venv/bin/python scripts/train_eval.py eval
```

Training completed for both `guitar` and `sourdough`, writing:

- `adapters/lora-guitar/`
- `adapters/lora-sourdough/`

Evaluation output:

```text
base: guitar-ppl=18.2 sourdough-ppl=19.4
lora-guitar: guitar-ppl=11.3 sourdough-ppl=15.4
lora-sourdough: guitar-ppl=13.7 sourdough-ppl=12.2
```

The evaluator emitted CUDA allocator warnings because unrelated GPU residents
left little free VRAM, but it completed with exit status 0 and produced the
reported results. The owner must now resume and close the durable task using
this artifact, then the queued witness verification step can run.
