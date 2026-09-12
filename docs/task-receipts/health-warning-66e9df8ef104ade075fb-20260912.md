# Health warning triage: repeated UVC metadata warning

Task: `health-warning/66e9df8ef104ade075fb/triage`

The task's 2026-09-10 snapshot reported a successful real one-buffer test (5,874 bytes) after
intermittent V4L2 stream-start timeouts, with an 8,800-byte artifact from 09:10Z. That historical
success did not establish steady health.

Current independent evidence is recorded in
[`health-warning-9acbe26cce46544962c3-20260912.md`](health-warning-9acbe26cce46544962c3-20260912.md):
a real test probe succeeded with 7,524 bytes / 342 records, while the next normal bounded capture
failed after timeouts and empty buffers. The failure remains intermittent. During this review the
canonical artifact changed again to 528 bytes, mtime `2026-09-12 13:15:27 UTC`, SHA-256
`15d42a8cd4c8afd73e779df51a486dafeefa8edd730f93b62f306432c6aa947a`; independent parsing found
24 timestamped records. The artifact's writer is not attributable from the retained log.

Verdict: this is a duplicate warning for the same known intermittent V4L2 startup/read failure, not
a newly established fault or a fix. It adds corroboration that a parseable artifact may change
without a known per-invocation producer. Preserve the current behavior and do not add a speculative
device or substrate change. Keep the known blind explicit: the metadata organ is wired and can
produce valid buffers, but individual runs can time out or return empty data, and the latest-file
path alone does not identify its writer. No previously-DONE task was reopened.

Verification: current artifact hash and byte count were recomputed; `mesh-uvc-metadata --parse`
returned 24 valid records. The related live test and failed normal capture, plus schedule wiring,
are documented in the linked receipt.
