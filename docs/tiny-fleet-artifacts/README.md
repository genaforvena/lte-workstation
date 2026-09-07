# Tiny-fleet corpus lock artifacts

This directory is the offline first step of the expansion plan.

- `corpus-candidates.tsv` freezes the pilot candidate set. The local
  `lte-workstation` and CC0 `tiny-fleet` rows are resolved at immutable commits;
  external rows are explicit deferred exclusions until immutable commits and
  license evidence are collected.
- `fixture-input/` is a deterministic protocol fixture, not a redistributable
  source corpus. It exercises empty files, duplicate blobs, and generated-file
  exclusion.

Rebuild the node-local artifacts without network access:

```bash
TINY_FLEET_DIR=/tmp/tiny-fleet-lock scripts/mesh-tiny-fleet corpus-manifest
TINY_FLEET_DIR=/tmp/tiny-fleet-lock scripts/mesh-tiny-fleet fixture-build
TINY_FLEET_DIR=/tmp/tiny-fleet-lock scripts/mesh-tiny-fleet corpus-lock
```

`corpus-lock` additionally emits `corpus.lock.json`, `source-manifest.tsv`, and
`fixture-report.json`. These outputs are deterministic: two clean-room rebuilds
must be byte-identical. The lock fails closed on unresolved candidates, mutable
refs, missing SPDX declarations, or absent license evidence.
