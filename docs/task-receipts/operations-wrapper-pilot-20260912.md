# Operations wrapper pilot — 2026-09-12

Task: `tg-scripts-layout-migration-20260912/operations-wrapper-pilot` (owner: genome).

Moved the `mesh-model-pin` implementation to `scripts/operations/mesh-model-pin` and retained
`scripts/mesh-model-pin` as an executable compatibility shim. The shim resolves installed symlink
chains to the source checkout before entering the nested implementation, so it does not recurse
through `~/.local/bin`. Its cadence and state declarations remain on the installed top-level owner.
The manifest now classifies the top-level shim as the sole installable `mesh-model-pin`; the nested
implementation remains visible as a non-deployed tool owned by the same compatibility basename.

The caller census found one live runtime caller at `~/.mesh/reflexes.cron:297` (`11,41 * * * *`
invoking `~/.local/bin/mesh-model-pin`) and one source comment in `scripts/mesh-mind-state`. The
installed path is a symlink to the source shim. The cron entry and cadence were not changed.

Verification passed:

```text
scripts/mesh-model-pin --test before the move
  pass: pure verdict arms and live pane read; ledger byte-count unchanged
bash -n scripts/mesh-model-pin scripts/operations/mesh-model-pin
  pass
scripts/mesh-manifest --check
  PASS (1200 complete rows; no duplicate installed basenames)
manifest rows for the pilot
  scripts/mesh-model-pin: operations/tool/install, cadence header
  scripts/operations/mesh-model-pin: operations/tool/none, same compatibility owner
cmp scripts/mesh-model-pin ~/.local/bin/mesh-model-pin
  pass; deployed symlink target is the source shim
(cd /tmp && /home/mesh-home/lte-workstation/scripts/mesh-model-pin --test)
  pass; 15/16 live panes carried a readable engine argv, ledger byte-count unchanged
(cd /tmp && /home/mesh-home/.local/bin/mesh-model-pin --test)
  pass with the same live-read result; proves the installed symlink reaches the nested implementation
scripts/mesh-doctor --test
  pass; manifest inventory checked (Python SyntaxWarnings from embedded test code only)
scripts/mesh-sync-tools --test
  pass; nested manifest parity and shim basename ownership fixture passed
scripts/mesh-autowire --test
  pass
(cd /tmp && ~/.local/bin/mesh-autowire --check)
  pass (exit 0); mesh-model-pin was absent from new-candidate output because its existing cron
  entry is already wired
scripts/mesh-land --test
  pass; nested manifest fixture and branch-override fixture passed
scripts/mesh-vitality --test
  pass
temporary inverse-move rehearsal
  pass; manifest accepted shim+nested-tool shape, then accepted restored top-level-only shape;
  restored implementation bytes matched the moved source
```

Landing: `mesh-land` landed the original implementation at `d9cf26fe`, then landed the top-level
shim at `1db25387`. Both revisions are on `origin/main` (`HEAD == origin/main` at verification).
After deployment, the installed path still resolves to `scripts/mesh-model-pin`, and `cmp` confirms
the deployed shim is byte-identical to the source shim.

Rollback: remove the top-level shim, move `scripts/operations/mesh-model-pin` back to
`scripts/mesh-model-pin`, remove the empty `scripts/operations/` directory, then run
`scripts/mesh-manifest --check` and `scripts/mesh-model-pin --test` from `/tmp`. The inverse move was
rehearsed in an isolated temporary repository; no live cron, service, or deployed file was changed.
