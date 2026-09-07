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
- Exact source hashes: HEAD blob before change `f265864f37669b09d8f931f2c390cc6b02fcbb86`;
  working-tree blob after change `f91b8154851200806e8f22516d97b4bb141be500`;
  working-tree SHA-256 `9306cfb82f4cd1670fbdee8a3962c1e7cf30c7f0a3e4df69638895f934f2b7f4`.
- Deployed copy remains unchanged pending the normal MeshLand landing gate: SHA-256
  `a115eadb9dd1eb6c14e0222fdca02728b46eecec3ffab247eda25131a067267a`.
- No after-landing commit hash exists yet: this work is intentionally left uncommitted so the
  normal `mesh-land --apply` / push gates can create it without hand-editing history.

The implementation and this artifact remain subject to the normal MeshLand commit/push gate.
