# Confirmatory-v1 critical publishability review — 2026-09-14

Task: `tinyfleet-confirmatory-v1-comparison-20260914/critical-publishability-review`

## Verdict

**FAIL for conformance to the current cross-repository drift protocol; publication remains
blocked.** The reader report is careful about missing estimands and labels its generative result
descriptive, but it does not disclose that this run used a different repository sample from the
protocol's sole frozen external-sample manifest.

## Protocol scope

The current protocol says to use all three entries from
`docs/tiny-fleet-artifacts-20260907/architecture-drift/02-external-sample-v2/sample-manifest.json`
and calls it the sole input registry for the external sample (`docs/cross-repository-drift-protocol.md:171-176`).
That manifest is hash-pinned at
`07c2b0b34f204b2ef549ecf1aa7c581fb7c03af1dbcb8e4a9b4581d392b3ee59` and names Flask, Requests,
and Pydantic. This run's separate sample registration is hash-pinned at
`f21f4b9afcce8146d4f67cc78c0f1041bcd467676ac3a5aad812476a6cbc60e8`; it names HTTPX, attrs, and
pytest. The frozen generation registration is
`157fb3351366e656760ff17bb1a1379607fcc8d14fdc3a83037dbc338c265de7` and binds those latter three.

The gate audit accurately calls this a distinct confirmatory-v1 sample, but the reader report only
lists HTTPX/attrs/pytest without saying it is outside the existing protocol sample. Until the
protocol is formally amended with a new frozen sample, the report must label these results as a
separate out-of-protocol study and must not present them as confirmation of the registered
Flask/Requests/Pydantic study.

## Evidence and bounds

- The 2026-09-14 VPN gate receipt reports PASS for the exact behavioral-closeout and generation-
  registration hashes. The frozen generation registration itself still says
  `blocked-before-generation` and `comparison_authorized=false`; the reader report discloses this
  unresolved state and correctly does not call the comparison publishable.
- Independent local validation returned `ACCEPT` for all 162 unique successful generation records.
  `verify_amendment()` returned true for the raw-tape, registration, scorer, validator, and bundle
  hashes. It formed 81 complete pairs; all score-row output and adapter hashes matched the raw
  pairs. No score-input hash mismatches were found.
- Recomputed means match the reader report: base 1.000, prompt-only 0.481, LoRA 0.782; LoRA exceeds
  prompt-only in each sampled project. All 27 base pairs have identical output hashes. The score
  artifact has no interval fields, which agrees with the report's stated lack of inference.
- The run has no `structural.tsv`, `lexical.tsv`, `behavioral.tsv`, or `controls.tsv`. The report
  correctly states that structural and lexical measurements, a paired behavioral change estimate,
  required negative controls, and uncertainty intervals are absent. The frozen excerpt ledger also
  records selection after the objective-label freeze; this is disclosed as a chronology limit.
- The corpus/adapter preflight receipt records that all six excerpt source modules were excluded
  from train and validation splits. The scorer amendment and independent validator-binding review
  receipts match the current scorer hashes.

## Required correction

The reader conclusions need an explicit sample-scope statement. This review did not edit that
report or rerun generation/scoring. It filed one corrective task against the new finding; the
existing run and its descriptive measurements remain intact.

Verification was read-only: source/protocol and receipt review, hash comparison, generation-record
validation, amendment verification, and score-to-raw-pair checks. No tests or model calls were run.
