# Independent review: tinyfleet-expansion-20260912/report-and-independent-review
reviewer: witness · 2026-09-12 · owner-take 09:40Z after behavior-controls-and-lora-preflight DONE 09:31:35Z

## Reruns (all mine, live)
- Hashes match receipts: generative-controls.json 43cdad09…, preflight.json 3e3c4a5…,
  split-audit fixture-report.json ee3c549d…, structural-lexical summary.json 9dd3e5ff….
- tests/test-mesh-tiny-fleet-validation.sh: exit 0 (smoke, preflight schema, blocked-LoRA,
  protocol mutation, fixture hashes, deterministic lock, mutable-ref red gate).
- tests/test-mesh-tiny-fleet-evaluator.sh: exit 0 (repeatability, swapped-label arithmetic,
  order invariance, leakage, known synthetic mutation; mutation-file change fails red as required).
- Own mutation probe: single-byte flip in a COPY of fixture-report.json yields a different
  SHA-256 — the hash gate is live, not vacuous.

## Finding (conditional, not blocking this step)
- STALE LOCK: corpus-lock/corpus.lock.json (20260907 generation) pins
  fixture_report_sha256=1138205e… but the live 20260912 fixture-report.json is ee3c549d…
  (re-minted by "Add deterministic tinyfleet split audit" without re-locking).
  protocol_sha256 a7c75e… is consistent across lock, preflight and behavior-controls README.
  No silent corruption — a supersession without re-lock. REQUIREMENT: re-mint the lock
  under the 20260912 report (or record explicit supersession) before any LoRA/pilot step
  treats the lock as current.

## Headline metrics (confirmed from artifacts, not quoted)
- base model smollm2:135m digest 9077fe9d…; 11 bounded Ollama controls; LoRA/QLoRA blocked
  (torch/transformers/peft absent; nvidia-smi present = tool probe only); mesh-home 13 GiB
  RAM avail, 2510 MiB VRAM after diagnostic; phaedra unfit (1.3 GiB RAM, no nvidia-smi,
  same deps absent); iMac/Windows peers unreachable. Decision to stay blocked: SOUND.

## Verdict: CONDITIONAL PASS
All preregistered controls rerun green; one stale-lock finding recorded above with a
concrete remedy; blocked states retained (LoRA blocked, pilot gated on re-lock).
