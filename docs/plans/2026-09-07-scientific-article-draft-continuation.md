# Green Lies Scientific Article Continuation Plan

> Continuation plan for the existing manuscript; this is a working research artifact, not a publication or approval record.

**Goal:** finish a reproducible manuscript package for the existing *Green Lies* taxonomy without promoting blocked measurements into claims.

**Existing anchor:** `docs/paper/green-lies-taxonomy.md`, currently increment 5, with C1–C10 enumerated and D1–D3 implemented.

**Contribution boundary:** a case-based taxonomy of self-observation failures, three mechanically exercised detectors, class-dependent comparison results, and explicit limits on authorship/generalization claims.

**Global constraints:**

- Every positive result must point to a repository artifact, date, and commit or recorded run.
- `blocked`, `not-run`, and `failed` remain distinct states; none becomes zero or pass.
- The tiny-fleet bundle may support reproducibility and claim-discipline discussion, but not a general architecture-drift claim.
- No external publication occurs from this continuation; the output is a reviewable repository package.

## Chain and current state

1. **Source/draft audit — complete:** `docs/paper/continuation/01-source-draft-audit.md`
2. **Research gap and claims — complete:** `docs/paper/continuation/02-gap-and-claims.md`
3. **Methods/analysis contract — complete:** `docs/paper/continuation/03-methods-analysis.md`
4. **Figures/tables/evidence index — complete:** `docs/paper/continuation/04-evidence-index.md`
5. **Manuscript continuation — drafted:** `docs/paper/continuation/05-manuscript-draft.md`
6. **Review/reproducibility — complete for locked historical scope:** `docs/paper/continuation/06-review-reproducibility.md` records passing self-tests and `07-historical-scope-reproduction-20260907.md` records the commit-pinned reconciliation.
7. **Final package — assembled:** checksum/manifests-only package records the reviewable continuation; it is not a submission or publication artifact.

## Exact next actions

- Run `--selftest` for D1, D2, and D3, plus the three repository scans used by the manuscript. **Done; receipt records outputs.**
- Reconcile every number in the continuation draft against the source manuscript and detector output. **Done; historical scope is reproduced and pinned.**
- Record any changed counts as a new dated measurement, never as a silent edit to the old result. **Done; current drift is recorded in the reproduction receipt.**
- Add the reproducibility receipt and package manifest only after the checks above complete. **Done.**
