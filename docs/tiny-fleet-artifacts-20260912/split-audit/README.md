# Tiny-fleet fixture split audit

This is deterministic, offline test evidence for the expansion chain. The fixtures are synthetic
test inputs; they make no claim about a usable research corpus or redistribution rights. The audit
checks a clean train/held-out split across repository, blob SHA-256, a strict UTC time boundary, and
prompt family. Separate adversarial fixtures prove each axis rejects overlap, a duplicate record ID
is excluded, generated and malformed JSONL are excluded, and exact/near-duplicate content controls
fire across otherwise distinct metadata.

The near-duplicate control uses Jaccard similarity over lowercase alphanumeric token 3-gram sets
with a fixed threshold of 0.75. The time condition is `max(train.time) < min(heldout.time)` after converting
timezone-aware timestamps to UTC. Hashes and all observed results are in `output/fixture-report.json`
and `output/fixture-hashes.tsv`.

Rebuild into a fresh directory and compare the report bytes to verify determinism:

```bash
TINY_FLEET_DIR=/tmp/tinyfleet-split-audit scripts/mesh-tiny-fleet split-audit
```

The canonical report was built directly from `fixture-input/` with
`scripts/tinyfleet_split_audit.py`; wrapper wiring is exercised by
`tests/test-tinyfleet-split-audit.py`.
