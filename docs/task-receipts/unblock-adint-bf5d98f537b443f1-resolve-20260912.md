# Resolver receipt: `unblock/adint/bf5d98f537b443f1/resolve`

- Checked: `2026-09-12T02:08:04Z` UTC on `mesh-home`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/bf5d98f537b443f1/resolve adint` exited `0`; claimed by `adint`.
- Result: **BLOCKED/operator-input; fresh live recheck and exact operator-action packet recorded**

## Current evidence

`rtk mesh-task status unblock/haunt/fd5d75268b44e1cc` reports the parent as
`blocked`; its resolver is owned by `haunt`, with blocker type `operator-input`.
The parent's retry requires all five dictionary fields frozen with hashes.
`rtk mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt`
exited `2`, so the parent is not eligible to resume.

The fresh search
`rtk rg -l -i 'dictionary source|approved dictionary|lexicon' /home/mesh-home/tiny-fleet/docs /home/mesh-home/tiny-fleet/runs`
found no operator-approved study manifest or matching dictionary corpus. Hits
were application documentation/registry and prior task receipts, including the
parent receipt; these are not study inputs. The parent receipt
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-fd5d75268b44e1cc-20260911.md`
has SHA-256
`b4d851e5e285e407ffa60991e07f32be789babf5bc8947d0a21a763a98e4a18d` and
records the same missing scientific inputs. The tiny-fleet worktree has
pre-existing unrelated edits and untracked files; none were changed.

No safe local source can fill the gap. Choosing a dictionary, language,
normalization, version, or corpus would invent an input and change the study.
The existing six-case generative smoke does not discharge the dictionary arm;
no study or install command was run.

## Exact operator-action packet

Provide a tracked immutable manifest and the exact matching corpus bytes, with
all fields populated:

```yaml
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact executable Unicode and token normalization policy>
version: <immutable release, commit, or source checksum>
corpus: <immutable corpus path/URI and SHA-256 of the exact bytes>
```

When the manifest and corpus are available, verify the corpus digest, run the
parent's dependency preflight and dictionary-arm command, and record versions,
output hashes, and a typed verdict. Resume only after the dictionary arm has
its own artifact-backed result. Retry event:
`event:operator-dictionary-input`.
