# Resolver receipt: `unblock/adint/d33790336f0fc76f/resolve`

- Checked: `2026-09-12T01:35:17Z` UTC on `mesh-home`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Dispatch check: `mesh-task check dispatch unblock/adint/d33790336f0fc76f/resolve adint` exited `0`; claimed as adint.
- Result: **BLOCKED/operator-input; exact operator packet and retry condition recorded**

## Current evidence

The parent status remains `blocked` on operator input. A fresh
`mesh-task check resume unblock/haunt/62c0662129fa8ee9/resolve haunt` exited `2`.
Its owner-authored parent receipt at
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-62c0662129fa8ee9-20260911.md`
has SHA-256 `d1fbdfe4267e4e1c87b1971aab99c49568c5035bb82fe9deea444aa79c06f5d4`
and specifies that no operator-approved dictionary source, language,
normalization, version, or corpus was supplied.

The fresh filename scan `rg --files docs runs | rg -i
'(dictionary|lexicon|corpus|manifest)'` found `docs/mood-corpus-2026-09-06.md`
and `runs/applications/ticket-extraction/baseline-20260908/regex-dictionary-raw.jsonl`
among other manifest paths. The mood corpus is explicitly for operator-mood
classification; the regex dictionary is an application artifact. Neither is
the approved dictionary input and corpus for this study, so neither can satisfy
the parent blocker. No choice of scientific input is safe to infer locally.

The prior same-parent resolver receipt
`docs/task-receipts/unblock-adint-1b553ae52b482b74-resolve-20260912.md`
has SHA-256 `80cd9ded00b23c216e15f51fae8988a290e5e0826cc9d1b31ae0a8af3caa46ae`
and already records the full exact-input packet. This receipt revalidates the
blocker and points to that packet rather than creating competing study inputs.

## Exact operator-action packet and retry

Provide a tracked, immutable manifest and matching corpus bytes with all fields
populated:

```yaml
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact executable Unicode and token normalization policy>
version: <immutable release, commit, or source checksum>
corpus: <immutable corpus path/URI and SHA-256 of the exact bytes>
```

Once supplied, verify the corpus digest, run the parent's dependency preflight
and dictionary-arm command, and record versions, output hashes, and a typed
verdict. Resume the parent only after the dictionary arm has its own
artifact-backed result. The existing six-case smoke is insufficient.

Retry condition: `event:operator-dictionary-input` when the approved five-field
manifest and matching corpus bytes are available.
