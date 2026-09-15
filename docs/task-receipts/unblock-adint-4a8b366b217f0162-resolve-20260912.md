# Resolver receipt: `unblock/adint/4a8b366b217f0162/resolve`

- Checked: `2026-09-12T01:43:35Z` UTC on `mesh-home`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve`
- Dispatch check: `mesh-task check dispatch unblock/adint/4a8b366b217f0162/resolve adint` exited `0`; claimed as `adint`.
- Result: **BLOCKED/operator-input; exact operator packet and retry condition recorded**

## Current evidence

The parent remains blocked on the dictionary input. A fresh
`mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt` exited `2`.
Its owner-authored receipt at
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-fd5d75268b44e1cc-20260911.md`
has SHA-256
`b4d851e5e285e407ffa60991e07f32be789babf5bc8947d0a21a763a98e4a18d`.
That receipt says the runtime repair and six-case smoke pass, while the dictionary arm
still lacks an approved source, language, normalization, immutable version, and corpus.

The latest board search for `event:operator-dictionary-input` showed prior retry
instructions but no supplied manifest or matching corpus. The current repository filename
scan found study corpora and application artifacts, but no operator-approved dictionary
input. Existing mood and application dictionaries are for other tasks and are not valid
substitutes. The operator's fact base in `self-adint/docs/brief-2026-08-15-operator.md`
does not choose a source or language. Selecting one here would invent a scientific input,
so the parent must stay parked until the operator supplies it.

## Exact operator-action packet and retry

Provide a tracked, immutable manifest and the exact matching corpus bytes, with every field
populated:

```yaml
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact executable Unicode and token normalization policy>
version: <immutable release, commit, or source checksum>
corpus: <immutable corpus path/URI and SHA-256 of the exact bytes>
```

After receipt, verify the corpus digest, run the parent's dependency preflight and dictionary
arm, and record versions, output hashes, and a typed verdict. Resume the parent only if that
arm has its own artifact-backed result. The existing runtime retry command is:

```bash
cd /home/mesh-home/tiny-fleet
timeout 240 .venv/bin/python scripts/bbywvy_test.py
```

Retry condition: `event:operator-dictionary-input` with the approved five-field manifest and
matching corpus bytes available.
