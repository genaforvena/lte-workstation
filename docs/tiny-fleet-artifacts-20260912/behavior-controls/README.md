# Tiny-fleet behavior controls and LoRA/QLoRA preflight

Run on 2026-09-12 after the frozen protocol, corpus fixtures, and structural/lexical
measurement steps completed. This receipt separates synthetic evaluator controls from the
local base-model diagnostic; neither is evidence of a trained adapter or paired temporal
snapshot result.

## Artifacts and verification

- `generative-controls.json` contains 11 bounded Ollama calls, full synthetic prompts and raw
  responses, response hashes, fixed generation options, model digest, and per-call timing.
- SHA-256: `43cdad09abede9cb42236f721bb3d724aa416fa22cd5c462ea72c2e40bd19656`.
- `bash tests/test-mesh-tiny-fleet-validation.sh`: exit 0. Offline smoke, preflight schema,
  blocked-LoRA contract, protocol mutation, fixture hashes, deterministic corpus lock, and
  mutable-ref red gate passed.
- `bash tests/test-mesh-tiny-fleet-evaluator.sh`: exit 0. Same-snapshot repeatability,
  swapped-label arithmetic, path-order invariance, leakage, and known synthetic mutation passed;
  changing the mutation file made the mutation control fail as required.

The evaluator reports `shuffled_conditioning=not_run` because it has no live model-conditioning
input. The separate local diagnostic used only synthetic text and the installed base model
`smollm2:135m`, digest
`9077fe9d2ae1a4a41a868836b56b8163731a8fe16621397028c2c76f838c6907`, with temperature 0 and
64-token output cap. Exact repeated prompts at seed 20260912 matched; seeds 11, 22, and 33 also
matched. Permuting file order changed the response hash, so order invariance failed for this
generation. The swapped-label prompt abstained. The model returned `UNKNOWN` for the injected
“bounded retry counter” change, so known-change recovery failed. It declined the unsupported GPU
model question, but hallucinated generic changes for both the no-context and unrelated-context
prompts. These are observed failures, not a scored model-quality estimate; no semantic evaluator
or acceptance threshold was supplied by the frozen protocol.

## LoRA/QLoRA arm and resource decision

The canonical `scripts/mesh-tiny-fleet preflight` artifact is
`preflight.json` (SHA-256 `3e3c4a534a629711726a1df5dc44e791ed1b9ebbeaa7004b5e06a3a5cad25d21`);
the original node-local output is `~/.mesh/tiny-fleet/preflight/preflight_20260912T090240Z.json`.
It reports LoRA/QLoRA `blocked`:
`torch`, `transformers`, and `peft` are all absent. `nvidia-smi` is present, which satisfies only
the accelerator-tool probe; it does not make the training stack ready. No weights were updated,
and no adapter or training artifact was produced. Prompt-only availability is not used as a
fine-tuning substitute.

At the local check, mesh-home had 31 GiB RAM with 13 GiB available, an RTX 3060 with 3,019 MiB
free VRAM before the diagnostic (2,510 MiB after), and 643 GiB disk free. It could run the small
base-model diagnostic, but no LoRA-specific VRAM minimum or fit result is established by the
protocol, and the fine-tuning dependencies are absent. Phaedra was reachable and had 1.3 GiB RAM
available, 156 MiB immediately free, no `nvidia-smi` command, and the same three Python dependencies
absent. The iMac's SSH host key could
not be verified; the Windows peer timed out on SSH, so neither is counted as an available training
slot. No peer configuration was changed and no package was installed.

Decision: keep LoRA/QLoRA blocked and do not launch a partial training attempt. Resource
reconciliation is owned here: recheck at the next queue turn (30-minute cadence) and select a node
only if its live evidence shows all three dependencies, a compatible accelerator, and sufficient
headroom; otherwise preserve the blocked state with refreshed evidence. This turn's small
control-only inference ran on mesh-home and did not consume a training slot.

## Scope

The protocol and corpus artifacts remain unchanged. The current corpus lock has one immutable
snapshot per repository, so paired temporal drift and downstream adapter comparison remain
unavailable. This receipt closes only the behavior-controls/preflight step; it does not claim a
trained model, successful known-change recovery, or completion of paired-project DNA controls.
