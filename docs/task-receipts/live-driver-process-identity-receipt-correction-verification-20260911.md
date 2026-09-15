# Live driver receipt SHA correction — witness verification — 2026-09-11

PASS. Receipt-only commit `2495a657` is on `origin/main` and replaces the stale hash with the
actual final `mesh-consume-all` SHA-256
`31d7a6be9e0429417d7cd39a90f901a9abea5a6e6cf7cb779379b36d571165f5`.

Independent checks:

- source and deployed supervisor hashes both equal the corrected receipt value;
- the decoy/concurrency identity regression passes;
- all 15 live channel drivers are UP with preserved intervals;
- the receipt no longer contains the stale `c226...` value.
