# Frozen independent-repository sample

Freeze recorded 2026-09-08T05:09Z UTC for task
`tinyfleet-architecture-drift-review-20260907/freeze-independent-repository-sample`.

## Preregistered selection

The selection was taken from `docs/tiny-fleet-artifacts/corpus-candidates.tsv` and the
2026-09-07 expansion plan: public Git repositories, mature/high-commit, source-oriented,
license evidence present, and independent of `lte-workstation` and `tiny-fleet`. The first
three candidates with reachable immutable revision and downloadable license evidence were
admitted: curl, ripgrep, and jq. No popularity ranking was recomputed after observing source
contents. The sample is a bounded pilot of three, not the 24-repository expansion target.

## Freeze rule and comparable window

The snapshot selector is the latest commit on the preregistered default branch whose committer
timestamp is strictly before `2026-09-08T00:00:00Z`. Acquisition was performed in one collection
run beginning at `2026-09-08T05:09Z` UTC. Each row therefore has the same temporal cutoff and
acquisition protocol; commit dates differ because repositories evolve independently. Git object
identity (commit/tree) is authoritative; branch names are descriptive only.

`source-manifest.tsv` records the recursive Git-tree inventory summary. `snapshot-windows.tsv`
records the common cutoff and each selected commit date. `exclusions.tsv` records candidates not
admitted and why. `source-manifest.tsv` does not redistribute source; it records reproducible
object identities and counts.

## Honest unavailable inputs

- Full historical three-snapshot temporal windows were not collected in this freeze; only the
  common-cutoff snapshot is admitted. Longitudinal temporal analysis is `BLOCKED`.
- GitHub’s license classifier returned `NOASSERTION` for curl and jq. Their COPYING text and
  hashes are present, but SPDX normalization is `UNAVAILABLE` for those two rows.
- No popularity metadata, full per-file blob manifest, or model-analysis output is claimed here;
  those belong to later steps.

## Reproduction

Re-fetch each URL, resolve the recorded commit, enumerate `git ls-tree -r <commit>`, fetch the
recorded license path at that commit, and hash a tar archive of that commit. Network acquisition
is required; the hashes in this directory are the 2026-09-08 evidence, not a claim that GitHub is
immutable storage.
