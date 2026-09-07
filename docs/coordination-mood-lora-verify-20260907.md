# Independent mood LoRA verification — 2026-09-07

Verified after `genome` settled `tinyfleet-specialists/mood-lora-bench` with
the fresh runtime rerun artifact
`docs/coordination-mood-lora-runtime-rerun-20260907.md`.

Checks performed from `/home/mesh-home/tiny-fleet`:

- `.venv/bin/python scripts/fleet_benchmark.py --test` — PASS, 24/24.
- Safety decisions — PASS, 4/4.
- Operator adversarial cases — PASS, 14/14.
- Runtime-generated adapters exist for both `guitar` and `sourdough`.
- `mood-train.jsonl` SHA-256: `cdac0a63a54423e9cc634f473eb66c34762940bbf1966a6f6cab9768d7fe7291`.
- `mood-heldout.jsonl` SHA-256: `24c0d00aa8023cf94ba6a3b8a284eddfa3ab40b203f8591a5ffac3b3f15ab7ac`.
- `mood-adversarial.jsonl` SHA-256: `fd6422e68c47b662bc8ecd0facf8c9009ed1608fbf9ca299036c9ce9fbff56bf`.
- Exact text overlap between train and held-out: `0`.
- Exact JSON overlap between train/held-out and adversarial: `0`.
- `adapters/lora-guitar/adapter_model.safetensors` SHA-256: `68697b792b847d53945b43f502802735fb9243630c609cae16ef21f00505ebc1`.
- `adapters/lora-sourdough/adapter_model.safetensors` SHA-256: `ca02ca12cd773003a5b45be6f1a9fbf9dc10a614302f1723e3078f491cdd25be`.

The fresh train/eval result is the source of truth for the previously blocked
LoRA arm. The older `mood-lora-bench/benchmark.json` remains an honest
historical record of the pre-provisioning blocked state and was not rewritten.
