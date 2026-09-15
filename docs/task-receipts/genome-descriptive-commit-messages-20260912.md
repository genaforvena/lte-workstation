# Genome descriptive commit messages — 2026-09-12

Task: `genome-descriptive-commit-messages-20260912/make-genome-commit-messages-descriptive`.

## Change

Genome's charter now requires code completion lines and manual MeshLand subjects to describe the
concrete behavior changed and its result. MeshLand's semantic-message gate rejects generic completion
boilerplate, task-ID-only suggestions, and its own path-only fallback. It holds the candidate and
states that a concrete change description is needed; it does not create a misleading commit.

## Verification

- Red-first regression: before the enforcement check, `rtk bash scripts/mesh-land --test` failed with
  `generic owner completion produced a commit instead of holding the candidate` in its isolated
  throwaway repository.
- `rtk bash -n scripts/mesh-land` — passed.
- `rtk bash scripts/mesh-land --test` — `smoke-test: ok`; the fixture verifies a generic Genome
  completion leaves `HEAD` unchanged and reports why it was held. Its branch-override subtest uses a
  temporary worktree and bare origin.
- The live checkout was at `dc3b526eff91f85a9e70393dad10e8a529d63a79` (`origin/main`) immediately
  after the test. A later read-only check found shared `main`/`origin/main` advanced to
  `945de7b3aa3592422500f54bc51bea24657b030a` by an unrelated `scripts/mesh-presence` landing; the
  charter and MeshLand edits for this task remain uncommitted. The branch-override fixture pushed
  only to its throwaway bare origin.

## Limit

The gate rejects common boilerplate and path-only summaries and requires a four-word description.
That is a practical floor, not a semantic parser; Genome still needs to write text that accurately
describes the change.
