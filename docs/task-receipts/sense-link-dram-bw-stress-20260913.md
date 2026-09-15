# DRAM bandwidth × memory pressure link

Date: 2026-09-13. No commit.

## Change

`mesh-stress` now consumes the live `mesh-dram-bw` state artifact and current memory PSI, then
publishes the paired relation, both-axis values, and paired coverage in human and JSON output. The
relation is diagnostic only; it does not change the stress level. Missing, stale, malformed, or
uncovered DRAM state (or missing memory PSI) remains `UNKNOWN` with `0/1` pair coverage; machine
JSON and `--check` exit 2. The fusion reads `.dram-bw.state` rather than starting a second PMU sample.

## End-to-end evidence

- Producer artifact: `/home/mesh-home/.mesh/.dram-bw.state`, live cursor and covered interval. The
  paired run observed `pct=35.9`, `cov=93%(27rows)`.
- Consumer: `mesh-stress --json` returned exit 0 with
  `dram_memory_relation=LOW_THROUGHPUT_LOW_STALL`, `dram_memory_coverage=1/1 paired live sample`,
  and the producer's interval coverage. Current memory PSI was 0.01%; neither input alone produces
  this paired label.
- With `MESH_STRESS_DRAM_BW_STATE` pointed at a nonexistent artifact, `mesh-stress --json` emitted
  `dram_memory_relation=UNKNOWN`, `dram_memory_coverage=0/1 paired samples`, and exited 2.
- `scripts/mesh-stress --test` passed, including the four paired patterns and the unavailable
  producer case. `bash -n scripts/mesh-stress` and `git diff --check -- scripts/mesh-stress` passed.

## Doctor gate

`mesh-doctor` completed with **2 FAIL, 33 WARN**. The two failures are the existing egress path
using `tailscale0` and an exit node being set. The orphan scan reported
`+new:internet-test-hour.ps1`; that unrelated script is untracked in the shared worktree. The run
also reported 120 test temp leaks, 24 dead sign-vehicles, and other warnings. The doctor did not
pass cleanly, so the requested `[sense]` board line was not posted. No new tool file was created;
no autowire or chmod change was needed. No routing or exit-node state was changed.

Next action: after the existing doctor blockers are cleared, rerun `rtk proxy mesh-doctor`; only on
a clean pass, post `[sense] mesh-stress ↔ mesh-dram-bw: ...`.
