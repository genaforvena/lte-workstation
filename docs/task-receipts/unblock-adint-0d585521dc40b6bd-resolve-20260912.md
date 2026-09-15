# Resolver receipt: `unblock/adint/0d585521dc40b6bd/resolve`

- Checked: `2026-09-12T01:30:47Z` UTC on `mesh-home`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/0d585521dc40b6bd/resolve adint` exited `0`; subsequent ledger status confirmed the row active under owner `adint`.
- Result: **BLOCKED/operator-input; current revalidation and exact packet recorded**

## Diagnosis

The parent remains blocked on `operator-input`, with retry condition requiring
the five dictionary fields to be supplied and frozen with hashes. The current
`rtk mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt`
refused with exit `2`.

The fresh tiny-fleet study `docs/` and `runs/` filename search found no
dictionary, lexicon, or study-input manifest. Its sole dictionary-named hit is
`runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`,
an unrelated application artifact. The parent receipt
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-fd5d75268b44e1cc-20260911.md`
has SHA-256 `b4d851e5e285e407ffa60991e07f32be789babf5bc8947d0a21a763a98e4a18d`.
The previous same-parent receipt
[`unblock-adint-e6cb73fce0948079-resolve-20260912.md`](unblock-adint-e6cb73fce0948079-resolve-20260912.md)
has SHA-256 `a4e59f88df03e580a795d2ed066dd1ef053d298f944dae6c488d4b925bce7f52`
and records the same missing-input boundary.

No safe local source, language, normalization, version, or corpus can be
selected without changing the registered study.

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
verdict. Resume the parent only when the dictionary arm has its own
artifact-backed result. The bounded command
`cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`
checks six generative cases only and cannot clear the dictionary blocker.

Retry condition: `event:operator-dictionary-input` when the approved five-field
manifest and matching corpus bytes are available.
