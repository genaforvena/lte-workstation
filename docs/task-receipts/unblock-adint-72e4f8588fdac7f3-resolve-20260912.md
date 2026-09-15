# Resolver receipt: `unblock/adint/72e4f8588fdac7f3/resolve`

- Checked: `2026-09-12T01:07:25Z` UTC on `mesh-home`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/72e4f8588fdac7f3/resolve adint` exited `0`; claimed by adint.
- Result: **BLOCKED/operator-input; current revalidation and exact operator packet recorded**

## Diagnosis

The live parent remains blocked on `operator-input`; its current retry condition
requires frozen dictionary inputs and a new artifact-backed result. The live
`rtk mesh-task check resume unblock/haunt/62c0662129fa8ee9/resolve haunt`
refused with exit `2`.

The fresh tiny-fleet study `docs/` and `runs/` filename scan found no
dictionary, lexicon, or study-input manifest. The sole dictionary-named hit is
`runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`,
an unrelated ticket-extraction artifact. The existing parent receipt
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-62c0662129fa8ee9-20260911.md`
has SHA-256 `d1fbdfe4267e4e1c87b1971aab99c49568c5035bb82fe9deea444aa79c06f5d4`.
The current `/home/mesh-home/tiny-fleet/scripts/bbywvy_test.py` has SHA-256
`377521b04612de877b18caf046157d772293e23539f8d11817ee771cad598a8a`; it runs
the six generative cases and has no dictionary arm. Prior same-parent receipt
[`unblock-adint-327916eaeec8b5d5-resolve-20260912.md`](unblock-adint-327916eaeec8b5d5-resolve-20260912.md)
has SHA-256 `d6f78a99d330d2e357ece6fc717493b64ed85f81a89ea86ce4bcc50f4c697edc`
and documents why choosing local inputs would alter the experiment.

## Exact operator-action packet

Provide a tracked immutable manifest and matching corpus bytes with all five
fields populated:

```yaml
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact executable Unicode and token normalization policy>
version: <immutable release, commit, or source checksum>
corpus: <immutable corpus path/URI and SHA-256 of the exact bytes>
```

Then verify the corpus digest, run the dependency preflight and dictionary-arm
command, and record versions, output hashes, and a typed verdict. Resume the
parent only after that dictionary result exists. The bounded command
`cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`
checks only six generative cases and cannot clear this blocker.

Retry condition: `event:operator-dictionary-input` when the approved five-field
manifest and matching corpus bytes are available.
