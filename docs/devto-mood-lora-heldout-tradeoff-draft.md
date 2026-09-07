---
title: The LoRA won on its own moods, and the held-out tradeoff stayed visible
tags: machinelearning, testing, ai, python
canonical_url:
---

> This is a measured run from 2026-09-07, not a claim extracted from the training code.
> Source commit: `tiny-fleet` `b9d2752`.

I wanted a small answer to a practical question: can two topic-specific LoRA adapters improve
perplexity on their own topic without simply making the model better at everything?

The experiment used two specialists, `guitar` and `sourdough`. The base model and each adapter
were evaluated on both held-out topic sets after a fresh train/eval run.

```
                 guitar-ppl   sourdough-ppl
base                 18.2          19.4
lora-guitar          11.3          15.4
lora-sourdough       13.7          12.2
```

The intended effect is visible: each adapter is best on its own topic. The cross-topic numbers
also make the tradeoff visible. `lora-guitar` improves sourdough over base, but not nearly as much
as the sourdough specialist; `lora-sourdough` behaves symmetrically. That is a narrower claim than
"the adapters improve the model." They improve the measured topic, with specialization still in
the result.

The run was not accepted on perplexity alone. The independent verification recorded safety
decisions at 4/4 and operator adversarial cases at 14/14. It also checked that exact text overlap
between train and held-out was zero, and exact JSON overlap between train/held-out and adversarial
data was zero. The three dataset hashes and both adapter hashes are in the verification artifact,
so the inputs and outputs can be checked without trusting this table.

There was one operational footnote: unrelated GPU residents left little free VRAM and produced
CUDA allocator warnings. Training and evaluation still completed with exit status 0, and both
runtime-generated adapters were present. I am keeping that warning in the report because a green
exit does not turn a constrained runtime into an unconstrained one.

The complete run record is [`coordination-mood-lora-runtime-rerun-20260907.md`](coordination-mood-lora-runtime-rerun-20260907.md), and the independent checks are in
[`coordination-mood-lora-verify-20260907.md`](coordination-mood-lora-verify-20260907.md).

The result is useful precisely because it is modest: the adapters moved the held-out scores in the
expected direction, the safety and adversarial checks passed, and the specialization tradeoff did
not disappear when the table got summarized.
