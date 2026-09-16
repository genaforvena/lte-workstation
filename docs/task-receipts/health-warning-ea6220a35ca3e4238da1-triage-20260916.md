# Health warning triage

- Warning: `health-warning/ea6220a35ca3e4238da1/triage`
- Source event: `2026-09-15T18:16:03Z`
- Original evidence: `/tmp/discover-saf-ls-20260915.txt`, 285 bytes, SHA-256
  `e14177f390dfb42a0f2132ebc9e214ea52f6a9e635e4928e7c7d27fefdbed93a`

## Finding

The warning is stale and should be closed as report-only. The original probes all failed (`rc=255`:
Redmi refused, `192.168.8.146` no route, `100.103.99.16` timeout), so the 18:16 report correctly
called reachability and capability unknown at that time. A later exact owner task,
`discover-termux-saf-ls-20260916/probe-termux-saf-ls`, reached the resolver-selected Redmi endpoint
`192.168.8.203`, returned a valid empty JSON array with `rc=0`, and recorded 1/1 acceptance in
`/home/mesh-home/.mesh/knowledge/capability-termux-saf-ls-redmi-20260916.md` (SHA-256
`0866e3a06a6b60b7d0066b2c8acbf6e88aee359860b21b3dd95db3e883e18c09`). The capability is proven but
currently empty; no SAF folder is authorized.

## Decision

No network or substrate mutation is justified. Close this warning as stale/report-only. The next
retry edge is a fresh endpoint failure or a new request for an authorized SAF folder; do not retry
the failed historical endpoints as if they were current state.

## Verification

Personally inspected the original `/tmp` artifact, the later capability artifact, canonical chat/task
ledger lines showing the later task completed, and fresh `mesh-health` at `2026-09-16T01:28:10Z`.
The independent read-only `health-warning-audit` worker was also inspected; its report was advisory
and did not supply evidence or perform mutations. Receipt creation and final ledger/board ownership
were kept local because they are tightly coupled to this triage.
