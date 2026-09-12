# Tiny Fleet preflight environment correction — 2026-09-12

The behavior-controls receipt
`docs/tiny-fleet-artifacts-20260912/behavior-controls/README.md` (owner-authored task result at
09:09Z) described the system-Python preflight as if it described the training environment. That
was incorrect: it checked `/usr/bin/python3`, while the pinned BbyWVY baseline and its actual model
runtime use `/home/mesh-home/.venv-ai/bin/python`.

The corrected runtime preflight is
`docs/tiny-fleet-artifacts-20260912/paired-project-dna/runtime-preflight/preflight/preflight_20260912T091712Z.json`
(SHA-256 `c1cf4ff74970623e812ac15e49f73f7e3d3e2798c43102f378ebe876c9a54d70`). In that environment,
Torch 2.13.0+cu130, Transformers 5.14.1, PEFT 0.19.1, CUDA, and the RTX 3060 are present, so the
protocol's dependency/accelerator probe reports LoRA preflight `ready`. `bitsandbytes` is absent,
so QLoRA is not ready. This is a readiness probe only; no adapter was trained in the behavior step.

The paired-snapshot check then measured within-snapshot exact-blob duplicates (6 in A, 19 in B),
and 1,314 same-path identical blobs across snapshots. The repository/time evaluation therefore does
not provide a valid leakage-clean training/evaluation split. The genuine-update arm remains
BLOCKED; this is the corrected study verdict, despite LoRA dependencies being installed. No package
was installed and no model weights were changed.
