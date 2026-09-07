# mesh-land semantic commit verification

Date: 2026-09-07

The landing policy now creates one commit per settled semantic unit. Ordinary candidates are
independent units; a detected rename keeps its addition and deletion together so it cannot
half-land. Existing settle, parse, rollback, substrate, autoland test, path-limited staging,
push-heal, atomic deploy, autowire, and board outcome gates remain in the landing path.

Commit subject examples produced by the hermetic fixtures (readable from `git log --oneline`):

- `mesh-land: add scripts/mesh-zz-push as an independently revertible unit`
- `mesh-land: update docs/reviews/fix-2026-01-01.md as an independently revertible unit`
- `mesh-land: move scripts/mesh-zz-moved to job/mesh-zz-moved as one atomic unit`
- `mesh-land: remove docs/gone.md without leaving a deployed copy`

The subject carries the landing intent, not only the filename. This keeps the one-line history
useful without pretending that MeshLand can infer the internal purpose of arbitrary uncommitted
code; exact scope and gate evidence remain in the body.

Each body has these fields:

```text
Why/context: <why this settled unit is being landed>
Scope: <exact unit path or paths>
Verification: <settle/parse/review/path-limited result>
```

Verification performed:

```text
rtk bash -n scripts/mesh-land
rtk bash scripts/mesh-land --test
smoke-test: ok
```

The focused fixture also confirms that an ungated staged path remains staged and is explicitly
reported, two settled candidates land in two separately named commits, a rename is one two-path
commit, and a lone deletion is its own removal commit. No live repository landing, deployment, or
push was performed by this verification artifact.
