# Genome dashboard one-shot probe bound

Date: 2026-09-15
Task: `genome-dash-one-shot-20260915/bound-genome-one-shot-land-probe`

## Change

`scripts/mesh-dash` now bounds the genome frame's read-only `mesh-land` and
`mesh-sync-tools` probes to two seconds by default, with one-second kill
escalation. Timeout and non-zero results are rendered explicitly in the frame;
the probe cannot hold `mesh-dash --once genome` indefinitely.

## Verification

- Red: `tests/test-mesh-dash-genome-one-shot-bounds-land-probe.sh` timed out at
  five seconds against the old 20-second probes (rc=124).
- Green: the same fixture test passed with both probe timeout arms.
- Green: `timeout 12s scripts/mesh-dash --once genome` returned rc=0 and
  rendered the full frame, including `mesh-land probe timed out after 2s`.
- Green: `scripts/mesh-dash --test-fast`.
- Green: `bash -n` and `git diff --check` for the changed source and test.
