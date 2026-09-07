# MeshLand informative commit messages — 2026-09-07

Task: `meshland-informative-commit-messages`.

## Before

The live landing commit `7a69ca72d0028fdaa0a0dac6519c119ad4c38f7d` had subject:

```text
mesh-land: land 1 settled stream fix(es): mesh-nic-rx-loss
```

Its body described the generic landing policy, but did not identify the concrete change,
affected path, or verification result. That made the commit opaque outside the steward's
runtime context.

## Contract and implementation

`scripts/mesh-land` now generates every landing commit with these non-empty sections:

- `Why/context:` — why the steward is committing the change;
- `What changed:` — repo-relative paths and per-path diff counts/removal status;
- `Affected scope:` — exact repo-relative paths in the commit;
- `Verification/result:` — settlement, parse/test status, path-limited commit scope, and deployment result.

The commit path rejects an opaque generated message before invoking `git commit`, then uses a
deterministic fallback builder. The end-to-end `--test` fixture asserts all four sections, rejects
an opaque proposal, exercises the fallback, and asserts that the exact landed path is named in the
body. Staged paths outside the gated set remain staged and are still reported.

## Before/after message shape

Before (commit `7a69ca72d0028fdaa0a0dac6519c119ad4c38f7d`):

```text
Stream-produced genome fixes that posted [done] but weren't committed (...).
Settled (...), parse-clean, steward-reviewed. Landed + deployed by mesh-land.
```

After (fixture shape; exact path is now required):

```text
Why/context: stream-produced genome fixes posted [done] but not yet committed; commits are
steward-centralised by design.
What changed: landed the gated candidate set (docs/reviews/fix-2026-01-01.md).
Affected scope: docs/reviews/fix-2026-01-01.md
Verification/result: settled (...), parse-clean where applicable, steward-reviewed; the commit
is path-limited to the gated set and landed + deployed by mesh-land.
```

## Verification

- Red-first regression: the fixture failed against the old generator with
  `commit body does not name the landed path in its scope/result evidence`.
- Green: `scripts/mesh-land --test` → `smoke-test: ok` (exit 0).
- Syntax: `bash -n scripts/mesh-land` → exit 0.
- Exact source/deployed SHA-256 after landing: `9306cfb82f4cd1670fbdee8a3962c1e7cf30c7f0a3e4df69638895f934f2b7f4`.
- The implementation and artifact landed through the normal MeshLand commit/push gate in
  `75d8167f468f1696d352e12bb7496b519bc4331a`; `origin/main` matches HEAD.
- That commit also carried the pre-existing study artifact
  `docs/study-self-healing-systems-hold-retirement-20260907.md`.

## Scope correction — every MeshLand commit

The first implementation enforced section labels but still permitted the latest subject shape:

```text
mesh-land: land 1 settled stream fix(es): <path>
```

That was still too opaque in `git log`: the subject did not say what changed, and the body reused
the same generic landing rationale. The contract now requires every generated MeshLand subject to
use `land N changed: <path-and-diff-summary>`, marks deleted paths with `-path: removed`, and
rejects the old generic subject/context pair. The throwaway-repository regression asserts the
subject names the concrete changed path and that the removal fixture names deleted paths too.

The normal gate for this correction is `scripts/mesh-land --test`, `bash -n scripts/mesh-land`,
then `mesh-land --apply` and `mesh-land --push`; the resulting landing commit and source SHA-256
are recorded below after the gate completes.

## Correction verification

- Red-first target: the previous generator's generic `land N settled stream fix(es)` subject and
  boilerplate `Why/context` now fail `commit_message_informative`.
- Green: `scripts/mesh-land --test` → `smoke-test: ok` (exit 0); `bash -n scripts/mesh-land` → exit 0.
- Normal landing: `mesh-land --apply` committed and pushed `143dce65edd69665b72fb24002b7accb86f05a5c`;
  `mesh-land --push` then reported `nothing settled+clean to land` (exit 0).
- `HEAD=origin/main=143dce65edd69665b72fb24002b7accb86f05a5c`.
- Source and deployed `scripts/mesh-land` SHA-256: `0fde7fb6188a3be8fcfc4a7f6340240c30a1bca1230f39f41523ef72ac209852`.
