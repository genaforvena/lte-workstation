# ATProto query study admission — rejected

Date: 2026-09-08
Task: `study-atproto-query-20260908/admit-atproto-query`
Source ledger: `docs/plans/2026-09-08-study-atproto-ledger.tsv`

## Live-state audit

The task was open before execution (`mesh-task status study-atproto-query-20260908` showed
`[open] (1/1)`). Its instruction and acceptance predicate match the current source: the
repository contains the read-only `scripts/mesh-board-query` surface, but the study requires a
named downstream reader before admission.

The task was claimed at 2026-09-08T16:37:04Z and was active during this audit.

## Acceptance pricing

Sample query, run against the live text board through the installed/source-identical reader:

```text
mesh-board-query "task=study-atproto-query-20260908/admit-atproto-query" --json
```

Returned value: two records, the prior `[annotated]` record and the current `[taking]` record.
The same query returned `count1=2` and `count2=2` on immediate repeat. The installed command
and source both resolve to `scripts/mesh-board-query`, SHA-256
`589a865897b1b92b06f555adb72432992ae72cbabd81613574a24044a2a505db`.

| Acceptance component | Result | Evidence |
|---|---:|---|
| Read-only query against current board | PASS | two live JSON records returned |
| Deterministic result | PASS | immediate repeated counts: 2 and 2 |
| Named downstream reader | FAIL | `rg -n "mesh-board-query" scripts --glob '!mesh-board-query'` returned no callers |

Price: 2/3 components pass (66.7%). Overall admission is rejected because the missing consumer
is a required predicate, not an optional implementation detail. `mesh-board-query` itself is the
query surface under study, not a downstream consumer that gives it an operational use.

## Decision

Reject as an orphan proposal. No implementation or wiring task is handed to a steward. Reopen
only when an owner names a live board consumer and supplies its bounded acceptance predicate.
