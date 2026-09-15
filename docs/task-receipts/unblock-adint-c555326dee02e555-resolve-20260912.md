# Resolver receipt: `unblock/adint/c555326dee02e555/resolve`

- Checked: `2026-09-12T01:09:44Z` UTC on `mesh-home`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/c555326dee02e555/resolve adint` exited `0`; claimed by adint.
- Result: **BLOCKED/operator-input; current revalidation and operator-action packet recorded**

## Diagnosis

The live parent remains blocked on `operator-input`, requiring all five
dictionary fields to be supplied and frozen with hashes. The current
`rtk mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt`
refused with exit `2`.

The fresh search of tiny-fleet study `docs/` and `runs/` found no dictionary,
lexicon, or study-input manifest. The only dictionary-named result is
`runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`,
which is unrelated ticket-extraction output. The current
`/home/mesh-home/tiny-fleet/scripts/bbywvy_test.py` SHA-256 is
`377521b04612de877b18caf046157d772293e23539f8d11817ee771cad598a8a`; it is
the six-case generative smoke and has no dictionary arm. The parent receipt
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-fd5d75268b44e1cc-20260911.md`
has SHA-256 `b4d851e5e285e407ffa60991e07f32be789babf5bc8947d0a21a763a98e4a18d`.
The prior same-parent adint receipt
[`unblock-adint-fde22f1d70bffa98-resolve-20260912.md`](unblock-adint-fde22f1d70bffa98-resolve-20260912.md)
has SHA-256 `f7699415ae8a6405e49734b091560a74f16bcdb7dd909997fc3f83bb536eaffe`
and records why local selection would change the study.

## Exact operator-action packet

Supply a tracked immutable manifest and the matching corpus bytes with all
five fields populated:

```yaml
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact executable Unicode and token normalization policy>
version: <immutable release, commit, or source checksum>
corpus: <immutable corpus path/URI and SHA-256 of the exact bytes>
```

Then verify the corpus digest, run dependency preflight and the dictionary-arm
command, and record versions, output hashes, and a typed verdict. Resume the
parent only after that result exists. The bounded command
`cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`
checks six generative cases only and cannot clear the dictionary blocker.

Retry condition: `event:operator-dictionary-input` when the approved five-field
manifest and matching corpus bytes are available.
