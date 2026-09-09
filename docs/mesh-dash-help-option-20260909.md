# mesh-dash help and bounded sound render verification

Date: 2026-09-09

The live executable resolves to `scripts/mesh-dash`:

```text
/home/mesh-home/lte-workstation/scripts/mesh-dash
```

Regression artifact: `tests/test-mesh-dash-help-option.sh`.

Verified:

- Before the implementation, `timeout 2 scripts/mesh-dash --help` failed with rc 124.
- After the implementation, the regression passed: `test-mesh-dash-help-option: PASS`.
- `timeout 30 scripts/mesh-dash --test-fast` passed.
- `timeout 180 scripts/mesh-dash --test` completed successfully.
- The live symlink path returned the explicit usage text immediately.
- A one-shot sound render remains bounded by `MESH_DASH_SOUND_TIMEOUT` and reports the
  dependency verdict/timeout in the RENDERS header.

Implementation: `-h`/`--help` is handled before role dispatch; `mesh-room-music --diversity`
is bounded (default 15 seconds, configurable) and timeout rc 124 is rendered as a named
`diversity TIMEOUT` diagnosis.
