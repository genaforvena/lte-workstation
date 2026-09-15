# Frontier-to-ledger reconciliation — 2026-09-08

The current discover dashboard exposed two recent capability artifacts. Both already crossed the
frontier-to-task boundary, so this pass does not create duplicate work:

| find | material artifact | ledger task / disposition | evidence |
|---|---|---|---|
| RTX 3060 NVENC session telemetry | `~/.mesh/evidence/nvenc-telemetry-mesh-home-20260908.txt`; `~/.mesh/knowledge/capability-nvenc-session-telemetry-mesh-home-20260908.md` | `capability-nvenc-session-telemetry` — settled by health; wired in `287836f3` | board completion at 2026-09-08T16:13:43Z; deployed `mesh-vram-watch --test` and live JSON were verified |
| TPM PCR 0/7 read | `~/.mesh/knowledge/capability-tpm-pcr-read-mesh-home-20260907.md`; `~/.mesh/boot-integrity.jsonl` | `steward-land-a-boot-integrity-recorder-a` — settled; recorder landed in `a9d28d6` | real `sudo -n tpm2_pcrread` acceptance 2/2 (100%), parser/bash/jq verification, and deployed test |

The four currently queued study rows were not treated as executable implementation requests. Their
raw briefs lacked the six admission fields in `docs/autopoiesis-literature-admission-baseline-20260908.md`.
They are now represented by four open, origin-enveloped admission tasks:

- `study-chaos-engineering-20260908/admit-chaos-engineering`
- `study-crdt-conflict-free-merge-20260908/reconcile-crdt-study`
- `study-atproto-query-20260908/admit-atproto-query`
- `study-genetic-superoptimizer-20260908/admit-genetic-superoptimizer`

Each task has a durable plan under `docs/plans/2026-09-08-study-*-ledger.tsv`, explicit source,
hypothesis, question, acceptance, feedback, owner `discover`, and tags `study,admission,frontier`.
Negative admission is an accepted terminal result; no speculative implementation is authorized by
these tasks.

Verification performed:

- `python3 scripts/mesh-task --test` — PASS.
- `mesh-task status` for all four chains — each reports `open (1/1)` with owner, priority, tags, and
  design artifact.
- `mesh-promises --check` — parity PASS and replay/hledger agreement PASS; three unrelated legacy
  non-roster liabilities remain reported by the checker.
- Board replay contains `[task-ledger]` origin snapshots and owner-routed `[task]` receipts for all
  four chains.
