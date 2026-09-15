# Resolver receipt: `unblock/adint/8a7d394c7570d40c/resolve`

- Checked: `2026-09-12T00:54:25Z` UTC on `mesh-home`
- Parent: `unblock/haunt/fd5d75268b44e1cc/resolve`
- Owner check: `mesh-task check dispatch unblock/adint/8a7d394c7570d40c/resolve adint` exited `0`; claimed by adint.
- Result: **BLOCKED/operator-input; exact operator-action packet recorded below**

## Live diagnosis

`rtk mesh-task status unblock/haunt/fd5d75268b44e1cc` still reports the parent
blocked on `operator-input`; its retry condition requires the five dictionary
fields to be supplied and frozen with hashes. The explicit
`rtk mesh-task check resume unblock/haunt/fd5d75268b44e1cc/resolve haunt`
refused with exit `2`.

The prior target receipt at
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-fd5d75268b44e1cc-20260911.md`
has SHA-256 `b4d851e5e285e407ffa60991e07f32be789babf5bc8947d0a21a763a98e4a18d`
and records the same missing approved dataset. Current study script
`/home/mesh-home/tiny-fleet/scripts/bbywvy_test.py` has SHA-256
`377521b04612de877b18caf046157d772293e23539f8d11817ee771cad598a8a`; it is
the six-case runtime smoke, not a dictionary-arm study. The study-docs/runs
filename search found no dictionary, lexicon, or study-input manifest. Its
one dictionary-named hit was
`runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`,
whose sample rows are ticket-extraction predictions for Acme Widget tickets,
not an approved dictionary corpus for this study.

Selecting a source, language, normalization, version, or corpus locally would
invent a scientific input and alter the experiment. The unrelated application
artifact cannot satisfy the missing parent input. No safe local prerequisite
can clear the blocker.

## Exact operator-action packet

Provide a tracked immutable study-input manifest and matching corpus bytes with
all five fields populated; placeholders are not inputs:

```yaml
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact executable Unicode and token normalization policy>
version: <immutable release, commit, or source checksum>
corpus: <immutable corpus path/URI and SHA-256 of the exact bytes>
```

Then verify the corpus digest, run the dependency preflight and dictionary-arm
command, and record versions, output hashes, and a typed verdict. Only after
that artifact-backed dictionary result exists should this parent be resumed.
The requested bounded runtime command is
`cd /home/mesh-home/tiny-fleet && timeout 240 .venv/bin/python scripts/bbywvy_test.py`;
it checks only the six generative cases and does not discharge the dictionary
arm. Do not run it as a substitute for the missing input.

Retry condition: `event:operator-dictionary-input` when the complete approved
five-field manifest and matching corpus bytes are available.
