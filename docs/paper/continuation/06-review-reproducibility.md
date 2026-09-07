# Review and reproducibility receipt — Green Lies continuation

**Date:** 2026-09-07  
**Reviewer:** pub continuation pass  
**Verdict:** REVIEW-COMPLETE for the historical scope; no external publication

## Checks actually run

| check | result | evidence |
|---|---|---|
| D1 detector self-test | PASS | `d1_self_grepping_gate.py --selftest`, rc 0 |
| D2 detector self-test | PASS | `d2_silent_fallback.py --selftest`, rc 0 |
| D3 detector self-test | PASS | 24/24 arms, rc 0 |
| tiny-fleet evaluator test | PASS | `tests/test-mesh-tiny-fleet-evaluator.sh`, rc 0; mutation arm intentionally observed FAIL and was caught |
| tiny-fleet validation tests | PASS | `tests/test-mesh-tiny-fleet-validation.sh`, rc 0 |
| continuation placeholder scan | PASS | no unresolved placeholder markers |

## Fresh detector scans

These are current scans of `scripts/` on 2026-09-07, not replacements for the historical counts
in the existing manuscript:

| detector | fresh result |
|---|---|
| D1 | 121 source-grep sites; 40 undecidable; 62 decidable boolean gates; 29 vacuous |
| D2 | 14,969 fallback sites; 7,950 decidable; 821 silent; 14 critical; 687 numeric |
| D3 | 337 cadence-header tools; 285 undecidable; 13 sample-as-state; 7 honest; 32 full |

## Reconciliation finding

The manuscript reports earlier measurements (for example D1 60 sites / 3 vacuous and D3 320
tools / 275 undecidable). The detector code and repository have changed since those measurements,
or the historical scans used a different corpus boundary. This is exactly the kind of provenance
gap the paper studies. The final package must choose one of two honest forms and record it:

1. reproduce the historical scope from the cited commit and retain the historical table, or
2. promote the 2026-09-07 scans as a new dated measurement and rewrite every affected table,
   interpretation, and denominator.

The historical-scope option was selected and reproduced. Receipt:
`docs/paper/continuation/07-historical-scope-reproduction-20260907.md`. The manuscript retains its
historical tables, while the current working-tree counts are recorded as dated drift only. The
external comparison corpus remains inherited from the source manuscript and is explicitly not
claimed as a fresh 2026-09-07 scan.
