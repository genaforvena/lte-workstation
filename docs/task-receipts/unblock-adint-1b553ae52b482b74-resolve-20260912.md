# Resolver receipt: `unblock/adint/1b553ae52b482b74/resolve`

- Checked: `2026-09-12T01:28:07Z` UTC on `mesh-home`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/1b553ae52b482b74/resolve adint` exited `0`; claimed by adint.
- Result: **BLOCKED/operator-input; current revalidation and exact packet recorded**

## Diagnosis

The parent ledger remains blocked on `operator-input`; its retry condition
requires frozen dictionary inputs and a new artifact-backed study result. The
current `rtk mesh-task check resume unblock/haunt/62c0662129fa8ee9/resolve haunt`
refused with exit `2`.

The fresh filename scan across tiny-fleet study `docs/` and `runs/` found no
dictionary, lexicon, or study-input manifest. Its sole dictionary-named result
is `runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`,
an unrelated application artifact. The parent receipt
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-62c0662129fa8ee9-20260911.md`
has SHA-256 `d1fbdfe4267e4e1c87b1971aab99c49568c5035bb82fe9deea444aa79c06f5d4`.
Prior same-parent receipt
[`unblock-adint-e6cb73fce0948079-resolve-20260912.md`](unblock-adint-e6cb73fce0948079-resolve-20260912.md)
has SHA-256 `a4e59f88df03e580a795d2ed066dd1ef053d298f944dae6c488d4b925bce7f52`
and records the same missing input boundary.

No safe local choice can supply a study dictionary, language, normalization,
version, or corpus without changing the registered experiment.

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
verdict. Resume only after the dictionary arm has its own artifact-backed
result. The bounded command
`cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`
checks six generative cases only and cannot clear this blocker.

Retry condition: `event:operator-dictionary-input` when the approved five-field
manifest and matching corpus bytes are available.
