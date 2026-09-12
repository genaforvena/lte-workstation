# 360M capacity ladder — blocked, 2026-09-12

## Decision

**BLOCKED before larger-model comparison.** The pinned 360M baseline is reproducible, but the
paired project-DNA evidence does not pass its evidence gate: its within-snapshot leakage control
fails (6 duplicate blobs in snapshot A; 19 in B), the exact-count retrieval answer is wrong, and the
genuine-update arm has no independent split or trained adapter. Do not treat these results as a
clean 360M comparison or substitute a larger model. No 1B/1.5B inference was run and no cost row was
fabricated.

## Gate evidence

- Baseline receipt: `/home/mesh-home/tiny-fleet/docs/task-receipts/tinyfleet-operator-ideas-verify-bbywvy-baseline-20260912.md`.
  It pins `StarpowerTechnology/BbyWVY-360m` revision `154a243ffa13d3259a824c40a23d709d3ea42fa7`,
  weights SHA-256 `3e26b40ed65c3fcd53e2930c38e3c9b9a5912389e0a6924f047cafa8eaa68c14`, and records a real
  inference smoke. This establishes baseline availability, not a passing paired-study gate.
- Paired artifact: [`../paired-project-dna/README.md`](../paired-project-dna/README.md), with raw
  outputs and machine-readable controls in that directory. Leakage is `fail`; exact-count base and
  retrieval controls do not recover the measured `1441 → 1867` / `+426` change; genuine update is
  blocked. The artifact explicitly calls this a blocked pilot.
- Therefore identical-prompt/snapshot/control/cost comparisons against larger models are deferred
  until the 360M evidence is repaired. No larger-model result can discharge the missing 360M gate.

## Current roster observed

Read-only checks on mesh-home:

- `mesh-model-resolve --json` exited 0. Its active text consumer is `room-wake` on `qwen2.5:3b`;
  its other rows are STT, vision, and TTS consumers. It does not declare an active 1B/1.5B code
  model. `mesh-model-watch` separately reported its resolver input unreadable at 08:54Z, so that
  cached watch line is not treated as the authoritative roster.
- `ollama list` includes `llama3.2:1b` (1.3 GB), but no 1.5B model. The Hugging Face cache includes
  `OpenBMB/MiniCPM5-1B`; no 1.5B model directory was present. These inventory entries do not by
  themselves verify the requested Linux-trained/code-model eligibility, and neither was run.

## Comparison columns

| Arm | Same prompts/snapshots/controls | Quality/delta | Cost/latency/memory | Verdict |
|---|---|---|---|---|
| Pinned BbyWVY-360M | Existing paired artifact only | Leakage fail; count delta missed | Baseline resource/latency receipt exists; paired cost comparison is incomplete | blocked |
| `llama3.2:1b` | not run | n/a | n/a | deferred |
| `OpenBMB/MiniCPM5-1B` | not run | n/a | n/a | eligibility unverified; deferred |
| 1.5B candidate | none in observed local roster | n/a | n/a | no candidate observed |

Next action: repair the leakage/independent-split evidence and rerun the 360M paired controls; only
then select a currently verified eligible larger comparator and execute the frozen comparison.
