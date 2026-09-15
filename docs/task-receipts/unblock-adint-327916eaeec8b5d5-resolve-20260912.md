# Resolver receipt: `unblock/adint/327916eaeec8b5d5/resolve`

- Checked: `2026-09-12T01:02:39Z` UTC on `mesh-home`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/327916eaeec8b5d5/resolve adint` exited `0`; claimed by adint.
- Result: **BLOCKED/operator-input; current revalidation and operator packet recorded**

## Diagnosis

The live parent remains blocked on `operator-input`; its retry condition says to
wait for frozen dictionary inputs and then capture a new artifact-backed result.
`rtk mesh-task check resume unblock/haunt/62c0662129fa8ee9/resolve haunt`
refused with exit `2`.

The fresh search across tiny-fleet study `docs/` and `runs/` found no
dictionary, lexicon, or study-input manifest. Its sole dictionary-named result
is `runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`;
prior adint receipt
[`unblock-adint-bbbf61288c3bb8cd-resolve-20260912.md`](unblock-adint-bbbf61288c3bb8cd-resolve-20260912.md)
(`acb51c26932d7bb13f873f756711c7e5cfabf596447b91124f210f2bbd14f234`)
records an inspected sample showing that file is ticket-extraction output,
not this study's corpus. The current
`/home/mesh-home/tiny-fleet/scripts/bbywvy_test.py` has SHA-256
`377521b04612de877b18caf046157d772293e23539f8d11817ee771cad598a8a` and
contains the six-case generative smoke, not a dictionary arm. The existing
parent receipt has SHA-256
`d1fbdfe4267e4e1c87b1971aab99c49568c5035bb82fe9deea444aa79c06f5d4`.

No safe local prerequisite can choose scientific inputs without altering the
experiment. The unrelated ticket-extraction artifact is not a valid substitute.

## Exact operator-action packet

Provide a tracked immutable study-input manifest and matching corpus bytes with
all fields populated:

```yaml
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact executable Unicode and token normalization policy>
version: <immutable release, commit, or source checksum>
corpus: <immutable corpus path/URI and SHA-256 of the exact bytes>
```

After those inputs arrive, verify the corpus digest, run dependency preflight
and the dictionary-arm command, and record versions, output hashes, and a typed
verdict. Resume the parent only after the dictionary arm has its own verified
result. The bounded command
`cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`
checks six generative cases only and cannot clear the dictionary blocker.

Retry condition: `event:operator-dictionary-input` when the approved five-field
manifest and matching corpus bytes are available.
