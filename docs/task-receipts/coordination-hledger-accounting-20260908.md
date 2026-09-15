# Coordination hledger accounting — live reconciliation checkpoint

Task: `coordination-hledger-plan-20260908/accounting-coverage`  
Owner: `genome`  
Observed: 2026-09-12 01:39 UTC  
Source cutoff: latest `spend.log` TURN at `2026-09-12T01:39:12Z`  
Journal watermark: `2026-09-12T01:19:01Z`

## Current evidence

- `rtk proxy bash tests/test-mesh-labor-reconciliation.sh` passes its isolated cases for concurrent
  overlapping feeders, a balanced missing transaction, a balanced duplicate transaction, and a
  delayed completion behind the watermark.
- `rtk mesh-labor --check` exits 1. hledger parity passes, but exact source-window reconciliation
  reports 8641 source TURN and 8257 journal TURN (difference 384), across 574 feed windows. The
  current partition is 370 pre-inception and 14 not-yet-fed TURN, with zero documented corrections,
  two duplicate-feed TURN, two missing-feed TURN, zero interval-overlap rows, and three unexplained
  source/journal groups. The 370 + 14 partition explains the headline 384 only; it does not discharge
  the additional group mismatches.
- The three remaining mismatches are untagged groups:
  - `2026-09-06T12:19:01Z..2026-09-06T12:29:06Z`, `openai/witness`: source 2, journal 4.
  - `2026-09-08T19:19:01Z..2026-09-08T20:19:01Z`, `openai/wake`: source 4, journal 3.
  - `2026-09-11T20:19:01Z..2026-09-11T21:19:02Z`, `openai/health`: source 20, journal 19.
- Raw `spend.log` inspection confirms these groups have respectively 2, 4 and 20 source TURN rows,
  all without `task:` tags. The matching journal feed transaction records only the aggregate
  4/3/19 TURN by provider/window; it cannot identify which source event was duplicated or omitted.
  The opposing deltas (+2, -1, -1) net to zero, so the headline 384 difference alone hid them.
- Historical source for the Sep 6 witness delta is now located. `~/.mesh/labour/2026.journal` has
  a separate `Codex root-identity migration correction` transaction immediately after that feed,
  reversing 2 TURN; its comment says it reverses three title-generation events booked at 12:29,
  including root `eb08bcf6` omitted by the old minute-resolution watermark. The raw window has two
  `turn witness` rows (12:26 root `d552c556`, 12:29 root `eb08bcf6`); their turn-result artifacts
  say they restored prior results without additional work. Thus feed 4 minus correction 2 equals
  source 2 for this group. The correction is real but the reconciliation still reports this group
  unexplained and its “documented corrections” count as zero, so the audit is failing to associate
  the historical correction with its source window. The correction's prose says three events while
  its posting is -2 TURN; preserve that distinction and do not infer a third source TURN.
- Explicit task attribution is 313/8641 TURN (3.6%), across 46 task IDs; 8328 source TURN remain
  untagged/unknown. The journal has 313 explicitly tagged TURN.
- `rtk mesh-ledger --check` passes (parity and 682 non-overlapping feed windows).
- `rtk mesh-promises --check` exits 1: its claims agreement is 145 replayed versus 0 journaled;
  promises balance and match at 268. This is outside this step's labor writer and remains visible.

## Next action

Trace the Sep 8 wake and Sep 11 health groups in the same way; for Sep 6, fix or classify the
reconciliation's correction recognition so the verified -2 TURN journal correction discharges its
source window. Keep unknown rows explicit; do not force totals to agree with guessed bookings.
Rerun the focused fixture and all three checks after any warranted fix, then query one completed and
one open task by explicit task ID.

## 2026-09-12 continuation and disposition

The raw source rows were traced against the exact feed windows, with event IDs retained as the
independent identity evidence:

| source window | source events | journal feed | disposition |
|---|---:|---:|---|
| Sep 6 12:19:01–12:29:06Z, `openai/witness` | 2 (`d552c556`, `eb08bcf6`) | 4, followed by a separate `-2 TURN` correction | correction is supported: the transaction comment identifies the old minute-resolution watermark and root `eb08bcf6`; net 2 matches the source. Its prose says “Reverse 3 … events” while the posting is `-2 TURN`; the posting, not prose, is the amount. The checker does not read the correction transaction, so its `documented_corrections=0` and 2-vs-4 mismatch are a parser/classification limitation, not an unexplained source loss. |
| Sep 8 19:19:01–20:19:01Z, `openai/wake` | 4 untagged events at 19:19:04, 19:49:07, 20:03:12 and 20:19:01Z | 3 TURN | 1 source TURN absent from the aggregate feed; no correction transaction found. Keep as a real reconciliation failure; event attribution remains unknown. |
| Sep 11 20:19:01–21:19:02Z, `openai/health` | 20 untagged events from 20:20:50 through 21:19:02Z | 19 TURN | 1 source TURN absent from the aggregate feed; no correction transaction found. Keep as a real reconciliation failure; event attribution remains unknown. |

At the source check cutoff `2026-09-12T01:53:29Z`, `spend.log` contained 8,654 TURN and the feed watermark
was `2026-09-12T01:19:01Z`. The helper reported 8,257 windowed journal TURN, difference +397, partitioned as
370 pre-inception and 27 not-yet-fed. The actual hledger labour balance is 8,255 because it also includes
the -2 historical correction. There were 314/8,654 explicit source task tags (3.6%), 8,340 untagged/unknown,
and 46 task IDs. The correction changes the net ledger balance but does not explain either of the two
currently missing source rows.

Focused verification at this continuation:

- `rtk proxy bash tests/test-mesh-labor-reconciliation.sh` — PASS, including overlapping concurrent
  feeders, balanced missing/duplicate transactions, and a delayed event behind the watermark.
- `rtk mesh-ledger --check` — PASS, 682 windows, 0 overlaps, 0 gaps.
- `rtk mesh-promises --check` — FAIL, replay 263 vs journal 0; parity itself passes. This is a separate
  promises-ledger discrepancy, not caused by the labour reconciliation.
- Repository source invocation `MESH_LABOR_DIR="$HOME/.mesh/labour" MESH_SPEND_LOG="$HOME/.mesh/spend.log" bash scripts/mesh-labor --check` — runs the checked-in helper and correctly FAILs on the two missing feed rows (plus the correction-parser limitation above).
- Installed `mesh-labor --check` — UNKNOWN/rc 2 because its adjacent helper is absent at
  `~/.local/bin/mesh_labor_reconcile.py`; source helper exists at `scripts/mesh_labor_reconcile.py` but is
  not deployed. Do not present the installed check as green.
- Explicit completed-task query `autopoiesis-observation-windows-20260908/materialize-observation-series`:
  hledger task tag totals 69 TURN; interval estimate 1 TURN for owner `senses`. These are different measures;
  the interval estimate is not proof of per-turn task attribution.
- Explicit open-task query `coordination-hledger-plan-20260908/accounting-coverage`: hledger task tag totals
  0 TURN; interval estimate 5 TURN for owner `genome` through `2026-09-12T01:54:09Z`. Current task turns are
  untagged, so exact task cost remains unknown despite the interval estimate.

Disposition: acceptance is met as an observation and reconciliation report: the historical correction is
classified with source evidence, the two unexplained feed omissions remain explicit failures, balanced
missing feeds are rejected by the fixture, and explicit-vs-interval task coverage is shown for one closed
and one open task. Follow-up obligations remain visible: teach the helper to recognize documented
correction transactions, restore its installed companion-file wiring, reconcile the two omitted source
turns from an authoritative adjustment if one exists (otherwise retain the failure), and investigate the
separate promises check failure. No historical task attribution was guessed.
