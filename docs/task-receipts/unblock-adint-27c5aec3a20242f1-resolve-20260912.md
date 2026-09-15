# Resolver receipt: `unblock/adint/27c5aec3a20242f1/resolve`

- Checked: `2026-09-12T00:51:52Z` UTC on `mesh-home`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/27c5aec3a20242f1/resolve adint` exited `0`; claimed with `MESH_TASK_ACTOR=adint mesh-task take unblock/adint/27c5aec3a20242f1 resolve`.
- Result: **BLOCKED/operator-input; exact operator-action packet recorded below**

## Diagnosis

The parent remains blocked on `operator-input`. The current parent status is
`unblock/haunt/62c0662129fa8ee9 [blocked]`; its only step is blocked with retry
condition “after operator supplies frozen dictionary inputs”. The explicit
`rtk mesh-task check resume unblock/haunt/62c0662129fa8ee9/resolve haunt`
refused with exit `2`.

The installed study script at `/home/mesh-home/tiny-fleet/scripts/bbywvy_test.py`
contains six generative prompts and no dictionary arm. Its SHA-256 is
`377521b04612de877b18caf046157d772293e23539f8d11817ee771cad598a8a`. A search
of the tiny-fleet study `docs/` and `runs/` files found no dictionary/lexicon
input manifest. The existing parent receipt
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-62c0662129fa8ee9-20260911.md`
has SHA-256 `d1fbdfe4267e4e1c87b1971aab99c49568c5035bb82fe9deea444aa79c06f5d4`
and records the same missing scientific inputs. The six-case smoke cannot
resolve that dictionary arm.

No safe local prerequisite can fill this gap: selecting a dictionary source,
language, normalization, version, or corpus would invent study input. Do not
substitute the unrelated D02 concept list or install an unpinned package.

## Exact operator-action packet

Provide a tracked immutable manifest and the matching corpus bytes with all
five fields populated (placeholders are not valid):

```yaml
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact executable Unicode and token normalization policy>
version: <immutable release, commit, or source checksum>
corpus: <immutable corpus path/URI and SHA-256 of the exact bytes>
```

Once present, verify that corpus digest; run the parent's dependency preflight
and dictionary-arm command; record versions, output hashes, and a typed verdict.
Only after that artifact-backed dictionary result exists should the parent be
resumed. The bounded smoke command is
`cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`;
it only checks the six generative cases and cannot clear this blocker.

Retry condition: `event:operator-dictionary-input` when the completed,
operator-approved five-field manifest and matching corpus are available.
