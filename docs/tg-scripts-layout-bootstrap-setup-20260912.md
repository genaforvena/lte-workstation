# Manifest-driven bootstrap and setup installation

This is migration slice 1 of `tg-scripts-layout-migration-20260912`. No source directories or live
deployments were moved.

`bootstrap.sh` now asks `scripts/mesh-manifest-install tools` to link every `install` row into
`~/.local/bin`. Manifest classification retains every executable direct child of `scripts/` that
the old bootstrap glob exposed and includes nested `mesh-*` tools; nested implementations that
already have a top-level compatibility entry remain non-installing rows. `setup.sh` resolves its
explicit `ngrok-notify.sh`, `bore-mtg.sh`, `ngrok.service`, and conditional `bore-mtg.service`
copies through the same manifest. Units still land in `~/.config/systemd/user`.

The helper also supports a bounded rollback for the selected outputs: `rollback-tools` removes only
links whose target is still the manifest source, while `rollback-legacy-bin <names...>` and
`rollback-units <names...>` remove only regular copies that still match their source. The fixture
test installs to temporary directories and exercises all three rollback paths.

Verification performed:

```text
scripts/mesh-manifest --check
  PASS (1192 complete rows; no duplicate installed basenames)
bash tests/test-mesh-manifest.sh
  fixture matrix and duplicate guard pass
bash tests/test-mesh-manifest-install.sh
  fixture deployment, source/deployed basename parity, service ExecStart resolution, and rollback pass
bash -n bootstrap.sh setup.sh scripts/mesh-manifest-install tests/test-mesh-manifest-install.sh
python3 -m py_compile scripts/mesh-manifest
git diff --check
```

An inventory comparison confirmed that the new manifest install rows retain the executable
direct-child names selected by the previous bootstrap glob, with no additional direct-child names.
Bootstrap and setup were not run against the live home directory; deployment effects are covered by
the isolated fixture.
