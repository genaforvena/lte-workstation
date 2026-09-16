# Redmi `termux-saf-ls` consumer — senses receipt

Date: 2026-09-16  
Owner: `senses`  
Source contract: `docs/task-plans/discover-termux-saf-ls-handoff-20260916.tsv:1`  
Capability evidence: `/home/mesh-home/.mesh/knowledge/capability-termux-saf-ls-redmi-20260916.md`

## Implementation

Added [`scripts/mesh-phone-saf-ls`](../scripts/mesh-phone-saf-ls), a narrow on-demand consumer:

- accepts one `folder-uri` argument;
- resolves the Redmi through `mesh-phone-ip` and invokes `termux-saf-ls '<folder-uri>'` over SSH;
- validates that stdout is a JSON array and preserves the array verbatim, including valid empty `[]`;
- renders transport, remote-command, and malformed-response failures as `UNKNOWN` with exit `2`;
- rejects a missing or multi-line local URI with exit `1`.

No phone permission was granted and no substrate state was changed.

## Verification

- Added `tests/test-mesh-phone-saf-ls.sh` with stubs for a successful JSON array, valid `[]`, malformed
  JSON, transport failure, and folder-URI forwarding.
- TDD red check: before the implementation existed, the test failed with
  `scripts/mesh-phone-saf-ls: No such file or directory`.
- Green checks: `bash tests/test-mesh-phone-saf-ls.sh` passed; `bash -n scripts/mesh-phone-saf-ls
  tests/test-mesh-phone-saf-ls.sh` passed.
- Live gate: `scripts/mesh-phone-saf-ls --test` performed a fresh SSH read and returned exit `2`
  with `UNKNOWN ... why=malformed-json-array`; this is an honest unavailable result for the
  default URI, not a false empty-list success. A future test with an operator-granted SAF URI is
  the retry edge.

Delegation: `senses-termux-audit` performed a read-only contract/artifact audit via CSD. I personally
inspected its cited plan, capability artifact, handoff receipt, and ledger status; its findings
matched those artifacts. Ownership, edits, task settlement, and final verification remained in
this window.
