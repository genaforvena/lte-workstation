# Manifest autowire, land, and vitality consumer slice — 2026-09-12

Task: `tg-scripts-layout-migration-20260912/manifest-autowire-land-vitality` (owner: genome).

The three consumers now use the checked manifest as their shared source inventory. Autowire maps
installable basenames to their classified source paths and checks cadence declarations across all
installable rows, including nested and `job/` tools; deployed node-local candidates still follow the
existing no-source path. Mesh-land validates the full inventory and uses classified `scripts/` and
`job/` paths when selecting source candidates, while preserving its existing docs, skills, installers,
and deleted-path handling. Vitality uses installable manifest rows for its live tool counts and source
coverage analyses, including witness, rhizome, protocol, and RAF scans. No files or directories moved,
and no live cadence or crontab was changed.

Unknown classifications and duplicate owners fail in the shared reader before it emits paths. The
consumer test covers install-source lookup and complete source coverage, including empty-output
refusal on an unknown row. Existing compatibility paths and domain-specific gates remain in place.

Verification performed:

```text
scripts/mesh-manifest --check
  PASS (1199 complete rows; no duplicate installed basenames)
bash -n scripts/mesh-autowire scripts/mesh-land scripts/mesh-vitality scripts/lib/mesh-manifest-reader.sh
  PASS
scripts/mesh-autowire --test
  PASS (smoke-test: ok)
scripts/mesh-land --test
  PASS (smoke-test: ok; branch-override integration fixture passed)
scripts/mesh-vitality --test
  PASS (smoke-test: ok; synthetic manifest-backed phylum and rhizome corpora passed; witness, protocol,
        and RAF live scans completed)
bash tests/test-mesh-manifest-consumers.sh (run from /tmp)
  PASS (unknown-row refusal; sync-tools and doctor --test paths passed outside the checkout)
(cd /tmp && /home/mesh-home/lte-workstation/scripts/mesh-autowire --test)
  PASS (smoke-test: ok)
(cd /tmp && /home/mesh-home/lte-workstation/scripts/mesh-land --test)
  PASS (smoke-test: ok; branch-override integration fixture passed)
(cd /tmp && /home/mesh-home/lte-workstation/scripts/mesh-vitality --test)
  PASS (smoke-test: ok)

Real cadence/reflex check:
  source scripts/mesh-land and deployed ~/.local/bin/mesh-land both declare 3-59/15 * * * *.
  ~/.mesh/reflexes.cron:148 declares the same cadence for mesh-land --autoland.
  An isolated HOME with only its crontab fixture changed to 7 * * * * produced:
    DIVERGED mesh-land: header says 3-59/15 * * * *, crontab:1 runs 7 * * * *
  The isolated check exited 0 and left the real schedule untouched.

Landing and post-deploy verification:
  mesh-land committed the six scoped source/test files across commits 4908bc2, 4aaaf62,
  47670f2, f2cf477, 30d4eb6, and 213ca4a (with concurrent mesh-land activity advancing main in between).
  Manifest parity reports deployed mesh-autowire, mesh-land, and mesh-vitality as `same`; the
  shared reader is a source library and is not installed as a command.
  A post-deploy `mesh-land --check` exited 1 (its quiet settled-strand signal). The check posted
  four separate steward-required candidates: mesh-board (no --test), mesh-hh-drive (--test failing),
  mesh_labor_reconcile.py (non-executable source), and tinyfleet_split_audit.py (no --test).
  These are outside this task; the failing and unverified candidates were not landed here.
```

Rollback: revert this slice's landing commit, then run `mesh-sync-tools --apply` to restore the
previous deployed consumers. The change adds no source directories and alters no schema, unit, or
reflex line, so there is no move or scheduler rollback. The task-specific `[task]` posts in
`~/.mesh/chat.log` contain no suggested commit subject; the landing uses mesh-land's path-specific
semantic message.
