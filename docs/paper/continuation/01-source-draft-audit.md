# Source and draft audit — Green Lies continuation

**Date:** 2026-09-07  
**Owner:** pub  
**Status:** audited; continuation in progress

## Recovered draft and intended contribution

The active long-form draft is `docs/paper/green-lies-taxonomy.md`, not one of the shorter
`docs/devto-*-draft.md` posts. Git history shows five evidence-bearing increments:

| revision | artifact | recovered contribution |
|---|---|---|
| `0a620fe2` | manuscript + `d1_self_grepping_gate.py` | C1 and the zero-rate comparison arm |
| `06c90e63` | manuscript | C9: absence from the candidate set |
| `70f5961d` | manuscript | C10: runtime echo-port failure |
| `e6481f0e` | manuscript + `d2_silent_fallback.py` | C2 and the class-dependent comparison |
| `e358837e` | manuscript + `d3_window_under_cadence.py` | C3, coverage, and detector self-failure |

The intended contribution is empirical, not a universal theory: define recurring structural
ways self-observation can emit a fresh-looking green result, tie each class to a real incident,
and test which classes are statically decidable and how their rates differ across a bounded
comparison corpus.

## Evidence inventory

- Manuscript: `docs/paper/green-lies-taxonomy.md` (explicitly DRAFT, not submitted).
- Detectors: `docs/paper/detectors/d1_self_grepping_gate.py`, `d2_silent_fallback.py`,
  `d3_window_under_cadence.py`.
- Reproducibility instructions: manuscript §5 and each detector's `--selftest`.
- Measurement package: `docs/tiny-fleet-artifacts-20260907/report/`, with raw inputs and
  control results under `measurement-controls/`.
- Review boundary: `report/review-receipt.md` says the tiny-fleet bundle is a blocked pilot,
  not a general cross-repository or architectural-drift study.

## Audit findings

1. The manuscript's numbered classes exceed its implemented detectors; C4–C10 are taxonomy
   entries, not seven completed detector implementations.
2. The strongest measured contribution currently rests on C1–C3 plus the documented C9/C10
   cases. The paper must not imply a complete automated taxonomy.
3. The existing §4 already names the key gaps: authorship confounding, monitoring-corpus
   comparison, longitudinal re-derivation, undecidable buckets, and detector precision/recall.
4. The tiny-fleet artifacts demonstrate the paper's desired claim discipline: leakage fails,
   fine-tuning is blocked, and lexical change is not called architectural drift.

**Recovery decision:** continue the existing manuscript in place conceptually, but keep new
audit, claims, methods, evidence, manuscript, review, and package artifacts in this directory.
