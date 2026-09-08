# MeshLand semantic commit-message guard — 2026-09-08

## Problem

MeshLand could describe a landing solely as `change N additions, M deletions` when no useful
completion context was available. A diff statistic describes the size of a patch, not the intent
or effect of the independently revertible unit; it makes `git log` unhelpful to an operator.

## Change

`scripts/mesh-land` now treats that exact diff-statistic shape as opaque in both a commit subject
and `Why/context:`. Its shared `commit_message_informative` predicate rejects the message before
`git commit`; the fallback is checked by the same predicate, so it cannot invent semantic intent.
The landing holds loudly until the candidate has a path-linked board completion or an explicit,
meaningful subject.

## Verification

- `bash -n scripts/mesh-land` exited 0.
- `scripts/mesh-land --test` exited 0. Its hermetic Git fixture rejects diff-stat-only subject and
  context variants, while accepting a path-specific semantic subject and context.
- `git diff --check -- scripts/mesh-land` exited 0.

## Scope

This applies to MeshLand-generated commits. Historical commits are immutable and are not rewritten;
new landings must name the changed path and semantic reason in their subject and body.
