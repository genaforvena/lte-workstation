# Resolver receipt: `unblock/adint/fde22f1d70bffa98/resolve`

- Checked: `2026-09-12T01:00:07Z` UTC on `mesh-home`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/fde22f1d70bffa98/resolve adint` exited `0`; claimed by adint.
- Result: **BLOCKED/operator-input; current revalidation and exact input packet recorded**

## Diagnosis

The parent remains blocked on `operator-input`. Its current retry condition
requires the five dictionary fields to be supplied and frozen with hashes. The
live `rtk mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt`
refused with exit `2`.

The fresh search under the tiny-fleet study `docs/` and `runs/` found no
dictionary, lexicon, or study-input manifest. The only dictionary-named match
is `runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`,
an unrelated application artifact. The current
`/home/mesh-home/tiny-fleet/scripts/bbywvy_test.py` SHA-256 is
`377521b04612de877b18caf046157d772293e23539f8d11817ee771cad598a8a`; it is
the six-case generative runtime smoke and does not implement the dictionary
arm. The prior same-parent revalidation
[`unblock-adint-8a7d394c7570d40c-resolve-20260912.md`](unblock-adint-8a7d394c7570d40c-resolve-20260912.md)
has SHA-256 `a370b7fc78d6580c8952c464f7e155c1a9ef2b3cbbc8b593c6fe34c76f9b9007`
and documents why no local choice can safely fill the missing study input.

## Exact operator-action packet

Provide a tracked immutable study-input manifest and the matching corpus bytes
with all five fields populated; placeholders are not valid:

```yaml
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact executable Unicode and token normalization policy>
version: <immutable release, commit, or source checksum>
corpus: <immutable corpus path/URI and SHA-256 of the exact bytes>
```

Then verify the corpus digest, run the parent's dependency preflight and
dictionary-arm command, and record versions, output hashes, and a typed
verdict. Resume only after that dictionary result exists. The bounded runtime
command `cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`
checks six generative cases only and cannot clear the dictionary blocker.

Retry condition: `event:operator-dictionary-input` when the complete approved
five-field manifest and matching corpus bytes are available.
