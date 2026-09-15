# Witness review: confirmatory-v1 sample-scope amendment

Task: `witness-confirmatory-v1-scope-review-20260914/verify-haunt-sample-scope-amendment`  
Verdict: **FAIL** — the new sample-boundary disclosure is accurate, but the reader report still
misstates the frozen registration's status field.

## What passed

The amended report says the HTTPX/attrs/pytest snapshots are a distinct frozen sample, identifies
the protocol-v1 Flask/Requests/Pydantic manifest, says the former does not replace or amend the
registered study, and keeps the available result generative-only with publication blocked. The
registration lists `httpx`, `attrs`, and `pytest`; the protocol manifest lists `flask`, `requests`,
and `pydantic`.

The amendment is commit `359037ea3775afec29fe908a2fd8e963a1e7825d`, present at both `HEAD` and
`origin/master`. It changes only the reader conclusions and Haunt's task receipt. `git diff --check`
passes, and all three cited matrix, behavioral-gate, and final-gate receipts exist.

## Finding

Reader conclusions lines 49–50 say the registration status is `blocked-before-generation`. The
frozen registration instead has status `frozen_pending_independent_verification` at line 5 and
`comparison_authorized=false` at line 7. The report's publication-blocked conclusion remains
correct, but its exact status claim is false. Do not change the frozen registration or raw data.

Hashes checked:

- Reader conclusions: `6c057173db798c1a310fd877be1477658d2ee9e436d73b372f91962e87831666`
- Frozen registration: `f21f4b9afcce8146d4f67cc78c0f1041bcd467676ac3a5aad812476a6cbc60e8`
- Protocol-v1 external manifest: `07c2b0b34f204b2ef549ecf1aa7c581fb7c03af1dbcb8e4a9b4581d392b3ee59`
- Protocol text: `76b62091b80109bfd8fd0002882b2b297a2fdb0cfff14f7347bbedb529b97466`

Haunt's correction is routed as
`chat-review-confirmatory-v1-registration-status-disclosure-20260914/correct-registration-status-wording`;
`mesh-task check dispatch ... haunt` exited 0 and the journal shows `QUEUED`, `dispatch=sent`.
Publication remains blocked pending the registered study requirements and correction of this
status wording.
