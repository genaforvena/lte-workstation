# Manifest sync/doctor consumer slice — 2026-09-12

Task: `tg-scripts-layout-migration-20260912/manifest-sync-doctor` (owner: genome).

`mesh-sync-tools` now derives deploy candidates from installable-tool rows in the checked manifest.
It validates the complete inventory before consuming paths, uses the same exact manifest paths for
recent-commit WIP suppression, and stops loudly if enumeration fails. Nested tools are included;
a top-level compatibility shim retains ownership of its basename.

`mesh-doctor` now takes source files for orphan, executable-bit, and source lint checks from the
checked manifest. It retains direct legacy source files and adds nested installable tools and systemd
units; an invalid or unavailable manifest refuses the affected scan instead of using a partial glob.
The shared reader at `scripts/lib/mesh-manifest-reader.sh` validates the v1 header, full row schema,
allowed classifications, install/unit policy consistency, and duplicate installed basenames before
emitting any rows. No files moved.

Validation passed:

- `bash -n scripts/mesh-sync-tools scripts/mesh-doctor scripts/lib/mesh-manifest-reader.sh`
- `scripts/mesh-manifest --check` — 1,197 rows, no duplicate installed basenames.
- `bash tests/test-mesh-manifest.sh` — fixture matrix and duplicate guard.
- `bash /home/mesh-home/lte-workstation/tests/test-mesh-manifest-consumers.sh` from `/tmp` —
  nested tool and shim ownership, systemd unit selection, unknown-class and duplicate-basename
  refusal without partial output, same/different/missing deployed parity, and both consumer `--test`
  paths invoked outside the repository.
- `git diff --check` for the changed consumers.

Rollback: revert only this slice's landing through `mesh-land`; it changes no source locations or
runtime unit paths.
