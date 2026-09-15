# Resolver receipt: `unblock/adint/eb4c5cff68622566/resolve`

- Checked: `2026-09-12T01:48:49Z` on `mesh-home`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Dispatch check: `mesh-task check dispatch unblock/adint/eb4c5cff68622566/resolve adint` exited `0`; claimed as `adint`.
- Result: **BLOCKED/operator-input; exact input request sent to operator**

## Fresh state

`mesh-task status unblock/haunt/62c0662129fa8ee9` still reports the parent as `blocked`,
owned by `haunt`, with blocker `operator-input`. The owner resume gate,
`mesh-task check resume unblock/haunt/62c0662129fa8ee9/resolve haunt`, exited `2`.
The latest board search for `operator-dictionary-input` contains no supplied manifest or
corpus after the 01:45 UTC handoff. A filename scan of `/home/mesh-home/tiny-fleet`
found no dictionary, lexicon, vocabulary, or word-list input outside task receipts;
the declaration search found only prior receipts, not an approved input. No scientific
input can be selected locally without inventing the operator's choice.

## Operator packet and next action

At 01:48 UTC, `mesh-voice-tx` sent the operator a Russian voice note and duplicated text
requesting these frozen inputs:

```text
source: operator-approved dictionary/lexicon URI or repository-relative path
language: ISO language or explicit language set
normalization: exact executable Unicode and token-normalization policy
version: immutable release, commit, or source checksum
corpus: immutable corpus path/URI plus SHA-256 of the exact bytes
```

On receipt, validate the manifest and corpus digest, run the parent's dependency preflight
and dictionary arm, then capture an artifact-backed typed result. Only after that result
exists may the parent resume. The bounded retry command is:

```bash
cd /home/mesh-home/tiny-fleet
timeout 240 .venv/bin/python scripts/bbywvy_test.py
```

No package, corpus, runtime, or model was changed; the study command was not run because
the required inputs are absent. The parent remains blocked pending `event:operator-dictionary-input`.
