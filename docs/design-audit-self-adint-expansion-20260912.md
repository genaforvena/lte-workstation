# Self-ADINT expansion plan audit — 2026-09-12

## Verdict

The assigned audit task was live: `mesh-task check dispatch design-audit-task-sweep-20260907/plans-self-adint tg` returned eligible, and the task ledger showed this step open before it was taken. Its instruction is sound. The plan does not authorize active collection or irreversible operations, and its active-oracle gate remains closed in current state.

The plan's eight work packages are mapped below to existing completion evidence, an explicit operator/dependency block, or the still-open artifact-gated release task. Do not create duplicate implementation tasks for the two completed packages or the already-open release task. The existing three-task manifest had two unsafe ambiguities; those scopes are corrected in `docs/implementation-tasks-20260907.md`.

## Current state checked

- Plan: `docs/plans/2026-09-07-self-adint-expansion.md`, SHA-256 `73675dce754ad88bf00fcde8c945254157ecca27f1f02bc57e0f808e74e0c324`.
- Separate repository: `/home/mesh-home/self-adint`, HEAD `097b40f750aac248b4631a6364fea31708ed886d`. Its current dirty paths are `README.md`, `docs/INDEX.md`, `report.html`, and eight untracked `docs/task-receipts/unblock-adint-*.md` files. These are preserved; no writes were made to that repository.
- Current `data/study-status.json` says device entry points `MEASURED`, local receiver `MEASURED`, web passive lane `MEASURED`, device capture `BLOCKED_OPERATOR_EXPORT`, active oracle `NOT_ELIGIBLE`, seat `GATED_OPERATOR_GO`, and GAID reset `NO-BASIS`. The separate device-capture state is distinct from the older measured entry-point result.
- `data/operator-release-2026-09-07/decision-ledger.jsonl` has explicit device, seat, active-oracle, and GAID dispositions, but has no outbound-DSAR-letter row. The open release task must add that row and its exact per-step question/gate before it closes.
- No active bid, targeting query, injection, payment, outbound letter, or GAID operation is evidenced. The passive treatment/control replay is not an active persistence run.

## Work-package disposition

| WP | Current disposition | Existing task or block | Artifact gate / next action |
|---|---|---|---|
| 0. Reconcile implementation baseline | **Done** as the historical start-of-work reconciliation | `self-adint-expansion/baseline-and-receiver` completed by `adint` | `~/self-adint/docs/baseline-reconciliation-2026-09-07.md` records revision, dirty paths, checks, and status interpretation. Current head and dirty state are captured above for this audit; preserve them during the open release work. |
| 1. Close the device lane | **Blocked: operator input** | `self-adint-device-capture-export` was explicitly closed blocked | `~/self-adint/docs/device-capture-export-blocked-2026-09-07T0919Z.md` records the safe dry run and exact missing input: one complete PCAPdroid CSV, reachable Termux host/path, and explicit device label. Resume only on those inputs; do not substitute old PCAPs or report absence as no demand. |
| 2. Receiver gate | **Done** | `self-adint-expansion/baseline-and-receiver` completed | `~/self-adint/docs/receiver-red-before-green-2026-09-07.md` records the real mutation red/restored green and fresh corpus. Current `go test ./...` in `~/self-adint/receiver` passes (12 tests). |
| 3. Passive baseline/report contract | **Done for the passive browser lane** | `self-adint-expansion/passive-oracle-persistence` completed | `~/self-adint/docs/passive-oracle-persistence-2026-09-07.md` and `~/self-adint/data/passive-oracle-2026-09-07/` record schema 7, 3,987 request rows, 48 load rows, 116 ledger outcomes, source digest, egress report, and checksums. This evidence is browser-passive only; it does not discharge the device/seat payload gate in WP 4. |
| 4. Decide active-oracle eligibility | **Blocked: measured prerequisite absent** | Explicit state block `NOT_ELIGIBLE` | `oracle-verdict.json` has `active_result: null`; the missing prerequisite is measured device/seat payload evidence showing empty/hashed payload plus the independence assessment. Keep all active runs refused until that evidence exists. |
| 5. Measure persistence | **Blocked: WP 4 and exact intervention go** | Explicit dependency/operator block; no active successor is eligible | Existing events/runs and persistence report prove passive replay only. A future active schedule requires WP 4 eligibility and an exact operator go tied to that intervention. No retention estimate or active result may be claimed meanwhile. |
| 6. Handle operator-gated branches | **Open reversible preparation task; operations remain gated** | Existing `self-adint-expansion/operator-gated-release` task, owner `adint` | `~/self-adint/docs/operator-gated-release-2026-09-07.md` and its release bundle cover device, seat, active oracle, and reset. Add the missing outbound-DSAR-letter/mailbox row, exact question, evidence block, and explicit decision gate. Seat still requires per-step operator go; letters require the chosen jurisdiction/recipient and exact send go; reset remains `NO-BASIS` until a measured device baseline and exact reset go. |
| 7. Publish reproducibility and handoff | **Open artifact-gated task** | Same existing `self-adint-expansion/operator-gated-release` task, ordered after the passive task that is complete | The redacted release bundle, baseline lock, guide, HANDOFF, manifest, checksum list, and decision ledger exist. `adint-operator-release --test` and its bundle `sha256sum -c SHA256SUMS` pass. Still required: clean-tree reproduction of the non-private report, complete disposition/DSAR ledger, final status and task evidence, and `mesh-handoff adint`. The current dirty tree means clean reproduction is not yet demonstrated. |

## Manifest correction and verification

`docs/implementation-tasks-20260907.md` now allows the device lane to close with an explicit block instead of requiring a nonexistent JSONL, and defines the completed passive task as passive-only. Any active treatment/control run is a gated successor. The open release task now names the outbound-letter branch separately and states that preparation does not authorize an external action.

Read-only self-tests passed against the current separate repository:

```text
tools/adint-collect-passive --test       PASS
tools/adint-device-capture --test        PASS
tools/adint-study --test                 PASS
tools/adint-import-pcapdroid --test      PASS (0 failures)
tools/adint-aggregate --test             PASS (0 failures)
tools/adint-status --test                PASS
tools/adint-operator-release --test      PASS
receiver: go test ./...                  PASS (12 tests)
operator-release SHA256SUMS               PASS
```

These checks validate the safe code paths and existing release bundle; they do not create a device observation, make the oracle eligible, or authorize an active or external operation.

## Next action

`adint` should finish the already-open `self-adint-expansion/operator-gated-release` task after its current study step stabilizes: add the outbound-DSAR branch and exact operator question to the decision ledger, regenerate and verify the redacted report bundle from a clean tree, publish final status and `mesh-handoff adint`. Keep WP 4–6 operational blocks in force unless their stated evidence/go arrives.
