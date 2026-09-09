# Relevance realization & the frame problem — frame leakage in aggregate disk health

**Area:** relevance realization & the frame problem (Vervaeke)  
**Target organ:** `scripts/mesh-disk-health` (assigned by coin at p=0.20; not chosen by me or the lane)  
**Arm:** treated (assigned)  
**Date:** 2026-09-09 · **Window:** genome  
**Outcome:** APPLIES — one new frame-boundary mechanism landed in the assigned organ, uncommitted

## Live review and critique

The current failure mode I followed is **frame leakage**: a relevance mechanism can appear to solve
selection while its goal, ontology, and candidate features were already supplied by the model. That
is the circularity critique of the frame problem, not a claim that every precision-weighting system
is useless.

I read Darius Parvizi-Wayne, *What active inference still can't do: the (frame) problem that just
won't go away*, **Philosophy and the Mind Sciences 6 (2025), 1–26**, published 17 October 2025,
[doi:10.33735/phimisci.2025.12118](https://doi.org/10.33735/phimisci.2025.12118). The paper's
abstract argues that active-inference accounts remain explanatorily inadequate; its central detailed
objection is that the agent must already circumscribe goals, actions, and relevant features before
the optimization or heuristic can run. In other words, a formal relevance score can merely hide the
frame in its predefined ontology.

This is a useful critique of the Vervaeke-adjacent economic/predictive proposals because it gives a
failure test: **does the organ publish what it excludes, or does its output invite a consumer to infer
more than the sensor can see?**

For a live engineering comparison, I also read Huang, Zhang & Youcef-Toumi, *Perceive What Matters:
Relevance-Driven Scheduling for Multimodal Streaming Perception*, **arXiv:2603.13176** (13 March
2026), [full text](https://arxiv.org/abs/2603.13176). It operationalizes relevance as an information-
gain/cost reward over schedulable perception modules and reports lower latency, but also reports a
small recall reduction from imperfect information-gain estimation. That result makes the critique
concrete: a scheduler's selected feature set is an empirical frame with blind spots, not relevance
itself.

## What was not already embodied

The disk organ already had an honest **measurement** boundary in comments: whole devices only,
`/proc/diskstats`, with partitions excluded. It did not carry that boundary in its readings. Thus a
consumer could read `await_ms` and silently treat it as process-specific, partition-specific, or
causal evidence. Existing `UNKNOWN`/reset handling says when the counter is unavailable or rolled
back; it does not say what the counter fundamentally cannot discriminate.

The new concept is **published frame boundary**: the sensor emits its observed scope and its
non-observable exclusions with every output. This is deliberately a limitation artifact, not a new
health verdict and not a claim to have solved relevance realization.

## Concrete application landed

`mesh-disk-health` now adds this field to every JSON reading, including `--raw`:

```json
"relevance_frame": {
  "scope": "whole-device",
  "source": "/proc/diskstats",
  "excludes": ["partitions", "processes", "causes"]
}
```

Human-readable output carries the same frame. The exclusions are exact for this organ: its counters
are aggregate whole-device counters, so they cannot attribute an interval to a partition or process,
or explain why latency changed. Consumers can now refuse an over-broad inference or route a causal
question to a different organ. This is the one application; no silent retargeting was made.

## Verification

The source's `--test` was extended first with a fixture assertion for the frame field. Before the
implementation it failed with:

```text
smoke-test: FAIL (raw reading omitted its relevance frame boundary: ...)
```

After the implementation:

```text
smoke-test: ok (field-index incl. discards-mislabel trap + whole-disk-vs-partition filter x2 + no-whole-disk-reject + live real-read gate, dev=nvme1n1)
```

Additional checks passed:

```text
bash -n scripts/mesh-disk-health
MESH_DIR=<temporary> bash scripts/mesh-disk-health --raw --json
```

The live JSON probe returned both `nvme1n1` and `nvme0n1`, each carrying the frame object. Changes
remain uncommitted in the genome source tree for the steward to land.

## Sources

- [Parvizi-Wayne (2025), *What active inference still can't do*](https://doi.org/10.33735/phimisci.2025.12118)
- [Huang, Zhang & Youcef-Toumi (2026), *Perceive What Matters*](https://arxiv.org/abs/2603.13176)
- [Jaeger et al. (2024), *Naturalizing relevance realization*](https://doi.org/10.3389/fpsyg.2024.1362658) — background statement of the non-computational/circularity challenge
