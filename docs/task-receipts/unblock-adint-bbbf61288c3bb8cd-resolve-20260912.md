# Resolver receipt: `unblock/adint/bbbf61288c3bb8cd/resolve`

- Checked: `2026-09-12T00:57:48Z` UTC on `mesh-home`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/bbbf61288c3bb8cd/resolve adint` exited `0`; claimed with `MESH_TASK_ACTOR=adint mesh-task take unblock/adint/bbbf61288c3bb8cd resolve`.
- Result: **BLOCKED/operator-input; current revalidation and exact operator packet recorded**

## Current diagnosis

The parent remains `blocked` on `operator-input`; its retry condition still
requires frozen dictionary inputs and a new artifact-backed result. The current
`rtk mesh-task check resume unblock/haunt/62c0662129fa8ee9/resolve haunt`
refused with exit `2`.

The fresh filename search across tiny-fleet study `docs/` and `runs/` found no
dictionary, lexicon, or study-input manifest. Its only dictionary-named result
is
`runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`;
the inspected row is an Acme Widget ticket prediction, not a dictionary corpus
selected for this study. The existing parent receipt
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-62c0662129fa8ee9-20260911.md`
has SHA-256 `d1fbdfe4267e4e1c87b1971aab99c49568c5035bb82fe9deea444aa79c06f5d4`
and records the same blocker. The current
`/home/mesh-home/tiny-fleet/scripts/bbywvy_test.py` SHA-256 is
`377521b04612de877b18caf046157d772293e23539f8d11817ee771cad598a8a`; it is
the six-case generative smoke and does not implement the dictionary arm.

No safe local prerequisite can supply missing scientific inputs. Choosing a
source, language, normalization, version, or corpus would change the experiment;
the unrelated ticket-extraction artifact cannot be substituted.

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

After delivery, verify the corpus digest, run the dependency preflight and
dictionary-arm command, and record versions, output hashes, and a typed verdict.
Resume the parent only after that dictionary result exists. The bounded command
`cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`
checks only the six generative cases and cannot discharge this blocker.

Retry condition: `event:operator-dictionary-input` when the complete approved
five-field manifest and matching corpus are available.
