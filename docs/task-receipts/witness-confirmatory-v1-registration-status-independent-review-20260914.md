# Independent review of the confirmatory-v1 status correction — 2026-09-14

Task: `witness-confirmatory-v1-registration-status-independent-review-20260914/verify-corrected-report`.

**Verdict: PASS for the factual correction and retained scope.** This review does not authorize or
validate the underlying comparison as publishable.

The corrected reader report at
`/home/mesh-home/tiny-fleet/docs/confirmatory-v1-reader-conclusions-20260914.md` now quotes the
frozen registry at `runs/drift-confirmatory-v1/registration.json`: its status is
`frozen_pending_independent_verification`, while `comparison_authorized` remains `false`. The
report describes the HTTPX/attrs/pytest material as a distinct sample from the protocol-v1
Flask/Requests/Pydantic sample, limits its result to descriptive generative-only evidence, and
retains the publication block. The obsolete `blocked-before-generation` wording is absent.

Evidence hashes:

- Reader report: `a376c97beb40ca5ed8718abe223045ad47c6bcfdb1317081dea0cffb5191e54d`
- Frozen registration: `f21f4b9afcce8146d4f67cc78c0f1041bcd467676ac3a5aad812476a6cbc60e8`
- Correction receipt: `f66520a1cd7c2469bfc95d5d1e97aeb928501e7b76f206a4922771a1858de349`
- Protocol v1: `76b62091b80109bfd8fd0002882b2b297a2fdb0cfff14f7347bbedb529b97466`

Verification performed:

- Parsed the exact frozen registration and checked both values against the report.
- Confirmed the prior incorrect wording is absent, the sample and publication scope remain explicit,
  and all relative Markdown links resolve.
- Confirmed the correction receipt contains the current report and registration hashes.
- Confirmed commit `525573451a8d23ca6da662bd1b2bd8aaa8afd542` changes only the reader report and its
  correction receipt, not the frozen registration; local `HEAD`, `origin/master`, and remote
  `refs/heads/master` resolve to that commit.

No Tiny Fleet files were changed during this independent review.
