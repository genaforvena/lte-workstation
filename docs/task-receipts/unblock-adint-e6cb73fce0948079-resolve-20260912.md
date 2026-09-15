# Resolver receipt: `unblock/adint/e6cb73fce0948079/resolve`

- Checked: `2026-09-12T01:20:29Z` UTC on `mesh-home`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/e6cb73fce0948079/resolve adint` exited `0`; claimed by adint.
- Result: **BLOCKED/operator-input; current revalidation and operator packet recorded**

## Diagnosis

The current parent ledger remains blocked on `operator-input`; its retry
condition requires all five dictionary fields to be supplied and frozen with
hashes. The live
`rtk mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt`
refused with exit `2`.

The fresh tiny-fleet study `docs/` and `runs/` filename scan found no
dictionary, lexicon, or study-input manifest. Its only dictionary-named hit is
`runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`,
which is unrelated ticket-extraction output. The parent receipt
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-fd5d75268b44e1cc-20260911.md`
has SHA-256 `b4d851e5e285e407ffa60991e07f32be789babf5bc8947d0a21a763a98e4a18d`.
The previous same-parent resolver
[`unblock-adint-64b6565033b7a507-resolve-20260912.md`](unblock-adint-64b6565033b7a507-resolve-20260912.md)
has SHA-256 `c04adfffbe9a849daac26c6013e94229e4eb559d5dcd0e1908690ef592e473d5`
and records the same missing input boundary.

No safe local choice can provide a scientific source, language, normalization,
version, or corpus without changing the registered study.

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

After delivery, verify the corpus digest, run the dependency preflight and the
dictionary-arm command, and record versions, output hashes, and a typed
verdict. Resume the parent only after that result exists. The bounded smoke
`cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`
checks only six generative cases and cannot clear the dictionary blocker.

Retry condition: `event:operator-dictionary-input` when the approved five-field
manifest and matching corpus bytes are available.
