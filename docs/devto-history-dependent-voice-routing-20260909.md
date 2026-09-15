---
title: A Failed Voice Path Should Change the Next Call
tags: devops, ai, automation, observability
canonical_url:
---

Our local voice reflex had a sensible routing rule: when the workstation was occupied and the
event was proven, deliver it locally. Then the local TTS engine failed.

The next proven event met the same predicates and tried the same broken path again. The rule was
right for the current state and still wrong for the next decision, because it had forgotten what
had just happened.

This is a small failure, but it is a useful boundary for systems that claim to adapt: a detector
that remembers nothing cannot change its behaviour because of experience.

## The measured change

On September 9, 2026, I reviewed and tested a change to `scripts/mesh-say`. Before it landed,
`--deliver` routed from instantaneous `OCCUPIED × PROVEN` state. A failed local TTS attempt did not
become input to the following delivery.

The new path records a real local TTS failure in `$HOME/.mesh/mesh-say-coupling` (or the path in
`MESH_SAY_COUPLING_FILE`). For the next 300 seconds, a later `OCCUPIED + PROVEN` event is sent
through `mesh-voice-tx` instead, and the output identifies the decision as
`coupling=quarantined`.

That is not a permanent preference and it is not a global routing change. It is a bounded memory
of one failed interaction with one organ.

## The release condition matters

The marker is cleared only after a later local delivery is proven. Expired or unreadable state is
treated as no memory. Ambient non-`--deliver` speech is unchanged.

Those details keep the adaptation from becoming a second outage. A stale marker must not quarantine
local voice forever, and a failed read of the marker must not manufacture a confident routing
decision.

## Why I call this structural coupling

The useful idea from the autopoiesis literature is not the label. It is the mechanism: a system's
history can reorganize how later perturbations are metabolized. Wong et al. describe learning as a
history-dependent change that modifies responses to future perturbations ([A Biological Learning
Theory](https://link.springer.com/article/10.1007/s10956-026-10340-6)). Heylighen and Busseniers
connect resilience to compensation selected for the particular perturbation
([Modeling autopoiesis and cognition with reaction networks](https://doi.org/10.1016/j.biosystems.2023.104937)).

The workstation implementation is much smaller than those theories, but the operational test is
clear: cause a local TTS failure, observe the next proven event take the alternate route, then
observe a proven local delivery release the quarantine.

## Verification

The case and its evidence are recorded in
[`docs/autopoiesis-literature-mesh-say-20260909.md`](https://github.com/mesh-home/lte-workstation/blob/main/docs/autopoiesis-literature-mesh-say-20260909.md).
The measured checks were:

```text
bash -n scripts/mesh-say
scripts/mesh-say --test
smoke-test: ok (... history-dependent coupling quarantine/release ...)
```

The point is modest: if a failed attempt should affect the next attempt, write that history at the
source and make both the quarantine and the release observable. Otherwise the system is not
adapting; it is merely repeating a correct rule against a changed world.
