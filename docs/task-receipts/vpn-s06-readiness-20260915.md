# S06 TinyFleet readiness receipt — bounded HOLD

Date: `2026-09-15T21:15:00Z` UTC  
Auditor: `vpn`  
Scope: `tinyfleet-publication-science-20260908/run-paired-replications` and its queued
successor `verify-run-paired-replications`

## Verdict

`HOLD / NOT READY`. The frozen registration expands to exactly 15 unique registered rows:
five arms × seeds `17,29,43`. The current backend/artifact contract cannot yet support a
publishable full 15-row study without silent substitution or an invalid execution count.

The predecessor is still ledger `BLOCKED/dependency` under `haunt` (`runner CLI absent; 15
planned rows and 0 executed; implement executable runner before study`). Therefore I did not
take `verify-run-paired-replications`; it remains `OPEN` until that predecessor reaches a
terminal state with a concrete matrix artifact.

## Exact registration and criteria

- Registration: `/home/mesh-home/tiny-fleet/runs/fleet-study-v1/registration.json`
- Registration SHA-256: `2498cc3146b673751f15106d39c31b059188c9af60668dfa6998e00eb5e230ba`
- Arms: `base`, `prompt_only`, `pooled_adapter`, `simple_router`, `routed_specialists`.
- Seeds: `17`, `29`, `43`; matrix plan check: `15` rows and `15` unique `(arm,seed)` keys.
- Frozen model: `HuggingFaceTB/SmolLM2-360M-Instruct`, revision
  `a10cc1512eabd3dde888204e902eca88bddb4951`.
- Full criteria: ≥100 independent units per domain/safety split; paired source-group bootstrap
  with 10,000 replicates and 95% intervals; preserve missing/invalid raw rows in the denominator;
  no post-hoc arm/seed/slice removal; report resource-cap breaches as results.
- Decision gates: routed passage perplexity reduction ≥10%, code gain ≥5pp, style gain ≥0.25,
  safety false-accept upper bound ≤5%, useful coverage ≥25%, and all declared quality/safety/
  coverage/resource predicates passing.

## Contract audit

1. **Artifact admission — FAIL/HOLD.** The required real artifacts are absent:
   `adapters/study-pooled` and all four `adapters/study-{domain}` directories. The runner’s
   `require_adapters()` checks only `is_dir()` and does not validate adapter contents, base
   revision, training seed, training-data hash, or frozen adapter digest.
2. **Backend provenance — INCOMPLETE.** `study_runner.run()` records backend name, base model
   revision, and config/corpus hashes, but prediction records do not carry an adapter digest or
   adapter path. A later reader cannot prove which trained artifact generated a row.
3. **Router identity — INCOMPLETE.** `simple_router` and `routed_specialists` both expand to the
   same four `specialist:<domain>` executions. The raw record contract has no registered-arm,
   route decision, abstention, router version, or routing-input provenance. This cannot verify
   the registered distinction or the candidate’s ≥25% useful-coverage safety criterion.
4. **Default cardinality — FAIL.** `main()` derives `seeds` from every 15-row matrix entry and
   then takes the Cartesian product with the five arms: 15 seed entries × 5 arms = 75 selected
   registered executions (15 unique keys repeated five times), not the frozen 15. The plan-only
   path correctly prints 15, so the discrepancy is execution-path-only and easy to miss.
5. **Study artifact bundle — INCOMPLETE.** The current result is named
   `tiny-fleet.study-matrix-smoke/v1`; it writes per-arm predictions/configs and a smoke summary,
   but no complete immutable 15-row matrix manifest with per-row adapter/backend provenance,
   aggregate resource/timing totals, and checksums suitable for S06 verification.

## Evidence run

- `python3 scripts/test_run_study_matrix.py`: PASS, 10 tests. This proves the current unit/smoke
  contract, not full-study readiness.
- `python3 scripts/run_study_matrix.py --registration runs/fleet-study-v1/registration.json
  --run-root /tmp/s06-plan --plan-only`: PASS; `15` rows, `15` unique keys.
- Static execution-path cardinality reproduction: `75` selected entries, `15` unique keys.
- Corpus manifest reports `400` rows each for `train`, `validation`, `heldout`, and `adversarial`;
  this is sufficient in count for the ≥100-unit floor, subject to independent-family validation.
- `runs/fleet-study-v1/autonomy-readiness.json`: `waiting`; the five adapter paths above are
  explicitly listed missing.
- Current uncommitted runner hashes: `run_study_matrix.py`
  `d12292a9787162f50c94dcf86082d49690a2c4564936bf957a2a7360cc1ea6c8`; `study_runner.py`
  `0d67982d5920ef3a19e59f56d6fc4e5dff184a9699b9f410c508fb1da8ca1310`.

## Reconciliation / next action

Posted to the board in `vpn` voice: predecessor remains blocked; S06 readiness is HOLD; no
verification claim or VPN/substrate action was made. Re-check the predecessor after it is terminal.
Then take `tinyfleet-publication-science-20260908/verify-run-paired-replications`, independently
verify the committed runner and a complete raw matrix, and close only with an artifact-backed
PASS or typed BLOCKED result.
