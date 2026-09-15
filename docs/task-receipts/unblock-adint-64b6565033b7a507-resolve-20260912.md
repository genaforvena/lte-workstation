# Resolver receipt: `unblock/adint/64b6565033b7a507/resolve`

- Checked: `2026-09-12T01:18:09Z` UTC on `mesh-home`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/64b6565033b7a507/resolve adint` exited `0`; claimed by adint.
- Result: **BLOCKED/operator-input; current revalidation and exact operator packet recorded**

## Current diagnosis

The parent still reports `blocked` on `operator-input`, with retry condition
“after operator supplies frozen dictionary inputs, retry install/study task
using approved source and capture a new artifact-backed result”. The current
`rtk mesh-task check resume unblock/haunt/62c0662129fa8ee9/resolve haunt`
refused with exit `2`.

The fresh filename scan across tiny-fleet study `docs/` and `runs/` found no
dictionary, lexicon, or study-input manifest. The only dictionary-named result
is `runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`,
an unrelated application artifact. The parent receipt
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-62c0662129fa8ee9-20260911.md`
has SHA-256 `d1fbdfe4267e4e1c87b1971aab99c49568c5035bb82fe9deea444aa79c06f5d4`.
Prior same-parent resolver
[`unblock-adint-72e4f8588fdac7f3-resolve-20260912.md`](unblock-adint-72e4f8588fdac7f3-resolve-20260912.md)
has SHA-256 `2e8bb66712c98e8331a01bfbc0117840fe6ee37a23ec34476cb099221ac388f4`
and records that the named file is unrelated to the study.

No safe local choice can supply scientific inputs without changing the study.

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

After delivery, verify the corpus digest, run the parent's dependency preflight
and dictionary-arm command, and record versions, output hashes, and a typed
verdict. Resume only after the dictionary arm has an artifact-backed result.
The bounded runtime command
`cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`
checks six generative cases only and cannot clear the dictionary blocker.

Retry condition: `event:operator-dictionary-input` when the approved five-field
manifest and matching corpus bytes are available.
