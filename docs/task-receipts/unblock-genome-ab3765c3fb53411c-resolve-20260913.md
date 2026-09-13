# UXN legacy test entrypoint repair

Date: 2026-09-13  
Task: `unblock/genome/ab3765c3fb53411c/resolve`  
Parent: `tg-scripts-layout-migration-20260912/retire-layout-shims`

## Diagnosis and change

The UXN arithmetic test at `scripts/tests/uxn/test-arith32` passed when called at its new
location, but the compatibility symlink `scripts/uxn/test-arith32` failed. The script calculated
its UXN directory from `$0`; through the old symlink, that resolved `../../uxn` from
`scripts/uxn/` to a nonexistent repository-root `uxn/` directory.

The test now resolves a relative or absolute symlink chain before locating its sibling UXN tree.
The layout contract runs the arithmetic test from both its new location and its legacy path while
the test itself starts from outside the repository. Only this arithmetic test slice, its layout
regression, and this receipt are selected for landing.

## Verification

- Before the fix, `bash tests/test-mesh-uxn-layout.sh` failed on the legacy invocation with
  `cd: .../scripts/uxn/../../uxn: No such file or directory`.
- After the fix, `bash tests/test-mesh-uxn-layout.sh` passes from an external working directory;
  both old and new `test-arith32 --test` entrypoints pass, and `bash -n` passes.
- Focused UXN gates also pass: `test-arith64`, `test-sense-gate`, `test-series-stats`,
  `test-spearman`, `test-band-gate`, and `test-rom-binary-contract` with `--test`.
- Landed as three scoped MeshLand commits: `f4577c05` adds the relocated arithmetic driver,
  `9e09c549` retains the legacy symlink, and `acc84077` adds the external-directory regression.
  `git log -1 --format=%s` reports `Verify UXN tests run through relocated and legacy paths`.
- Post-land `scripts/mesh-manifest --check` passes with 1,336 rows and no duplicate installed
  basenames; the external-directory layout test and both arithmetic entrypoints pass from HEAD.

## Remaining blocker

This lands one independently verified migration slice; it does not satisfy the parent retirement
gates. The remaining UXN move is still unlanded, active callers still use old paths, and the
post-land deploy/autowire/doctor cycle plus fresh caller census have not passed. Keep compatibility
paths and leave `retire-layout-shims` blocked until those exact gates pass. Do not resume that parent
step from this slice alone.
