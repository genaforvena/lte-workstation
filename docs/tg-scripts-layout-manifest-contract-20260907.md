# Manifest/enumerator contract — 2026-09-07

This is the first, no-move slice of the TG scripts layout work. The manifest command is the
single source of enumeration truth for the two genome source roots: `scripts/` and `job/`.
Consumers are not rewired in this slice; the command exists to make omissions and collisions
observable before a consumer migration.

## Row schema

`manifest/mesh-manifest.schema.json` defines one row with these fields:

| field | contract |
|---|---|
| `source_path` | repository-relative regular-file path under `scripts/` or `job/` |
| `installed_basename` | basename in `~/.local/bin` for installable tools; empty otherwise |
| `domain` | one of `core`, `communication`, `integrations`, `operations`, `tests`, `ux` |
| `kind` | one of `tool`, `unit`, `asset`, `fixture`, `library` |
| `deploy_policy` | `install`, `systemd`, or `none` |
| `cadence_policy` | `header`, `unit`, or `none` |
| `compatibility_owner` | stable consumer/legacy owner label, never empty |

The command emits these fields as tab-separated values after a `# mesh-manifest v1` line. Paths
and rows are sorted. `--check` validates the complete walk and fails on an unknown classification
or duplicate install basename. `--parity` is report-only: it compares installable rows to the
deployed basename under `~/.local/bin` and never mutates either tree.

## Required fixture matrix

The focused test covers all classes that the layout audit identified as dangerous to a direct glob:

| fixture | expected kind/policy | why it matters |
|---|---|---|
| `scripts/mesh-fixture-tool` | `tool` / `install` | current top-level compatibility path |
| `scripts/reticulum/mesh-fixture-nested` | `tool` / `install` | nested tool must not disappear |
| `scripts/demo.service` | `unit` / `systemd` | launcher/unit is not an installed executable |
| `scripts/tests/sample.fixture` | `fixture` / `none` | test material must remain visible but not deploy |
| `scripts/__pycache__/sample.cpython-312.pyc` | `asset` / `none` | generated cache must be classified, not guessed away |
| `job/mesh-fixture-job` | `tool` / `install` | lane directory is a genome source root |

The test also creates a duplicate install basename and requires a loud failure. A file outside
the two roots is intentionally ignored because it is outside the manifest's declared source
boundary, not silently treated as a source row.

## Boundary and rollback

This slice adds no directory moves, deployment, cron changes, service changes, or consumer rewiring.
Rollback removes only the schema, enumerator, focused test, plan, and this contract note. The next
slice is to review the live inventory and wire one existing enumerator consumer to the command.

## Verification captured

```text
(cd /tmp && bash /home/mesh-home/lte-workstation/tests/test-mesh-manifest.sh)
  mesh manifest contract: fixture matrix and duplicate guard pass
python3 -m py_compile scripts/mesh-manifest
scripts/mesh-manifest --check
  mesh-manifest: PASS (1106 complete rows; no duplicate installed basenames)
scripts/mesh-manifest --parity | head -10
  report-only TSV emitted successfully; pipe-close exits cleanly
```

The live tree contains an intentional compatibility pair for `mesh-rns-linkcheck`: the top-level
shim owns the installed basename and the nested canonical implementation is inventoried with
`deploy_policy=none`. Two nested candidates without a top-level owner remain a fatal duplicate,
covered by the synthetic fixture.
