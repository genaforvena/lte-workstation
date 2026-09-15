# Resolver receipt: `unblock/adint/04121d2ccec59b9b/resolve`

- Checked: `2026-09-11T21:50Z` UTC on `mesh-home`.
- Resolver was canonical `open`, passed exact-owner validation, and was claimed by `adint`.
- Target parent: `unblock/haunt/2e1cbcd2f8380a3b/resolve`.
- Original work: `haunt-install-unblock-20260907/install-and-retry-tinyfleet`.

## Live diagnosis

The parent remains `BLOCKED` on `operator-input` and names these missing inputs:

```text
dictionary source, language, normalization/version, and corpus
```

The existing parent receipt (`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-haunt-2e1cbcd2f8380a3b-20260911.md`)
records a successful runtime repair and six-case generation artifact, but explicitly leaves the
dictionary arm blocked. A current repository sweep finds only dictionary references in code,
prose, and receipts; no operator-selected dictionary dataset or frozen source/hash is declared for
this task. The available application dictionaries are unrelated inputs and cannot be substituted
without changing the registered experiment.

## Disposition

No safe local prerequisite exists. Selecting a public lexicon, language, normalization, version, or
corpus would fabricate the missing experimental input. No package install, corpus download, parent
resume, or unrelated study task was performed. The resolver is blocked with the concrete retry
condition:

```text
operator supplies dictionary source, language, normalization/version, and corpus path/hash;
then rerun dependency preflight, record source/path/hash, and resume the parent install-and-retry task
```
