# Haunt dictionary unblock receipt — adint/58601f297f9dd0d6

- Resolver: `unblock/adint/58601f297f9dd0d6/resolve`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Checked: `2026-09-12T00:29Z`
- Result: **BLOCKED/operator-input**

## Revalidation and required input

The parent remains blocked on `operator-input`; the explicit resume check
returned exit 2. The dictionary arm still lacks five frozen scientific inputs:

```text
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact Unicode/token normalization policy>
version: <immutable release, commit, or content checksum>
corpus: <immutable corpus path/URI plus SHA-256>
```

The exact operator-action packet and bounded retry command are recorded in
[`unblock-adint-398efe9f5089c41b-resolve-20260912.md`](unblock-adint-398efe9f5089c41b-resolve-20260912.md).
Selecting a dataset or normalization policy here would invent the study input.

After the operator supplies the completed manifest and matching corpus bytes,
verify the corpus digest, run the parent dependency preflight and dictionary
arm, and record their outputs and hashes. The six-case runtime smoke alone does
not clear this blocker. Resume the parent only after the dictionary arm has its
own verified result. Retry this resolver on
`event:operator-dictionary-input`.
