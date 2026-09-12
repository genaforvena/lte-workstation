# Structural and lexical source measures

This artifact runs a deterministic static extraction over the two repositories resolved in the
frozen corpus lock. It reads Git objects at the locked commits, so dirty working-tree files do not
enter the measurement. It does not make a temporal drift or cross-repository population claim.

Reproduce from the repository root with:

```sh
python3 scripts/tinyfleet_structural_lexical.py \
  --corpus-manifest docs/tiny-fleet-artifacts-20260907/corpus-lock/corpus-manifest.json \
  --protocol docs/tiny-fleet-protocol.md \
  --output-dir docs/tiny-fleet-artifacts-20260912/structural-lexical \
  --bootstrap-rounds 2000
```

The lock resolves `lte-workstation` at `e8f47364e5a0f224c1bd03331df592272a187df5` and
`tiny-fleet` at `991b08f6e9e68ae8743ee92f5bcebbed2254324b`. Across those pinned trees, 1,515 tracked
file rows were enumerated; 606 passed the UTF-8 text filter and 909 were excluded for unsupported
extensions. The included rows contain 5,337,031 bytes and 759,265 lexical tokens. Per-repository,
per-language, and pooled language-stratum summaries are in the TSV files; `file-rows.tsv` preserves
the file-level denominators, exclusions, hashes, parser coverage, and measured counts. Term
frequencies are lowercased matches of the recorded identifier-like regex; they are lexical terms,
not parser-resolved identifiers.

The supported structural measures are file and byte counts, extension/language mix, line counts,
Python AST node/parse counts, and lexical marker counts for comments, tests, errors, imports, and
declarations where the extractor has a language-specific rule. Marker counts are text heuristics,
not semantic test or comment coverage. Missing per-file import/declaration parsers are recorded as
`na`; the Python AST is the only parser-backed arm. Bootstrap intervals describe file-level
variation within each locked repository/language slice. They do not estimate temporal change or
between-repository uncertainty.

Paired snapshot changes, JSD, new/gone vocabulary, architecture/package/import graph edits, API
matching, component churn, and LoRA/QLoRA remain explicitly `na` or `blocked`: the corpus lock has
only one snapshot per resolved repository, no cross-language graph resolver is in this pass, and no
adapter/run evidence exists. The run ID and input hashes are in `summary.json`. No source text is
copied into this artifact.

The synthetic Git-repository contract and byte-for-byte repeatability check are exercised by
`python3 tests/test-tinyfleet-structural-lexical.py`.
