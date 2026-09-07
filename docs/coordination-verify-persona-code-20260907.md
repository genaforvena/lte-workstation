# Persona/code specialist verification — 2026-09-07

The previously blocked chain step is now independently verified. The dedicated
runner at `/home/mesh-home/tiny-fleet/scripts/persona_code.py` no longer emits
an unconditional blocked result: it requires a pinned base revision, trains
each requested domain, saves a LoRA adapter, and evaluates the complete
cross-domain held-out matrix.

## Run

- Base: `HuggingFaceTB/SmolLM2-360M-Instruct`
- Revision: `a10cc1512eabd3dde888204e902eca88bddb4951`
- Device: CPU fallback; the live RTX 3060 was occupied by unrelated services.
- Persona: 5 epochs, losses `4.0064 → 1.2124`.
- Code: 5 epochs, losses `3.4421 → 1.3333`.
- Adapters: `adapters/persona-code-persona` and `adapters/persona-code-code`.
- Each domain has 12/10 train rows, 4 held-out rows, and 14 adversarial rows;
  raw inputs were not copied and the two NUL-corrupt operator-field lines were
  reported rather than sanitized.

Held-out perplexity from `runs/persona-code/eval-all.json`:

| model | persona | code |
|---|---:|---:|
| base | 15.10 | 191.60 |
| persona adapter | 6.82 | 213.45 |
| code adapter | 23.72 | 31.31 |

Both adversarial sets contain 14 cases with expected action `abstain`.

## Verification

```text
py_compile scripts/persona_code.py              PASS
python scripts/persona_code.py self-test        PASS
persona train                                  PASS
code train                                     PASS
cross-domain held-out eval                     PASS
```

Key artifact hashes:

```text
manifest.json   f3bb0c51d9ed6e30670c5fd6829b737b282854197fe8263e0f60bb5e9d7f0ae1
eval-all.json   171b7a526e57b6d11a929aa19c126c1536e44819aa416b44d6fc1fe7e9f1af2d
persona adapter 14f33b81f395b1af5a1f87a1a350e7494f675992fdf76b19b71023ebec75552e
code adapter    ec7d2b941f16ce62c971b80e3ef90b014646523a12f0facadb7d9a0d5eb8bbc0
```

The GPU-occupancy blocker is therefore resolved without stopping unrelated
services or substituting a smaller model. The next gate is the chain’s normal
close-integration step.
