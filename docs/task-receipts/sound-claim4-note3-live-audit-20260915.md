# Sound claim 4 live audit — 2026-09-15

## Evidence

- Command: `mesh-series-stats --claims`
- Source: `/home/mesh-home/.mesh/records.log`
- Observed source mtime/row count: `2026-09-15T21:50:27Z`, `2423 rows`
- Claim 4 result: `REFUTED`; strict sub-window rows `n=1617`, impossible `300 (18.6%)`, abstained `406`.
- note3 arm: `293/458` violations (`64.0%`). Whole-file scans with `fbeats=1`: `322/1617`; `273/300` violations are in that degenerate population.
- The same live run reports note3 violation rows with mean `beats=6.0`, `fbeats=1.2`; clean rows mean `beats=4.4`, `fbeats=14.3`. It attributes the note3 effect to the whole-file side collapsing, not window inflation.

Representative ledger row, verified with `awk` from the same source:

```text
2026-08-20T01:02Z note3 c840f85d dur=11.80 win=3.00 cov=0.254 score=37.9 beats=6 [even·dark·tonal] dyn=0.112 act=0.266 rich=0.678 move=0.057 cent=1031.6 fbeats=1 fdyn=0.119 fact=0.291 frich=0.657 fmove=0.152 fcent=1046.4 -> skip:not-picked(a stronger record led this block)
```

The source/hash linkage is the ledger's `source=note3`, record hash `c840f85d`; no separate source path is emitted for this retained row. The row directly verifies `beats=6 > fbeats=1` and is a degenerate whole-file scan.

## Decision

Keep the finding as an audit-only `REFUTED` result. Do not retune the ranker, estimator, or gate from this observation: the violation is dominated by degenerate whole-file scans and the charter forbids unilateral live retuning. Next trigger: a fresh non-degenerate note3 sample with whole-file `fbeats>1` and a named source/hash join; re-run `mesh-series-stats --claims` before considering any change.
