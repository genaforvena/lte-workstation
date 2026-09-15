# AdFox research gap disposition — 2026-09-12

Task: `adfox-research-reconciliation-20260912/adfox-gap-disposition`.
Historical ask: `docs/historical-ask-adfox-research-design-20260906.md`.
Evidence reviewed: `docs/adfox-research-existing-evidence-manifest-20260912.md` and
`docs/design-audit-adfox-20260912.md`.

## Decision

The historical ask is **partly answered, but not fully satisfied**. The existing Adint
study already provides substantial prior-art and auction-field analysis across two date
buckets and multiple placements. Its own report limits the conclusions to observed,
page-visible browser data and records coverage and uncertainty. Repeating that broad
investigation would be duplicative.

The requested per-observation evidence contract is materially incomplete. The manifest
found no raw-response hashes or stored response bodies; only relative per-request times;
incomplete full URLs and query/profile provenance; and aggregate rather than
per-observation field-name reporting. In particular, 1,129 captured AdFox `getBulk`
paths lack `req_url_full`, and the existing parser excludes them. The prior data cannot
be retroactively made to satisfy these requirements by hashing a ledger or outbound
request URL.

**Disposition: no new collection in this task.** The current report remains useful for
its bounded conclusions, but the evidence-contract gap stays open. This disposition
does not dispatch or authorize future capture. Any future collection requires a
separately accepted task and fresh operator authorization for live browsing/capture.

## Bounded successor design (proposal only)

If the operator elects to close the gap with new evidence, use one consenting browser
profile and three operator-selected placements, represented in shared outputs only by
random aliases. Observe one ordinary page visit per placement on each of two distinct
UTC dates: six visits total, with a hard cap of ten minutes and 100 matching AdFox
responses per visit (600 responses maximum). Do not automate page reloads, create
accounts, vary identity/profile attributes, or generate requests solely to increase
the sample. Stop early at either cap and report the resulting coverage.

For each observed response, assign a random observation ID and record, in a private
restricted ledger: exact request URL; UTC retrieval timestamp; date, placement, and
profile-condition aliases; the declared condition values; response status; observed
field names; response-body SHA-256; and capture completeness. Hash the response bytes
before parsing or redaction. Keep the raw body only in a private, access-restricted
working area for validation, then discard it after the digest and redacted field record
are verified. Do not publish raw URLs, bodies, cookies, profile identifiers, bidder or
publisher names, placement/campaign identifiers, or query values. Shared results may
contain only salted or random aliases, aggregate counts, field names that pass a
privacy review, digests, redaction notes, and explicit coverage/uncertainty statements.

Before any live run, require an accepted task that records the operator's authorization,
the selected placements/profile conditions, storage location and access controls, and
the retention/deletion date. Validate capture on a synthetic fixture first: the test
must prove the UTC timestamp, complete URL byte length, condition aliases, response
field inventory, raw-body digest, redaction, and cap/stop behavior without contacting
AdFox. At completion, independently reconcile attempted visits, captured responses,
cap exits, missing fields, and digests; publish only the redacted manifest and bounded
aggregate findings. If any provenance field cannot be captured or privacy review
fails, stop and publish the shortfall without substituting inference.

No live browsing, traffic collection, source-ledger mutation, or edit in
`/home/mesh-home/self-adint` was performed for this disposition.
