# Autopoiesis live review — viability is an admissibility test, not merely persistence

**Date:** 2026-09-09 · **Node:** mesh-home · **Mind:** genome · **Lane:** LITERATURE (live review)
**Area:** autopoiesis & the biology of cognition (Maturana/Varela), entered from a foundational idea
we may be applying too loosely.
**Arm:** treated (assigned)
**Target organ:** `scripts/mesh-chaos-emu` — assigned by coin at p=0.20, drawn uniformly from the
604 never-reviewed tools in the lane's denominator (Serrano et al., arXiv:2603.28336, Phase 4).
Not chosen by me or by the lane; not retargeted.

## Live sources actually read

The current formal continuation is **“Autopoiesis as viability-localized self-production in a topos”**
(*BioSystems*, 265, 105808, July 2026; PubMed record [42107485](https://pubmed.ncbi.nlm.nih.gov/42107485/)).
Its abstract makes the relevant move explicit: viability is an internal modality, production/repair
is represented with realization data, and production is constrained by an **admissibility predicate**.
The paper's AP1–AP4 axioms therefore do not call every persistent transition self-production; only
transitions that remain inside the viable, admissible regime count.

I also read Jiang et al., **“Autopoiesis: A Self-Evolving System Paradigm for LLM Serving Under
Runtime Dynamics”** (arXiv:2604.07144, 8 April 2026; [paper](https://arxiv.org/abs/2604.07144)).
It is a useful live counterexample: it calls continuous LLM-driven policy rewriting “autopoiesis,”
but its own architecture is a data plane plus an external control plane that searches and deploys
policies. Runtime change alone is not the Santiago-school claim of organizational closure. This is
the loose application worth correcting here.

The older grounding is Maturana & Varela, *Autopoiesis and Cognition: The Realization of the Living*
(1980): a system's response is determined by its organization and its coupling, not instructed by a
perturbation as if the environment supplied a command. The 2025 continuation **“Flowing boundaries in
autopoietic systems and microniche construction”** (*BioSystems* 254, 105477;
[DOI record](https://doi.org/10.1016/j.biosystems.2025.105477)) likewise distinguishes physical
boundaries from boundaries constituted by structural coupling.

## One concept we did not embody

**Viability-localized admissibility:** a transition must be checked against the organ's own viable
organization before it is admitted as a sustaining/meaningful transition. We have embodied retry
persistence in this tool — a keyed counter survives calls — but not the alphabet's admissibility:
`--fail-rcs 0` and `--rc 0` were accepted even though exit status 0 is success. That lets a nominal
“failure” transition silently bypass the retry loop. Persistence was being mistaken for a valid
failure state.

## One concrete application to the assigned organ

In `scripts/mesh-chaos-emu`, make the injected failure alphabet admissible: reject exit code 0 for
`--rc` and every member of `--fail-rcs`; only 1–255 can be injected as a failure. This is a narrow
application of the paper's viability/admissibility distinction: the emulator's viable failure state
must remain a failure in the consumer's exit-status semantics. The command's real success path stays
untouched.

Implemented in the source file (not `~/.local/bin/`), with two regression assertions in
`tests/test-mesh-chaos-emu.sh` for scalar and scripted code 0. No deployed copy was edited.

## Verification

```text
bash -n scripts/mesh-chaos-emu
bash tests/test-mesh-chaos-emu.sh
test-mesh-chaos-emu: PASS (scripted transient/terminal rc sequence and validation)
```

The artifact is intentionally uncommitted for the steward, per the genome charter.
