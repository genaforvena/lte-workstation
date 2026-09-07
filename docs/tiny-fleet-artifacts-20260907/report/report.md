# Tiny-fleet expansion pilot report

**Report date:** 2026-09-07  
**Publication verdict:** BLOCKED for a general cross-repository or architectural-drift claim

## Scope and schema

This bundle is the publishable reporting contract for the measured pilot. It is a dependency-light,
offline comparison of `lte-workstation` at immutable commits
`5475816081b26a0f9aebb92da844493b19304eef` and
`e8f47364e5a0f224c1bd03331df592272a187df5`. The canonical protocol digest is
`a7c75ec9d74cbc6dcdd0033ab3fbe2ab041d372670159edf9a03b1a0e96dcf17`.

The report schema is `tiny-fleet-publishable-report/v1`. Every reported number is either copied from
`measurement-controls/metrics/evaluator.json` or marked unavailable. Raw rows remain in
`measurement-controls/raw/manifest.json`; controls and arm separation remain separate artifacts.

## Measured result

| estimand | result | interpretation |
|---|---:|---|
| structural file count | 232 → 1,441 (delta +1,209) | observed paired snapshot change only |
| lexical JSD | 0.2131325787540394 | lexical divergence; not architecture |
| byte delta bootstrap | 20,006.83 (95% 17,939.24–22,278.63; n=1,441) | file-level interval, not population CI |
| token delta bootstrap | 2,169.82 (95% 1,948.43–2,416.87; n=1,441) | file-level interval, not population CI |
| same-snapshot repeatability | PASS, delta 0 | mechanical evaluator control |

The evaluator's leakage control is **FAIL**: snapshot B contains six duplicate blobs within the
scanned snapshot. The mutation, path-order, and swapped-label controls pass. Shuffled conditioning
was not run because no live model conditioning was supplied.

The prompt-only arm is `control-only`, not training. Genuine LoRA/QLoRA is `blocked`: `torch`,
`transformers`, and `peft` are absent despite an accelerator tool being detectable. No proxy claim
is made.

## Limitations and interpretation rules

1. This is one repository and two snapshots. It cannot support cross-repository, temporal-trajectory,
   stratum, or generalization claims.
2. Lexical JSD, vocabulary, bytes, and file counts are not architectural drift. Architecture requires
   structural graph/API evidence and behavioral evidence, neither of which is estimated here.
3. The interval is file-level bootstrap uncertainty. It is not clustered by independent repositories
   and must not be presented as a population confidence interval.
4. Duplicate blobs invalidate a clean leakage interpretation until removed or explicitly explained.
5. Missing, blocked, and not-run arms remain those states; none is converted to zero or pass.
6. The corpus lock is an offline two-source fixture/provenance lock, while the measured evaluator
   run is explicitly the single-repository pilot above. These are not silently pooled.

## Reproduction

```bash
bash tests/test-mesh-tiny-fleet-evaluator.sh
bash tests/test-mesh-tiny-fleet-validation.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/mesh-tiny-fleet-evaluate
```

For the exact recorded evaluator output, use the replay command in
`measurement-controls/README.md`; expected evaluator exit is `2` because leakage fails.

## Bundle contents

- `report.json` — machine-readable schema, verdict, estimands, and artifact references.
- `claim-matrix.tsv` — every claim reconciled to raw evidence and disposition.
- `methodology.md` — drift/close methodology and weekly extension boundary.
- `roadmap.md` — prioritized work required to unblock publication.
- `review-receipt.md` — independent mechanical review, including concrete failures.
- `checksums.sha256` — digest manifest for this report bundle and its source artifacts.
